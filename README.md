# DUSK Lending Platform

A decentralized lending platform built on DUSK Network, based on AAVE v3 architecture. Deposit DUSK tokens as collateral and borrow USDT against it.

## Overview

This lending platform allows users to:
- 💰 Deposit DUSK tokens as collateral
- 💵 Borrow USDT against DUSK collateral
- 📈 Earn interest on USDT supplied to the pool
- 🔒 Secure overcollateralized lending with 150% collateralization ratio

### Key Features

- **Overcollateralized Lending**: 150% collateralization ratio ensures platform solvency
- **Liquidation Protection**: 125% liquidation threshold protects both borrowers and lenders
- **Interest-Bearing**: Competitive APRs for both borrowers (8%) and suppliers (5%)
- **Based on AAVE v3**: Built on battle-tested DeFi architecture
- **DuskEVM Compatible**: Deployed on DUSK Network's EVM-compatible layer

## Architecture

### Smart Contracts

1. **DuskLendingPool** - Main lending pool contract
   - Manages deposits, withdrawals, borrows, and repayments
   - Handles liquidations of undercollateralized positions
   - Tracks user positions and accrued interest
   - Located: `contracts/core/DuskLendingPool.sol`

2. **MockDUSK** - Test DUSK token (for testnet only)
   - ERC20 token with faucet functionality
   - Located: `contracts/mocks/MockDUSK.sol`

3. **MockUSDT** - Test USDT token (for testnet only)
   - ERC20 token with 6 decimals (matching real USDT)
   - Located: `contracts/mocks/MockUSDT.sol`

### Key Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Collateralization Ratio | 150% | Minimum collateral required to borrow |
| Liquidation Threshold | 125% | Health factor below which positions can be liquidated |
| Liquidation Bonus | 5% | Reward for liquidators |
| Borrow APR | 8% | Annual percentage rate for borrowing |
| Supply APR | 5% | Annual percentage rate for supplying liquidity |

## Getting Started

### Prerequisites

- Node.js v18 or higher
- npm or yarn
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DUSKLENDING
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` and add your private key:
```
PRIVATE_KEY=your_private_key_here
```

### Compile Contracts

```bash
npm run compile
```

### Run Tests

```bash
npm test
```

## Deployment

### Deploy to DUSK Testnet

```bash
npm run deploy:testnet
```

This will:
1. Deploy MockDUSK and MockUSDT tokens
2. Deploy the DuskLendingPool contract
3. Initialize the pool with 100,000 USDT liquidity
4. Save deployment addresses to `deployments/dusk-testnet.json`

### Deploy to DUSK Mainnet

⚠️ **For mainnet deployment, you should use real DUSK and USDT token addresses!**

1. Update `.env` with production RPC URL and private key
2. Modify `scripts/deploy.js` to use real token addresses instead of deploying mocks
3. Run:
```bash
npm run deploy:mainnet
```

## Usage

### 1. Get Test Tokens (Testnet Only)

```bash
node scripts/faucet.js
```

This gives you:
- 1,000 DUSK tokens
- 10,000 USDT tokens

### 2. Check Your Position

```bash
node scripts/interact.js
```

### 3. Deposit DUSK as Collateral

```bash
node scripts/examples/deposit.js
```

Default: Deposits 100 DUSK

### 4. Borrow USDT

```bash
node scripts/examples/borrow.js
```

Default: Borrows 30 USDT

### 5. Repay Loan

```bash
node scripts/examples/repay.js
```

Default: Repays 10 USDT (or full debt if less)

### Custom Interactions

You can interact directly with the contracts using ethers.js:

```javascript
const { ethers } = require("hardhat");

// Get contract instances
const pool = await ethers.getContractAt("DuskLendingPool", poolAddress);
const dusk = await ethers.getContractAt("MockDUSK", duskAddress);

// Deposit DUSK
const depositAmount = ethers.parseEther("100");
await dusk.approve(poolAddress, depositAmount);
await pool.depositDusk(depositAmount);

