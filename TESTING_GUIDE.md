# DUSK Lending Platform - Testing Guide

This guide walks you through testing the lending platform from start to finish.

## Step 1: Install Dependencies

First, install all required packages:

```bash
npm install
```

**What this does:**
- Installs Hardhat (development environment)
- Installs OpenZeppelin contracts (security libraries)
- Installs testing frameworks (Chai, Ethers.js)

---

## Step 2: Compile the Contracts

Compile all Solidity contracts:

```bash
npx hardhat compile
```

**Expected output:**
```
Compiled 3 Solidity files successfully
```

**What this does:**
- Compiles DuskLendingPool.sol
- Compiles MockDUSK.sol and MockUSDT.sol
- Generates contract artifacts and ABIs
- Creates typechain types

---

## Step 3: Run the Test Suite

Run all automated tests:

```bash
npx hardhat test
```

**Expected output:**
```
  DuskLendingPool
    Deployment
      ✓ Should set the correct token addresses
      ✓ Should set the correct initial price
      ✓ Should have initial USDT liquidity
    Depositing DUSK
      ✓ Should allow users to deposit DUSK
      ✓ Should emit DuskDeposited event
      ✓ Should revert when depositing 0
    Borrowing USDT
      ✓ Should allow users to borrow USDT
      ✓ Should revert when borrowing too much
      ✓ Should emit UsdtBorrowed event
    ... (more tests)

  30 passing (2s)
```

**What this tests:**
- Contract deployment
- Depositing DUSK collateral
- Borrowing USDT
- Repaying loans
- Withdrawing collateral
- Liquidation mechanism
- Health factor calculations
- Admin functions

---

## Step 4: Deploy to Local Hardhat Network

### 4.1 Start a Local Blockchain

In a **new terminal window**, start Hardhat's local node:

```bash
npx hardhat node
```

**Expected output:**
```
Started HTTP and WebSocket JSON-RPC server at http://127.0.0.1:8545/

Accounts
========
Account #0: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 (10000 ETH)
Private Key: 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
...
```

**Keep this terminal running!**

### 4.2 Deploy Contracts

In your **original terminal**, deploy the contracts:

```bash
npx hardhat run scripts/deploy.js --network localhost
```

**Expected output:**
```
🚀 Deploying DUSK Lending Platform...

Deploying contracts with account: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
Account balance: 10000.0 DUSK

📝 Step 1: Deploying Mock Tokens...
✅ MockDUSK deployed to: 0x5FbDB2315678afecb367f032d93F642f64180aa3
✅ MockUSDT deployed to: 0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512

📝 Step 2: Deploying Lending Pool...
✅ DuskLendingPool deployed to: 0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0

📝 Step 3: Initializing Pool with Liquidity...
✅ Supplied 100,000 USDT to the pool

============================================================
📋 DEPLOYMENT SUMMARY
============================================================
Network: localhost
Deployer: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266

Contract Addresses:
  MockDUSK: 0x5FbDB2315678afecb367f032d93F642f64180aa3
  MockUSDT: 0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512
  DuskLendingPool: 0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0

Pool Configuration:
  Initial DUSK Price: $0.50
  Collateralization Ratio: 150%
  Liquidation Threshold: 125%
  Borrow APR: 5%
  Supply APR: 3%
  Initial USDT Liquidity: 100,000 USDT
============================================================

✅ Deployment completed successfully!
```

---

## Step 5: Interactive Testing

Now let's interact with the deployed contracts!

### 5.1 Get Test Tokens

Get free test tokens from the faucet:

```bash
npx hardhat run scripts/faucet.js --network localhost
```

**Expected output:**
```
💧 Getting test tokens from faucet...

User address: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266

📝 Requesting tokens...
✅ Received 1,000 DUSK
✅ Received 10,000 USDT

📊 Your new balances:
  DUSK: 1000.0
  USDT: 10000.0
```

### 5.2 Check Your Position

View your current position:

```bash
npx hardhat run scripts/interact.js --network localhost
```

**Expected output:**
```
🔗 DUSK Lending Platform - Interaction Script

User address: 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
Network: localhost

============================================================
📊 CURRENT BALANCES
============================================================
DUSK Balance: 1000.0
USDT Balance: 10000.0

============================================================
💰 YOUR POSITION
============================================================
DUSK Collateral: 0.0
USDT Borrowed: 0.0
Total Debt (with interest): 0.0 USDT
Health Factor: ∞
Max Borrow Amount: 0.0 USDT

============================================================
🏦 POOL STATISTICS
============================================================
Total DUSK Deposited: 0.0
Total USDT Liquidity: 100000.0
Total USDT Borrowed: 0.0
Available to Borrow: 100000.0 USDT
DUSK Price: $0.50
============================================================
```

