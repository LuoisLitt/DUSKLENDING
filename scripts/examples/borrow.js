const hre = require("hardhat");
const ethers = hre.ethers;
const fs = require("fs");

async function main() {
  const deploymentPath = `./deployments/${hre.network.name}.json`;
  const deployment = JSON.parse(fs.readFileSync(deploymentPath, "utf8"));
  const [user] = await ethers.getSigners();

  const pool = await ethers.getContractAt("DuskLendingPool", deployment.contracts.DuskLendingPool);

  // Borrow 30 USDT
  const borrowAmount = ethers.parseUnits("30", 6);

  console.log("💸 Borrowing", ethers.formatUnits(borrowAmount, 6), "USDT...\n");

  const maxBorrow = await pool.getMaxBorrowAmount(user.address);
  console.log("📊 Max borrow amount:", ethers.formatUnits(maxBorrow, 6), "USDT");

  if (borrowAmount > maxBorrow) {
    console.error("❌ Borrow amount exceeds maximum!");
    process.exit(1);
  }

  console.log("📝 Borrowing...");
  const borrowTx = await pool.borrowUsdt(borrowAmount);
  await borrowTx.wait();
  console.log("✅ Borrowed successfully!");

  // Show updated position
  const healthFactor = await pool.getHealthFactor(user.address);
  const totalDebt = await pool.getUserDebt(user.address);

  console.log("\n📊 Updated position:");
  console.log("  Total debt:", ethers.formatUnits(totalDebt, 6), "USDT");
  console.log("  Health factor:", ethers.formatEther(healthFactor));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
