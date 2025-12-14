# DUSK Network Deployment Guide

## Current Status

✅ **Smart contracts are ready**
✅ **Hardhat configuration updated**
✅ **All tests passing (20/20)**
⏳ **Waiting for DuskEVM RPC endpoint**

## Network Information Found

From [DUSK Documentation](https://docs.dusk.network/operator/networks/):

### Nocturne Testnet (DuskDS)
- **Chain ID:** 2
- **Endpoint:** https://nodes.testnet.dusk.network
- **Type:** GraphQL/Custom RPC (not standard EVM JSON-RPC)
- **Faucet:** Discord command `!dusk`

### DuskEVM Testnet
- **Status:** Launched December 5, 2025
- **Type:** EVM-compatible (Solidity contracts)
- **RPC Endpoint:** Not yet publicly documented
- **Chain ID:** TBD

## How to Get DuskEVM RPC Endpoint

Since DuskEVM testnet just launched, you need to get the official endpoint from:

### Option 1: DUSK Discord (Recommended)
1. Join DUSK Discord: https://discord.gg/dusk
2. Check #announcements or #developer channels
3. Ask in #dev-support: "What is the DuskEVM testnet RPC endpoint?"
4. Request testnet DUSK tokens with: `!dusk YOUR_ADDRESS`

### Option 2: Official Documentation
Visit [https://docs.dusk.network/developer/](https://docs.dusk.network/developer/) and look for:
- DuskEVM deployment guides
- Network configuration
- MetaMask setup instructions

### Option 3: GitHub
Check [dusk-network repositories](https://github.com/dusk-network) for:
- Recent DuskEVM announcements
- Example configurations
- Deployment scripts

## Once You Have the RPC Endpoint

### Step 1: Update hardhat.config.js

Update the RPC URL and chain ID in `hardhat.config.js`:

```javascript
"dusk-testnet": {
  url: "YOUR_DUSKEVM_RPC_URL_HERE",  // e.g., https://rpc.duskevm.testnet.dusk.network
  accounts: process.env.PRIVATE_KEY !== undefined ? [process.env.PRIVATE_KEY] : [],
  chainId: YOUR_CHAIN_ID_HERE,  // e.g., 476, 1002, etc.
  gasPrice: "auto",
},
```

### Step 2: Get a Wallet with DUSK

**Create a new wallet:**
```bash
# Generate a new private key (use MetaMask or ethers.js)
npx hardhat console
> const wallet = ethers.Wallet.createRandom()
> console.log("Address:", wallet.address)
> console.log("Private Key:", wallet.privateKey)
```

**Update .env:**
```bash
PRIVATE_KEY=your_actual_private_key_here
```

**Get testnet DUSK:**
1. Copy your wallet address
2. Go to DUSK Discord
3. Use faucet: `!dusk YOUR_ADDRESS`

### Step 3: Test Connection

```bash
npx hardhat run scripts/test-connection.js --network dusk-testnet
```

Expected output:
```
✅ Connected to network:
   Chain ID: XXX
   Name: DuskEVM Testnet
✅ Latest block: XXXXX
💰 Balance: X.XX DUSK
```

### Step 4: Deploy!

```bash
npx hardhat run scripts/deploy.js --network dusk-testnet
```

## Alternative: Deploy to a Local DUSK Node

If you want to run your own node:

1. **Install DUSK node** following [operator docs](https://docs.dusk.network/operator/)
2. **Enable RPC access** (port 8080)
3. **Update hardhat.config.js:**
   ```javascript
   "dusk-local": {
     url: "http://localhost:8080",
     accounts: [process.env.PRIVATE_KEY],
     chainId: 2,
   }
   ```
4. **Deploy:**
   ```bash
   npx hardhat run scripts/deploy.js --network dusk-local
   ```

## Current Configuration

Your project is configured with:
- ✅ Solidity 0.8.20 (OpenZeppelin v5 compatible)
- ✅ OpenZeppelin contracts for security
- ✅ Mock DUSK and USDT tokens for testing
- ✅ DuskLendingPool contract (AAVE v3 based)
- ✅ Comprehensive test suite
- ✅ Deployment scripts
- ✅ .env file ready (update PRIVATE_KEY)

## Expected Deployment Cost

Approximate gas costs:
- MockDUSK: ~1,500,000 gas
- MockUSDT: ~1,500,000 gas
- DuskLendingPool: ~3,500,000 gas
- **Total: ~6,500,000 gas**

At gas price of 1 gwei: ~0.0065 DUSK

## Troubleshooting

### "Internal JSON-RPC error"
- Wrong RPC endpoint format
- Endpoint not accessible
- Incorrect chain ID

### "Insufficient funds"
- Need testnet DUSK from faucet
- Check balance: `npx hardhat run scripts/test-connection.js`

### "Contract too large"
- Enable optimizer in hardhat.config.js (already done)
- Use `viaIR: true` if needed

## Resources

- [DUSK Network](https://dusk.network/)
- [DUSK Documentation](https://docs.dusk.network/)
- [DUSK GitHub](https://github.com/dusk-network)
- [DuskEVM Announcement](https://mpost.io/privacy-focused-blockchain-dusk-launches-duskevm-testnet-allowing-devs-to-explore-and-test/)
- [Discord Community](https://discord.gg/dusk)

## Next Steps

1. ✅ Join DUSK Discord
2. ✅ Get DuskEVM RPC endpoint and chain ID
3. ✅ Update `hardhat.config.js`
4. ✅ Get testnet DUSK from faucet
5. ✅ Run test-connection.js
6. ✅ Deploy to testnet
7. ✅ Verify contracts work
8. ✅ Create pull request or document deployment

---

**Note:** This guide will be updated once official DuskEVM testnet endpoints are published.
