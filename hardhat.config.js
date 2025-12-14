require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    hardhat: {
      chainId: 31337,
    },
    "dusk-testnet": {
      url: process.env.DUSK_TESTNET_RPC_URL || "https://rpc.dusk.network/testnet",
      accounts: process.env.PRIVATE_KEY !== undefined ? [process.env.PRIVATE_KEY] : [],
      chainId: 476, // Dusk testnet chain ID (placeholder - verify actual chain ID)
      gasPrice: "auto",
    },
    "dusk-mainnet": {
      url: process.env.DUSK_MAINNET_RPC_URL || "https://rpc.dusk.network",
      accounts: process.env.PRIVATE_KEY !== undefined ? [process.env.PRIVATE_KEY] : [],
      chainId: 477, // Dusk mainnet chain ID (placeholder - verify actual chain ID)
      gasPrice: "auto",
    },
  },
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts",
  },
  mocha: {
    timeout: 40000,
  },
};
