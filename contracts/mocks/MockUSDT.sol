// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title MockUSDT
 * @notice Mock USDT token for testing purposes
 * @dev This is for testing only. On mainnet, use the actual USDT token or a bridged version
 */
contract MockUSDT is ERC20, Ownable {
    uint8 private _decimals;

    constructor() ERC20("Tether USD", "USDT") Ownable(msg.sender) {
        _decimals = 6; // USDT typically has 6 decimals
        // Mint initial supply for testing (1 million USDT)
        _mint(msg.sender, 1_000_000 * 10**6);
    }

    /**
     * @notice Mint tokens (for testing only)
     * @param to Address to receive tokens
     * @param amount Amount to mint
     */
    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }

    /**
     * @notice Faucet function for testing - anyone can get 10000 USDT
     */
    function faucet() external {
        _mint(msg.sender, 10000 * 10**6);
    }

    function decimals() public view virtual override returns (uint8) {
        return _decimals;
    }
}