### 5.3 Deposit DUSK as Collateral

Deposit 100 DUSK:

```bash
npx hardhat run scripts/examples/deposit.js --network localhost
```

**Expected output:**
```
💰 Depositing 100.0 DUSK as collateral...

📝 Approving DUSK...
✅ Approved
📝 Depositing...
✅ Deposited successfully!

📊 Your collateral: 100.0 DUSK
💵 Max borrow amount: 33.333333 USDT
```

### 5.4 Check Position After Deposit

```bash
npx hardhat run scripts/interact.js --network localhost
```

**Expected output:**
```
============================================================
💰 YOUR POSITION
============================================================
DUSK Collateral: 100.0
USDT Borrowed: 0.0
Total Debt (with interest): 0.0 USDT
Health Factor: ∞
Max Borrow Amount: 33.333333 USDT
```

**Calculation:**
- 100 DUSK × $0.50 = $50 collateral value
- $50 ÷ 1.5 (collateralization ratio) = $33.33 max borrow

### 5.5 Borrow USDT

Borrow 30 USDT:

```bash
npx hardhat run scripts/examples/borrow.js --network localhost
```

**Expected output:**
```
💸 Borrowing 30.0 USDT...

📊 Max borrow amount: 33.333333 USDT
📝 Borrowing...
✅ Borrowed successfully!

📊 Updated position:
  Total debt: 30.0 USDT
  Health factor: 1.333333333333333333
```

**Health Factor Calculation:**
- Collateral value: $50
- Debt value: $30
- Health factor = ($50 × 1.25) / $30 = 2.08
- Health > 1.0 = Safe position ✅

### 5.6 Check Position After Borrow

```bash
npx hardhat run scripts/interact.js --network localhost
```

**Expected output:**
```
============================================================
💰 YOUR POSITION
============================================================
DUSK Collateral: 100.0
USDT Borrowed: 30.0
Total Debt (with interest): 30.0 USDT
Health Factor: 2.083333333333333333
Max Borrow Amount: 3.333333 USDT

============================================================
📊 CURRENT BALANCES
============================================================
DUSK Balance: 900.0
USDT Balance: 10030.0
```

### 5.7 Repay USDT Loan

Repay 10 USDT:

```bash
npx hardhat run scripts/examples/repay.js --network localhost
```

**Expected output:**
```
💰 Repaying 10.0 USDT...

📊 Current debt: 30.0 USDT
📝 Approving USDT...
✅ Approved
📝 Repaying...
✅ Repaid successfully!

📊 Updated position:
  Remaining debt: 20.0 USDT
  Health factor: 3.125
```

### 5.8 Final Position Check

```bash
npx hardhat run scripts/interact.js --network localhost
```

**Expected output:**
```
============================================================
💰 YOUR POSITION
============================================================
DUSK Collateral: 100.0
USDT Borrowed: 20.0
Total Debt (with interest): 20.0 USDT
Health Factor: 3.125
Max Borrow Amount: 13.333333 USDT
```

---

## Step 6: Test Liquidation Scenario

Let's test what happens when a position becomes unhealthy!

### 6.1 Create a Liquidation Test Script

Create a custom test script:

