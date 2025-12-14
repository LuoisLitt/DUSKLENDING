const hre = require("hardhat");
const ethers = hre.ethers;
const fs = require("fs");

async function main() {
  const deploymentPath = `./deployments/${hre.network.name}.json`;
  const deployment = JSON.parse(fs.readFileSync(deploymentPath, "utf8"));
  const [user] = await ethers.getSigners();

  const usdt = await ethers.getContractAt("MockUSDT", deployment.contracts.MockUSDT);
  const pool = await ethers.getContractAt("DuskLendingPool", deployment.contracts.DuskLendingPool);

  const totalDebt = await pool.getUserDebt(user.address);

  if (totalDebt === 0n) {
    console.log("✅ No debt to repay!");
    process.exit(0);
  }

  // Repay 10 USDT or full debt if less
  const repayAmount = totalDebt < ethers.parseUnits("10", 6) ? totalDebt : ethers.parseUnits("10", 6);

  console.log("💰 Repaying", ethers.formatUnits(repayAmount, 6), "USDT...\n");
  console.log("📊 Current debt:", ethers.formatUnits(totalDebt, 6), "USDT");

  // Approve
  console.log("📝 Approving USDT...");
  const approveTx = await usdt.approve(deployment.contracts.DuskLendingPool, repayAmount);
  await approveTx.wait();
  console.log("✅ Approved");

  // Repay
  console.log("📝 Repaying...");
  const repayTx = await pool.repayUsdt(repayAmount);
  await repayTx.wait();
  console.log("✅ Repaid successfully!");

  // Show updated position
  const newDebt = await pool.getUserDebt(user.address);
  const healthFactor = await pool.getHealthFactor(user.address);

  console.log("\n📊 Updated position:");
  console.log("  Remaining debt:", ethers.formatUnits(newDebt, 6), "USDT");
  console.log("  Health factor:", healthFactor === ethers.MaxUint256 ? "∞" : ethers.formatEther(healthFactor));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