// Borrow USDT
const borrowAmount = ethers.parseUnits("30", 6);
await pool.borrowUsdt(borrowAmount);
```

## How It Works

### Depositing Collateral

1. User approves DUSK tokens to the lending pool
2. User calls `depositDusk(amount)`
3. DUSK tokens are transferred to the pool
4. User's collateral balance is updated

### Borrowing USDT

1. User calls `borrowUsdt(amount)`
2. Contract checks if user has sufficient collateral (150% ratio)
3. If approved, USDT is transferred to user
4. User's debt is tracked with interest

### Repaying Loans

1. User approves USDT tokens to the lending pool
2. User calls `repayUsdt(amount)`
3. Payment is applied to interest first, then principal
4. User's debt is reduced

### Liquidation

If a user's health factor drops below 1.0 (125% collateralization):
1. Anyone can call `liquidate(borrower, usdtAmount)`
2. Liquidator repays part/all of the debt in USDT
3. Liquidator receives DUSK collateral + 5% bonus
4. This protects the protocol from bad debt

## Calculating Maximum Borrow

Formula:
```
Max Borrow = (Collateral Value in USD) / Collateralization Ratio
```

Example:
- Deposit: 100 DUSK
- DUSK Price: $0.50
- Collateral Value: $50
- Max Borrow: $50 / 1.5 = $33.33 USDT

## Health Factor

Health Factor = (Collateral Value × Liquidation Threshold) / Debt Value

- Health Factor > 1.0: Position is safe
- Health Factor < 1.0: Position can be liquidated

## Project Structure

```
DUSKLENDING/
├── contracts/
│   ├── core/
│   │   ├── DuskLendingPool.sol      # Main lending pool
│   │   └── pool/                     # AAVE core contracts (reference)
│   ├── mocks/
│   │   ├── MockDUSK.sol              # Test DUSK token
│   │   └── MockUSDT.sol              # Test USDT token
│   ├── interfaces/                   # Contract interfaces
│   └── dependencies/                 # External dependencies
├── scripts/
│   ├── deploy.js                     # Deployment script
│   ├── interact.js                   # Check positions
│   ├── faucet.js                     # Get test tokens
│   └── examples/
│       ├── deposit.js                # Deposit example
│       ├── borrow.js                 # Borrow example
│       └── repay.js                  # Repay example
├── test/
│   └── DuskLendingPool.test.js       # Contract tests
├── hardhat.config.js                 # Hardhat configuration
├── package.json                      # Dependencies
└── README.md                         # This file
```

## Security Considerations

⚠️ **This is a demonstration project based on AAVE v3 architecture**

For production use, you should:

1. **Audit the contracts** - Have professional auditors review the code
2. **Use real price oracles** - Integrate Chainlink or similar oracle for DUSK price feeds
3. **Implement timelock** - Add timelock for admin functions
4. **Add emergency pause** - Circuit breaker for emergencies
5. **Gas optimizations** - Optimize for DuskEVM's gas model
6. **Multi-sig ownership** - Use multi-signature wallet for admin functions
7. **Gradual rollout** - Start with caps on deposits/borrows
8. **Bug bounty program** - Incentivize security researchers

## Testing

The project includes comprehensive tests covering:
- ✅ Deposits and withdrawals
- ✅ Borrowing and repayment
- ✅ Interest accrual
- ✅ Liquidations
- ✅ Health factor calculations
- ✅ Access control

Run tests:
```bash
npm test
```

## DUSK Network Integration

### DuskEVM Compatibility

This platform is designed for DUSK Network's EVM-compatible execution environment:

- **EVM Compatibility**: Standard Solidity contracts work on DuskEVM
- **Standard Tooling**: Use Hardhat, Ethers.js, and other Ethereum tools
- **Privacy Features**: Future versions can leverage DUSK's privacy capabilities

### Network Details

**Testnet**:
- RPC URL: `https://rpc.dusk.network/testnet`
- Chain ID: 476 (verify actual chain ID)
- Explorer: TBD

**Mainnet**:
- RPC URL: `https://rpc.dusk.network`
- Chain ID: 477 (verify actual chain ID)
- Explorer: TBD

## Roadmap

Future enhancements:

- [ ] Integration with Chainlink price oracles
- [ ] Support for multiple collateral types
- [ ] Flash loans functionality
- [ ] Governance token and DAO
- [ ] Privacy-preserving features using DUSK technology
- [ ] Interest rate optimization based on utilization
- [ ] Liquidation bot for automated liquidations
- [ ] Web UI for easier interaction

## Based on AAVE v3

This project is based on the AAVE v3 protocol:
- GitHub: https://github.com/aave-dao/aave-v3-origin
- Documentation: https://docs.aave.com/developers/

## Resources

- [DUSK Network](https://dusk.network/)
- [DUSK GitHub](https://github.com/dusk-network)
- [DUSK Documentation](https://docs.dusk.network/)
- [DuskEVM Information](https://dusk.network/news/third-party-smart-contracts-on-mainnet)
- [AAVE v3 Documentation](https://docs.aave.com/developers/)
- [AAVE v3 Smart Contracts](https://github.com/aave-dao/aave-v3-origin)

## License

MIT License - see LICENSE file for details

## Disclaimer

This software is provided "as is", without warranty of any kind. Use at your own risk. This is experimental software and should not be used in production without proper audits and testing.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## Support

For questions or issues:
- Open an issue on GitHub
- Check DUSK Network documentation
- Join DUSK Network Discord

---

Built with ❤️ for the DUSK Network ecosystem
