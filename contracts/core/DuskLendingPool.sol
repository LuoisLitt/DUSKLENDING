// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/**
 * @title DuskLendingPool
 * @notice A simplified lending pool for DUSK network
 * @dev Users can deposit DUSK as collateral and borrow USDT
 * Based on AAVE v3 architecture but simplified for single collateral/borrow pair
 */
contract DuskLendingPool is Ownable, ReentrancyGuard {
    using SafeERC20 for IERC20;

    // ============ State Variables ============

    IERC20 public immutable duskToken;
    IERC20 public immutable usdtToken;

    // Collateralization ratio: 150% (stored as 15000 basis points)
    uint256 public constant COLLATERALIZATION_RATIO = 15000; // 150%
    uint256 public constant LIQUIDATION_THRESHOLD = 12500; // 125%
    uint256 public constant LIQUIDATION_BONUS = 10500; // 105% - liquidator gets 5% bonus
    uint256 public constant BASIS_POINTS = 10000;

    // Interest rates (annual percentage rate in basis points)
    uint256 public borrowAPR = 800; // 8% APR (borrower rate)
    uint256 public supplyAPR = 500; // 5% APR (lender rate)

    // Pool reserves
    uint256 public totalDuskDeposited;
    uint256 public totalUsdtLiquidity;
    uint256 public totalUsdtBorrowed;

    // User data
    struct UserData {
        uint256 duskCollateral;
        uint256 usdtBorrowed;
        uint256 lastUpdateTimestamp;
        uint256 accruedInterest;
    }

    mapping(address => UserData) public users;

    // Price oracle (simplified - in production, use Chainlink or similar)
    uint256 public duskPriceUSD; // Price in USD with 8 decimals (like Chainlink)

    // ============ Events ============

    event DuskDeposited(address indexed user, uint256 amount);
    event DuskWithdrawn(address indexed user, uint256 amount);
    event UsdtBorrowed(address indexed user, uint256 amount);
    event UsdtRepaid(address indexed user, uint256 amount);
    event UsdtSupplied(address indexed supplier, uint256 amount);
    event UsdtWithdrawnBySupplier(address indexed supplier, uint256 amount);
    event Liquidation(
        address indexed liquidator,
        address indexed borrower,
        uint256 duskSeized,
        uint256 usdtRepaid
    );
    event PriceUpdated(uint256 newPrice);
    event InterestRateUpdated(uint256 borrowAPR, uint256 supplyAPR);

    // ============ Constructor ============

    /**
     * @notice Initialize the lending pool
     * @param _duskToken Address of DUSK token
     * @param _usdtToken Address of USDT token
     * @param _initialDuskPrice Initial DUSK price in USD (8 decimals)
     */
    constructor(
        address _duskToken,
        address _usdtToken,
        uint256 _initialDuskPrice
    ) Ownable(msg.sender) {
        require(_duskToken != address(0), "Invalid DUSK address");
        require(_usdtToken != address(0), "Invalid USDT address");
        require(_initialDuskPrice > 0, "Invalid price");

        duskToken = IERC20(_duskToken);
        usdtToken = IERC20(_usdtToken);
        duskPriceUSD = _initialDuskPrice;
    }

    // ============ Core Functions ============

    /**
     * @notice Deposit DUSK as collateral
     * @param amount Amount of DUSK to deposit
     */
    function depositDusk(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be > 0");

        _updateInterest(msg.sender);

        duskToken.safeTransferFrom(msg.sender, address(this), amount);

        users[msg.sender].duskCollateral += amount;
        totalDuskDeposited += amount;

        emit DuskDeposited(msg.sender, amount);
    }

    /**
     * @notice Withdraw DUSK collateral
     * @param amount Amount of DUSK to withdraw
     */
    function withdrawDusk(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be > 0");
        require(users[msg.sender].duskCollateral >= amount, "Insufficient collateral");

        _updateInterest(msg.sender);

        users[msg.sender].duskCollateral -= amount;
        totalDuskDeposited -= amount;

        // Check if user still has sufficient collateral
        require(_isHealthy(msg.sender), "Insufficient collateral ratio");

        duskToken.safeTransfer(msg.sender, amount);

        emit DuskWithdrawn(msg.sender, amount);
    }

    /**
     * @notice Borrow USDT against DUSK collateral
     * @param amount Amount of USDT to borrow
     */
    function borrowUsdt(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be > 0");
        require(totalUsdtLiquidity >= totalUsdtBorrowed + amount, "Insufficient liquidity");

        _updateInterest(msg.sender);

        users[msg.sender].usdtBorrowed += amount;
        totalUsdtBorrowed += amount;

        // Check collateralization ratio
        require(_isHealthy(msg.sender), "Insufficient collateral");

        usdtToken.safeTransfer(msg.sender, amount);

        emit UsdtBorrowed(msg.sender, amount);
    }

    /**
     * @notice Repay USDT loan
     * @param amount Amount of USDT to repay
     */
    function repayUsdt(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be > 0");

        _updateInterest(msg.sender);

        uint256 totalDebt = users[msg.sender].usdtBorrowed + users[msg.sender].accruedInterest;
        require(totalDebt > 0, "No debt to repay");

        uint256 repayAmount = amount > totalDebt ? totalDebt : amount;

        usdtToken.safeTransferFrom(msg.sender, address(this), repayAmount);

        // First repay accrued interest, then principal
        if (users[msg.sender].accruedInterest >= repayAmount) {
            users[msg.sender].accruedInterest -= repayAmount;
        } else {
            uint256 remainingRepay = repayAmount - users[msg.sender].accruedInterest;
            users[msg.sender].accruedInterest = 0;
            users[msg.sender].usdtBorrowed -= remainingRepay;
            totalUsdtBorrowed -= remainingRepay;
        }

        emit UsdtRepaid(msg.sender, repayAmount);
    }

    /**
     * @notice Supply USDT to the lending pool
     * @param amount Amount of USDT to supply
     */
    function supplyUsdt(uint256 amount) external nonReentrant {
        require(amount > 0, "Amount must be > 0");

        usdtToken.safeTransferFrom(msg.sender, address(this), amount);
        totalUsdtLiquidity += amount;

        // In a full implementation, we would mint aTokens here
        // For simplicity, we're just tracking the liquidity

        emit UsdtSupplied(msg.sender, amount);
    }

    /**
     * @notice Liquidate an undercollateralized position
     * @param borrower Address of the borrower to liquidate
     * @param usdtAmount Amount of USDT debt to repay
     */
    function liquidate(address borrower, uint256 usdtAmount) external nonReentrant {
        require(borrower != address(0), "Invalid borrower");
        require(usdtAmount > 0, "Amount must be > 0");

        _updateInterest(borrower);

        // Check if position is liquidatable
        require(!_isHealthy(borrower), "Position is healthy");

        uint256 totalDebt = users[borrower].usdtBorrowed + users[borrower].accruedInterest;
        require(totalDebt > 0, "No debt");

        uint256 repayAmount = usdtAmount > totalDebt ? totalDebt : usdtAmount;

        // Calculate DUSK to seize (with liquidation bonus)
        uint256 usdtValueUSD = repayAmount * 1e8 / 1e6; // Convert USDT to USD (assuming 6 decimals)
        uint256 duskToSeize = (usdtValueUSD * 1e18 * LIQUIDATION_BONUS) / (duskPriceUSD * BASIS_POINTS);

        require(users[borrower].duskCollateral >= duskToSeize, "Insufficient collateral to seize");

        // Transfer USDT from liquidator
        usdtToken.safeTransferFrom(msg.sender, address(this), repayAmount);

        // Update borrower's position
        if (users[borrower].accruedInterest >= repayAmount) {
            users[borrower].accruedInterest -= repayAmount;
        } else {
            uint256 remainingRepay = repayAmount - users[borrower].accruedInterest;
            users[borrower].accruedInterest = 0;
            users[borrower].usdtBorrowed -= remainingRepay;
            totalUsdtBorrowed -= remainingRepay;
        }

        users[borrower].duskCollateral -= duskToSeize;
        totalDuskDeposited -= duskToSeize;

        // Transfer DUSK to liquidator
        duskToken.safeTransfer(msg.sender, duskToSeize);

        emit Liquidation(msg.sender, borrower, duskToSeize, repayAmount);
    }

    // ============ View Functions ============

    /**
     * @notice Get user's total debt including interest
     * @param user Address of the user
     */
    function getUserDebt(address user) public view returns (uint256) {
        return users[user].usdtBorrowed + _calculateAccruedInterest(user);
    }

    /**
     * @notice Get user's health factor
     * @param user Address of the user
     * @return Health factor (1e18 = 100%)
     */
    function getHealthFactor(address user) public view returns (uint256) {
        uint256 totalDebt = getUserDebt(user);
        if (totalDebt == 0) return type(uint256).max;

        uint256 collateralValueUSD = (users[user].duskCollateral * duskPriceUSD) / 1e18;
        uint256 debtValueUSD = totalDebt * 1e8 / 1e6;

        return (collateralValueUSD * 1e18 * BASIS_POINTS) / (debtValueUSD * LIQUIDATION_THRESHOLD);
    }

    /**
     * @notice Get maximum amount user can borrow
     * @param user Address of the user
     */
    function getMaxBorrowAmount(address user) public view returns (uint256) {
        uint256 collateralValueUSD = (users[user].duskCollateral * duskPriceUSD) / 1e18;
        uint256 maxBorrowUSD = (collateralValueUSD * BASIS_POINTS) / COLLATERALIZATION_RATIO;
        uint256 maxBorrowUsdt = (maxBorrowUSD * 1e6) / 1e8;

        uint256 currentDebt = getUserDebt(user);
        if (maxBorrowUsdt <= currentDebt) return 0;

        uint256 availableToBorrow = maxBorrowUsdt - currentDebt;
        uint256 poolLiquidity = totalUsdtLiquidity - totalUsdtBorrowed;

        return availableToBorrow < poolLiquidity ? availableToBorrow : poolLiquidity;
    }

    // ============ Internal Functions ============

    /**
     * @notice Check if user's position is healthy
     */
    function _isHealthy(address user) internal view returns (bool) {
        return getHealthFactor(user) >= 1e18;
    }

    /**
     * @notice Update accrued interest for a user
     */
    function _updateInterest(address user) internal {
        uint256 newInterest = _calculateAccruedInterest(user);
        users[user].accruedInterest += newInterest;
        users[user].lastUpdateTimestamp = block.timestamp;
    }

    /**
     * @notice Calculate accrued interest since last update
     */
    function _calculateAccruedInterest(address user) internal view returns (uint256) {
        if (users[user].usdtBorrowed == 0) return 0;

        uint256 timeElapsed = block.timestamp - users[user].lastUpdateTimestamp;
        if (timeElapsed == 0) return users[user].accruedInterest;

        // Simple interest calculation: principal * rate * time / (seconds in year * basis points)
        uint256 principal = users[user].usdtBorrowed;
        return (principal * borrowAPR * timeElapsed) / (365 days * BASIS_POINTS);
    }

    // ============ Admin Functions ============

    /**
     * @notice Update DUSK price (in production, use oracle)
     * @param newPrice New DUSK price in USD (8 decimals)
     */
    function updateDuskPrice(uint256 newPrice) external onlyOwner {
        require(newPrice > 0, "Invalid price");
        duskPriceUSD = newPrice;
        emit PriceUpdated(newPrice);
    }

    /**
     * @notice Update interest rates
     * @param _borrowAPR New borrow APR in basis points
     * @param _supplyAPR New supply APR in basis points
     */
    function updateInterestRates(uint256 _borrowAPR, uint256 _supplyAPR) external onlyOwner {
        require(_borrowAPR > _supplyAPR, "Borrow rate must be > supply rate");
        borrowAPR = _borrowAPR;
        supplyAPR = _supplyAPR;
        emit InterestRateUpdated(_borrowAPR, _supplyAPR);
    }

    /**
     * @notice Emergency withdraw (admin only)
     */
    function emergencyWithdraw(address token, uint256 amount) external onlyOwner {
        IERC20(token).safeTransfer(owner(), amount);
    }
}
