const hre = require("hardhat");
const ethers = hre.ethers;

async function main() {
  console.log("🚀 Deploying DUSK Lending Platform...\n");

  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);
  console.log("Account balance:", ethers.formatEther(await ethers.provider.getBalance(deployer.address)), "DUSK\n");

  // Step 1: Deploy Mock Tokens (for testnet)
  console.log("📝 Step 1: Deploying Mock Tokens...");

  const MockDUSK = await ethers.getContractFactory("MockDUSK");
  const mockDUSK = await MockDUSK.deploy();
  await mockDUSK.waitForDeployment();
  const duskAddress = await mockDUSK.getAddress();
  console.log("✅ MockDUSK deployed to:", duskAddress);

  const MockUSDT = await ethers.getContractFactory("MockUSDT");
  const mockUSDT = await MockUSDT.deploy();
  await mockUSDT.waitForDeployment();
  const usdtAddress = await mockUSDT.getAddress();
  console.log("✅ MockUSDT deployed to:", usdtAddress);

  // Step 2: Deploy Lending Pool
  console.log("\n📝 Step 2: Deploying Lending Pool...");

  // Initial DUSK price: $0.50 (with 8 decimals like Chainlink)
  const initialDuskPrice = 50000000; // $0.50 with 8 decimals

  // Treasury address (using deployer for now, can be changed later)
  const treasuryAddress = deployer.address;

  const DuskLendingPool = await ethers.getContractFactory("DuskLendingPool");
  const lendingPool = await DuskLendingPool.deploy(
    duskAddress,
    usdtAddress,
    initialDuskPrice,
    treasuryAddress
  );
  await lendingPool.waitForDeployment();
  const poolAddress = await lendingPool.getAddress();
  console.log("✅ DuskLendingPool deployed to:", poolAddress);
  console.log("✅ Treasury set to:", treasuryAddress);

  // Step 3: Initialize the pool with USDT liquidity
  console.log("\n📝 Step 3: Initializing Pool with Liquidity...");

  const initialLiquidity = ethers.parseUnits("100000", 6); // 100k USDT
  await mockUSDT.approve(poolAddress, initialLiquidity);
  await lendingPool.supplyUsdt(initialLiquidity);
  console.log("✅ Supplied 100,000 USDT to the pool");

  // Step 4: Display contract information
  console.log("\n" + "=".repeat(60));
  console.log("📋 DEPLOYMENT SUMMARY");
  console.log("=".repeat(60));
  console.log("Network:", hre.network.name);
  console.log("Deployer:", deployer.address);
  console.log("\nContract Addresses:");
  console.log("  MockDUSK:", duskAddress);
  console.log("  MockUSDT:", usdtAddress);
  console.log("  DuskLendingPool:", poolAddress);
  console.log("  Treasury:", treasuryAddress);
  console.log("\nPool Configuration:");
  console.log("  Initial DUSK Price: $0.50");
  console.log("  Collateralization Ratio: 150%");
  console.log("  Liquidation Threshold: 125%");
  console.log("  Borrow APR: 8% (borrowers pay)");
  console.log("  Supply APR: 5% (lenders earn)");
  console.log("  Protocol Spread: 3% (to treasury)");
  console.log("  Initial USDT Liquidity: 100,000 USDT");
  console.log("=".repeat(60));

  // Save deployment addresses
  console.log("\n📝 Saving deployment addresses...");
  const fs = require("fs");
  const deploymentInfo = {
    network: hre.network.name,
    deployer: deployer.address,
    timestamp: new Date().toISOString(),
    contracts: {
      MockDUSK: duskAddress,
      MockUSDT: usdtAddress,
      DuskLendingPool: poolAddress,
      Treasury: treasuryAddress,
    },
    configuration: {
      initialDuskPrice: "$0.50",
      collateralizationRatio: "150%",
      liquidationThreshold: "125%",
      borrowAPR: "8%",
      supplyAPR: "5%",
      protocolSpread: "3%",
    },
  };

  const deploymentPath = `./deployments/${hre.network.name}.json`;
  if (!fs.existsSync("./deployments")) {
    fs.mkdirSync("./deployments");
  }
  fs.writeFileSync(deploymentPath, JSON.stringify(deploymentInfo, null, 2));
  console.log(`✅ Deployment info saved to: ${deploymentPath}`);

  console.log("\n✅ Deployment completed successfully!");
  console.log("\n📖 Next steps:");
  console.log("  1. Get test tokens from faucet:");
  console.log(`     - MockDUSK.faucet() - Get 1000 DUSK`);
  console.log(`     - MockUSDT.faucet() - Get 10000 USDT`);
  console.log("  2. Deposit DUSK as collateral");
  console.log("  3. Borrow USDT against your DUSK");
  console.log("\n🔗 Interact with the contracts:");
  console.log(`  DuskLendingPool: ${poolAddress}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
