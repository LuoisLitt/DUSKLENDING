const hre = require("hardhat");
const ethers = hre.ethers;
const fs = require("fs");

async function main() {
  console.log("🔗 DUSK Lending Platform - Interaction Script\n");

  // Load deployment info
  const deploymentPath = `./deployments/${hre.network.name}.json`;
  if (!fs.existsSync(deploymentPath)) {
    console.error("❌ Deployment file not found. Please deploy first!");
    process.exit(1);
  }

  const deployment = JSON.parse(fs.readFileSync(deploymentPath, "utf8"));
  const [user] = await ethers.getSigners();

  console.log("User address:", user.address);
  console.log("Network:", hre.network.name, "\n");

  // Get contract instances
  const dusk = await ethers.getContractAt("MockDUSK", deployment.contracts.MockDUSK);
  const usdt = await ethers.getContractAt("MockUSDT", deployment.contracts.MockUSDT);
  const pool = await ethers.getContractAt("DuskLendingPool", deployment.contracts.DuskLendingPool);

  console.log("=".repeat(60));
  console.log("📊 CURRENT BALANCES");
  console.log("=".repeat(60));

  const duskBalance = await dusk.balanceOf(user.address);
  const usdtBalance = await usdt.balanceOf(user.address);
  console.log("DUSK Balance:", ethers.formatEther(duskBalance));
  console.log("USDT Balance:", ethers.formatUnits(usdtBalance, 6));

  // Get user position
  const userData = await pool.users(user.address);
  const totalDebt = await pool.getUserDebt(user.address);
  const healthFactor = await pool.getHealthFactor(user.address);
  const maxBorrow = await pool.getMaxBorrowAmount(user.address);

  console.log("\n" + "=".repeat(60));
  console.log("💰 YOUR POSITION");
  console.log("=".repeat(60));
  console.log("DUSK Collateral:", ethers.formatEther(userData.duskCollateral));
  console.log("USDT Borrowed:", ethers.formatUnits(userData.usdtBorrowed, 6));
  console.log("Total Debt (with interest):", ethers.formatUnits(totalDebt, 6), "USDT");
  console.log("Health Factor:", healthFactor === ethers.MaxUint256 ? "∞" : ethers.formatEther(healthFactor));
  console.log("Max Borrow Amount:", ethers.formatUnits(maxBorrow, 6), "USDT");

  // Get pool stats
  const totalDuskDeposited = await pool.totalDuskDeposited();
  const totalUsdtLiquidity = await pool.totalUsdtLiquidity();
  const totalUsdtBorrowed = await pool.totalUsdtBorrowed();
  const duskPrice = await pool.duskPriceUSD();

  console.log("\n" + "=".repeat(60));
  console.log("🏦 POOL STATISTICS");
  console.log("=".repeat(60));
  console.log("Total DUSK Deposited:", ethers.formatEther(totalDuskDeposited));
  console.log("Total USDT Liquidity:", ethers.formatUnits(totalUsdtLiquidity, 6));
  console.log("Total USDT Borrowed:", ethers.formatUnits(totalUsdtBorrowed, 6));
  console.log("Available to Borrow:", ethers.formatUnits(totalUsdtLiquidity - totalUsdtBorrowed, 6), "USDT");
  console.log("DUSK Price:", "$" + (Number(duskPrice) / 1e8).toFixed(2));
  console.log("=".repeat(60));

  console.log("\n📖 Available Actions:");
  console.log("  1. Get test tokens: node scripts/faucet.js");
  console.log("  2. Deposit DUSK: node scripts/examples/deposit.js");
  console.log("  3. Borrow USDT: node scripts/examples/borrow.js");
  console.log("  4. Repay USDT: node scripts/examples/repay.js");
  console.log("  5. Withdraw DUSK: node scripts/examples/withdraw.js");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
