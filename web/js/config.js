// Network Configuration
const NETWORKS = {
    hardhat: {
        chainId: 31337,
        name: "Hardhat Local",
        rpcUrl: "http://localhost:8545",
        explorer: null
    },
    duskTestnet: {
        chainId: 745,
        name: "DuskEVM Testnet",
        rpcUrl: "https://rpc.testnet.evm.dusk.network",
        explorer: null // Add when available
    }
};

// Contract Addresses (will be updated after deployment)
// These are placeholders - update after deploying to testnet
const CONTRACT_ADDRESSES = {
    hardhat: {
        MockDUSK: "0xA51c1fc2f0D1a1b8494Ed1FE312d7C3a78Ed91C0",
        MockUSDT: "0x0DCd1Bf9A1b36cE34237eEaFef220932846BCD82",
        DuskLendingPool: "0x9A676e781A523b5d0C0e43731313A708CB607508"
    },
    duskTestnet: {
        MockDUSK: "", // Update after deployment
        MockUSDT: "", // Update after deployment
        DuskLendingPool: "" // Update after deployment
    }
};

// Contract ABIs (simplified - only essential functions)
const DUSK_ABI = [
    "function balanceOf(address owner) view returns (uint256)",
    "function approve(address spender, uint256 amount) returns (bool)",
    "function faucet()",
    "function decimals() view returns (uint8)",
    "function transfer(address to, uint256 amount) returns (bool)"
];

const USDT_ABI = [
    "function balanceOf(address owner) view returns (uint256)",
    "function approve(address spender, uint256 amount) returns (bool)",
    "function faucet()",
    "function decimals() view returns (uint8)",
    "function transfer(address to, uint256 amount) returns (bool)"
];

const LENDING_POOL_ABI = [
    "function depositDusk(uint256 amount)",
    "function withdrawDusk(uint256 amount)",
    "function borrowUsdt(uint256 amount)",
    "function repayUsdt(uint256 amount)",
    "function supplyUsdt(uint256 amount)",
    "function liquidate(address borrower, uint256 usdtAmount)",
    "function users(address) view returns (uint256 duskCollateral, uint256 usdtBorrowed, uint256 lastUpdateTimestamp, uint256 accruedInterest)",
    "function getUserDebt(address user) view returns (uint256)",
    "function getHealthFactor(address user) view returns (uint256)",
    "function getMaxBorrowAmount(address user) view returns (uint256)",
    "function totalDuskDeposited() view returns (uint256)",
    "function totalUsdtLiquidity() view returns (uint256)",
    "function totalUsdtBorrowed() view returns (uint256)",
    "function duskPriceUSD() view returns (uint256)",
    "function borrowAPR() view returns (uint256)",
    "function supplyAPR() view returns (uint256)",
    "event DuskDeposited(address indexed user, uint256 amount)",
    "event DuskWithdrawn(address indexed user, uint256 amount)",
    "event UsdtBorrowed(address indexed user, uint256 amount)",
    "event UsdtRepaid(address indexed user, uint256 amount)",
    "event UsdtSupplied(address indexed supplier, uint256 amount)"
];

// Default to localhost for development, switch to testnet for production
let CURRENT_NETWORK = 'hardhat'; // Change to 'duskTestnet' for testnet

// Helper to get current network config
function getNetworkConfig() {
    return NETWORKS[CURRENT_NETWORK];
}

// Helper to get current contract addresses
function getContractAddresses() {
    return CONTRACT_ADDRESSES[CURRENT_NETWORK];
}
