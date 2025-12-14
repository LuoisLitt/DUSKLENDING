const hre = require("hardhat");
const ethers = hre.ethers;
const fs = require("fs");

async function main() {
  console.log("💧 Getting test tokens from faucet...\n");

  const deploymentPath = `./deployments/${hre.network.name}.json`;
  if (!fs.existsSync(deploymentPath)) {
    console.error("❌ Deployment file not found. Please deploy first!");
    process.exit(1);
  }

  const deployment = JSON.parse(fs.readFileSync(deploymentPath, "utf8"));
  const [user] = await ethers.getSigners();

  console.log("User address:", user.address);

  const dusk = await ethers.getContractAt("MockDUSK", deployment.contracts.MockDUSK);
  const usdt = await ethers.getContractAt("MockUSDT", deployment.contracts.MockUSDT);

  console.log("\n📝 Requesting tokens...");

  const tx1 = await dusk.faucet();
  await tx1.wait();
  console.log("✅ Received 1,000 DUSK");

  const tx2 = await usdt.faucet();
  await tx2.wait();
  console.log("✅ Received 10,000 USDT");

  const duskBalance = await dusk.balanceOf(user.address);
  const usdtBalance = await usdt.balanceOf(user.address);

  console.log("\n📊 Your new balances:");
  console.log("  DUSK:", ethers.formatEther(duskBalance));
  console.log("  USDT:", ethers.formatUnits(usdtBalance, 6));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