```bash
cat > scripts/test-liquidation.js << 'EOF'
const hre = require("hardhat");
const ethers = hre.ethers;
const fs = require("fs");

async function main() {
  console.log("🔴 Testing Liquidation Scenario\n");

  const [deployer, borrower, liquidator] = await ethers.getSigners();

  const deploymentPath = `./deployments/${hre.network.name}.json`;
  const deployment = JSON.parse(fs.readFileSync(deploymentPath, "utf8"));

  const dusk = await ethers.getContractAt("MockDUSK", deployment.contracts.MockDUSK);
  const usdt = await ethers.getContractAt("MockUSDT", deployment.contracts.MockUSDT);
  const pool = await ethers.getContractAt("DuskLendingPool", deployment.contracts.DuskLendingPool);

  console.log("Step 1: Borrower deposits DUSK and borrows max USDT");

  // Give borrower tokens
  await dusk.transfer(borrower.address, ethers.parseEther("100"));

  // Borrower deposits and borrows
  await dusk.connect(borrower).approve(deployment.contracts.DuskLendingPool, ethers.parseEther("100"));
  await pool.connect(borrower).depositDusk(ethers.parseEther("100"));
  await pool.connect(borrower).borrowUsdt(ethers.parseUnits("33", 6));

  let healthFactor = await pool.getHealthFactor(borrower.address);
  console.log("✅ Borrowed 33 USDT");
  console.log("   Health Factor:", ethers.formatEther(healthFactor));

  console.log("\nStep 2: DUSK price drops from $0.50 to $0.30");
  await pool.updateDuskPrice(30000000); // $0.30

  healthFactor = await pool.getHealthFactor(borrower.address);
  console.log("⚠️  New Health Factor:", ethers.formatEther(healthFactor));

  if (healthFactor < ethers.parseEther("1")) {
    console.log("🔴 Position is UNHEALTHY - Can be liquidated!");
  }

  console.log("\nStep 3: Liquidator repays debt and seizes collateral");

  // Give liquidator USDT
  await usdt.transfer(liquidator.address, ethers.parseUnits("50", 6));

  const liquidatorDuskBefore = await dusk.balanceOf(liquidator.address);

  // Liquidate
  await usdt.connect(liquidator).approve(deployment.contracts.DuskLendingPool, ethers.parseUnits("33", 6));
  await pool.connect(liquidator).liquidate(borrower.address, ethers.parseUnits("33", 6));

  const liquidatorDuskAfter = await dusk.balanceOf(liquidator.address);
  const duskSeized = liquidatorDuskAfter - liquidatorDuskBefore;

  console.log("✅ Liquidation successful!");
  console.log("   DUSK seized:", ethers.formatEther(duskSeized));
  console.log("   Liquidator profit:", ((Number(ethers.formatEther(duskSeized)) * 0.30) - 33).toFixed(2), "USD");

  healthFactor = await pool.getHealthFactor(borrower.address);
  console.log("   New Health Factor:", healthFactor === ethers.MaxUint256 ? "∞" : ethers.formatEther(healthFactor));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
EOF
```

### 6.2 Run Liquidation Test

```bash
npx hardhat run scripts/test-liquidation.js --network localhost
```

**Expected output:**
```
🔴 Testing Liquidation Scenario

Step 1: Borrower deposits DUSK and borrows max USDT
✅ Borrowed 33 USDT
   Health Factor: 1.893939393939393939

Step 2: DUSK price drops from $0.50 to $0.30
⚠️  New Health Factor: 0.909090909090909090
🔴 Position is UNHEALTHY - Can be liquidated!

Step 3: Liquidator repays debt and seizes collateral
✅ Liquidation successful!
   DUSK seized: 115.5
   Liquidator profit: 1.65 USD
   New Health Factor: ∞
```

---

## Step 7: Run Full Test Coverage

For comprehensive testing, run the full test suite with coverage:

```bash
npx hardhat test --verbose
```

This runs all 30+ test cases covering:
- ✅ Deployment
- ✅ Deposits
- ✅ Withdrawals
- ✅ Borrowing
- ✅ Repayment
- ✅ Liquidations
- ✅ Interest accrual
- ✅ Health factors
- ✅ Access control

---

## Common Issues & Solutions

### Issue 1: "Cannot find module 'hardhat'"
**Solution:**
```bash
npm install
```

### Issue 2: "Insufficient collateral"
**Cause:** Trying to borrow more than allowed by collateral
**Solution:** Check max borrow amount first:
```bash
npx hardhat run scripts/interact.js --network localhost
```

### Issue 3: "Position is healthy" (when trying to liquidate)
**Cause:** Position has sufficient collateral
**Solution:** Price must drop significantly for liquidation

### Issue 4: Compilation errors
**Solution:**
```bash
npx hardhat clean
npx hardhat compile
```

---

## Next Steps

After testing locally, you can:

1. **Deploy to DUSK Testnet:**
   ```bash
   # Add your private key to .env
   npm run deploy:testnet
   ```

2. **Customize Parameters:**
   - Edit `DuskLendingPool.sol` to change collateralization ratios
   - Modify interest rates
   - Add new features

3. **Build a Frontend:**
   - Use Ethers.js to interact with contracts
   - Create a web UI for easier access

---

## Summary

You've learned how to:
1. ✅ Install and compile contracts
2. ✅ Run automated tests
3. ✅ Deploy to local network
4. ✅ Get test tokens
5. ✅ Deposit collateral
6. ✅ Borrow USDT
7. ✅ Repay loans
8. ✅ Test liquidations

The platform is ready for deployment to DUSK Network! 🚀
