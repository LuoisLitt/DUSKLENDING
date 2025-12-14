const hre = require("hardhat");
const ethers = hre.ethers;
const fs = require("fs");

async function main() {
  const deploymentPath = `./deployments/${hre.network.name}.json`;
  const deployment = JSON.parse(fs.readFileSync(deploymentPath, "utf8"));
  const [user] = await ethers.getSigners();

  const dusk = await ethers.getContractAt("MockDUSK", deployment.contracts.MockDUSK);
  const pool = await ethers.getContractAt("DuskLendingPool", deployment.contracts.DuskLendingPool);

  // Deposit 100 DUSK as collateral
  const depositAmount = ethers.parseEther("100");

  console.log("💰 Depositing", ethers.formatEther(depositAmount), "DUSK as collateral...\n");

  // Approve
  console.log("📝 Approving DUSK...");
  const approveTx = await dusk.approve(deployment.contracts.DuskLendingPool, depositAmount);
  await approveTx.wait();
  console.log("✅ Approved");

  // Deposit
  console.log("📝 Depositing...");
  const depositTx = await pool.depositDusk(depositAmount);
  await depositTx.wait();
  console.log("✅ Deposited successfully!");

  // Show updated position
  const userData = await pool.users(user.address);
  console.log("\n📊 Your collateral:", ethers.formatEther(userData.duskCollateral), "DUSK");
  console.log("💵 Max borrow amount:", ethers.formatUnits(await pool.getMaxBorrowAmount(user.address), 6), "USDT");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
