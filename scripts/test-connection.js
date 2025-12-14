const hre = require("hardhat");
const ethers = hre.ethers;

async function main() {
  console.log("🔍 Testing DUSK Testnet Connection...\n");

  try {
    // Get the network config
    const networkConfig = hre.config.networks["dusk-testnet"];
    const rpcUrl = networkConfig.url;

    // Get provider
    const provider = new ethers.JsonRpcProvider(rpcUrl);

    console.log("📡 RPC Endpoint:", rpcUrl);

    // Try to get network info
    console.log("📝 Fetching network information...");
    const network = await provider.getNetwork();
    console.log("✅ Connected to network:");
    console.log("   Chain ID:", network.chainId.toString());
    console.log("   Name:", network.name);

    // Try to get block number
    console.log("\n📝 Fetching latest block...");
    const blockNumber = await provider.getBlockNumber();
    console.log("✅ Latest block:", blockNumber);

    // Get test account address
    const [signer] = await ethers.getSigners();
    const address = await signer.getAddress();
    console.log("\n👛 Deployer address:", address);

    // Check balance
    console.log("📝 Checking balance...");
    const balance = await provider.getBalance(address);
    console.log("💰 Balance:", ethers.formatEther(balance), "DUSK");

    if (balance === 0n) {
      console.log("\n⚠️  WARNING: No DUSK tokens in wallet!");
      console.log("📖 To get testnet DUSK:");
      console.log("   1. Join DUSK Discord: https://discord.gg/dusk");
      console.log("   2. Use faucet command: !dusk " + address);
      console.log("   3. Wait for tokens to arrive");
    } else {
      console.log("\n✅ Wallet has DUSK! Ready to deploy.");
    }

  } catch (error) {
    console.error("\n❌ Error connecting to DUSK testnet:");
    console.error(error.message);

    if (error.message.includes("could not detect network")) {
      console.log("\n💡 This might not be an EVM-compatible endpoint.");
      console.log("   DUSK may use a different RPC format (GraphQL or custom).");
    }
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
