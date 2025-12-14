# Get Testnet DUSK Tokens

## Your Wallet Address
```
0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
```

## Current Status
- ✅ RPC Endpoint: https://rpc.testnet.evm.dusk.network
- ✅ Chain ID: 745
- ✅ Network: DuskEVM Testnet
- ❌ Balance: 0 DUSK (need tokens to deploy)

## How to Get Testnet DUSK

### Option 1: DUSK Discord Faucet (Recommended)

1. **Join DUSK Discord**: https://discord.gg/dusk

2. **Navigate to faucet channel** (usually #faucet or #testnet-faucet)

3. **Request tokens** with command:
   ```
   !dusk 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
   ```

4. **Wait for confirmation** - tokens should arrive in a few minutes

### Option 2: Use Your Own Wallet

If you prefer to use your own MetaMask wallet instead of the test wallet:

1. **Add DuskEVM Testnet to MetaMask:**
   - Network Name: `DuskEVM Testnet`
   - RPC URL: `https://rpc.testnet.evm.dusk.network`
   - Chain ID: `745`
   - Currency Symbol: `DUSK`
   - Block Explorer: (if available)

2. **Get your private key** from MetaMask:
   - Click account menu → Account details → Export private key
   - **⚠️ Keep this secure! Never share it!**

3. **Update .env file:**
   ```bash
   PRIVATE_KEY=your_actual_private_key_here
   ```

4. **Request faucet** with your address:
   ```
   !dusk YOUR_METAMASK_ADDRESS
   ```

### Option 3: Web Wallet

Visit DUSK Web Wallet and bridge tokens:
- https://wallet.dusk.network (if available)

## Verify Balance

After receiving tokens, verify with:

```bash
# Using curl
curl -s -X POST https://rpc.testnet.evm.dusk.network \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_getBalance","params":["0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266","latest"],"id":1}'

# Or check in Hardhat console
npx hardhat console --network dusk-testnet
> const balance = await ethers.provider.getBalance("0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266")
> ethers.formatEther(balance)
```

## How Much DUSK Do You Need?

Estimated deployment costs:
- MockDUSK: ~0.003 DUSK
- MockUSDT: ~0.003 DUSK
- DuskLendingPool: ~0.007 DUSK
- **Total: ~0.015 DUSK** (request at least 1 DUSK for safety)

## Once You Have DUSK

Deploy the contracts:

```bash
npx hardhat run scripts/deploy.js --network dusk-testnet
```

## Troubleshooting

### "Insufficient funds" error
- Request more DUSK from faucet
- Faucets usually have daily limits

### "Nonce too high" error
- Reset account in MetaMask
- Or wait a few minutes and try again

### Can't connect to Discord
- Try the official DUSK website for alternative faucet links
- Check DUSK documentation for testnet resources

## Resources

- DUSK Discord: https://discord.gg/dusk
- DUSK Documentation: https://docs.dusk.network/
- DuskEVM Info: https://dusk.network/news/multilayer-evolution
