// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title MockDUSK
 * @notice Mock DUSK token for testing purposes
 * @dev This is for testing only. On mainnet, use the actual DUSK token
 */
contract MockDUSK is ERC20, Ownable {
    uint8 private _decimals;

    constructor() ERC20("DUSK Network", "DUSK") Ownable(msg.sender) {
        _decimals = 18;
        // Mint initial supply for testing (1 million DUSK)
        _mint(msg.sender, 1_000_000 * 10**18);
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
     * @notice Faucet function for testing - anyone can get 1000 DUSK
     */
    function faucet() external {
        _mint(msg.sender, 1000 * 10**18);
    }

    function decimals() public view virtual override returns (uint8) {
        return _decimals;
    }
}
