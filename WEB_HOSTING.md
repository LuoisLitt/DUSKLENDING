# Web Interface Hosting Guide

## Overview

Your DUSK Lending Platform now has a beautiful web interface that users can access through their browser!

## 🚀 Quick Start (Local Testing)

### Option 1: Using Node.js HTTP Server (Recommended)

1. **Install http-server globally:**
   ```bash
   npm install -g http-server
   ```

2. **Start the server:**
   ```bash
   cd /home/user/DUSKLENDING
   npx http-server web -p 8080 -c-1
   ```

3. **Open in browser:**
   ```
   http://localhost:8080
   ```

### Option 2: Using Python

```bash
cd /home/user/DUSKLENDING/web
python3 -m http.server 8080
```

Then open: http://localhost:8080

### Option 3: Using PHP

```bash
cd /home/user/DUSKLENDING/web
php -S localhost:8080
```

## 📝 Before Testing

### 1. Deploy Contracts (if not done already)

**For local Hardhat testing:**
```bash
# Terminal 1: Start Hardhat node
npx hardhat node

# Terminal 2: Deploy contracts
npx hardhat run scripts/deploy.js --network localhost

# Terminal 3: Update web config
node scripts/update-web-config.js
```

**For DuskEVM Testnet:**
```bash
# Deploy to testnet
npx hardhat run scripts/deploy.js --network dusk-testnet

# Update web config
HARDHAT_NETWORK=dusk-testnet node scripts/update-web-config.js
```

### 2. Configure MetaMask

**For Hardhat Local Network:**
- Network Name: `Hardhat Local`
- RPC URL: `http://localhost:8545`
- Chain ID: `31337`
- Currency Symbol: `ETH`

**For DuskEVM Testnet:**
- Network Name: `DuskEVM Testnet`
- RPC URL: `https://rpc.testnet.evm.dusk.network`
- Chain ID: `745`
- Currency Symbol: `DUSK`

## 🌐 Deploy to GitHub Pages (Production)

### Step 1: Prepare Repository

1. **Ensure contracts are deployed to DuskEVM testnet**
2. **Update web config with testnet addresses:**
   ```bash
   HARDHAT_NETWORK=dusk-testnet node scripts/update-web-config.js
   ```

3. **Update `web/js/config.js` default network:**
   ```javascript
   let CURRENT_NETWORK = 'duskTestnet'; // Change from 'hardhat'
   ```

### Step 2: Push to GitHub

```bash
git add web/
git commit -m "Add web interface for DUSK Lending Platform"
git push origin claude/dusk-lending-platform-XP99i
```

### Step 3: Enable GitHub Pages

1. Go to repository Settings
2. Navigate to "Pages" section
3. Source: Select branch `claude/dusk-lending-platform-XP99i`
4. Folder: Select `/web`
5. Click "Save"

Your site will be live at:
```
https://LuoisLitt.github.io/DUSKLENDING/
```

(Adjust based on your GitHub username)

### Step 4: Update README

Add the live link to your README.md:
```markdown
## 🌐 Live Demo

Try the DUSK Lending Platform: [https://yourusername.github.io/DUSKLENDING/](https://yourusername.github.io/DUSKLENDING/)
```

## 🔧 Alternative Hosting Options

### Vercel

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Deploy:
   ```bash
   cd web
   vercel --prod
   ```

3. Follow prompts

### Netlify

1. Install Netlify CLI:
   ```bash
   npm install -g netlify-cli
   ```

2. Deploy:
   ```bash
   cd web
   netlify deploy --prod
   ```

### IPFS (Decentralized)

1. Install IPFS:
   ```bash
   npm install -g ipfs
   ```

2. Add site:
   ```bash
   ipfs add -r web/
   ```

3. Pin and share the hash

## 📱 Features of the Web Interface

### User Interface

- ✅ **Wallet Connection** - Connect MetaMask with one click
- ✅ **Real-time Balances** - See DUSK and USDT balances
- ✅ **Pool Statistics** - View total liquidity, available to borrow
- ✅ **Your Position** - Track collateral, debt, and health factor
- ✅ **Faucet Integration** - Get test tokens easily
- ✅ **All Actions** - Deposit, Borrow, Repay, Withdraw, Supply

### Visual Indicators

- **Health Factor Color Coding:**
  - 🟢 Green: > 1.5 (Safe)
  - 🟠 Orange: 1.2 - 1.5 (Warning)
  - 🔴 Red: < 1.2 (Danger)

- **Network Detection** - Auto-detects Hardhat or DuskEVM
- **Transaction Feedback** - Success/error messages
- **Responsive Design** - Works on mobile and desktop

## 🔒 Security Notes

### Important Warnings

1. **Never commit private keys** to git
2. **Use .gitignore** for sensitive files
3. **Testnet only** - Don't use real assets
4. **Audit before mainnet** - Get professional security audit

### Safe Practices

- Contract addresses are public (safe to commit)
- Frontend code is public (expected)
- Private keys stay in MetaMask (secure)
- Transactions require user approval

## 🐛 Troubleshooting

### "Please install MetaMask"
→ Install [MetaMask extension](https://metamask.io/)

### "Unsupported network"
→ Switch MetaMask to Hardhat (31337) or DuskEVM Testnet (745)

### "Contracts not deployed"
→ Run deployment script first:
```bash
npx hardhat run scripts/deploy.js --network dusk-testnet
```

### "Transaction failed"
→ Check:
- Sufficient gas (DUSK for testnet)
- Correct network
- Valid amounts
- Contract approvals

### CORS errors (local testing)
→ Use http-server with `-c-1` flag:
```bash
npx http-server web -p 8080 -c-1 --cors
```

## 📊 Testing Checklist

Before sharing with users:

- [ ] Deploy contracts to DuskEVM testnet
- [ ] Update web config with contract addresses
- [ ] Test wallet connection
- [ ] Test faucet function
- [ ] Test deposit DUSK
- [ ] Test borrow USDT
- [ ] Test repay USDT
- [ ] Test withdraw DUSK
- [ ] Verify health factor calculations
- [ ] Test on mobile device
- [ ] Test with different wallets
- [ ] Check all error messages

## 🎨 Customization

### Update Branding

Edit `web/index.html`:
```html
<h1>🌙 Your Project Name</h1>
```

### Change Colors

Edit `web/css/style.css`:
```css
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
```

### Add Features

Edit `web/js/app.js` to add:
- Price charts
- Transaction history
- Analytics
- Notifications
- More...

## 📚 Resources

- **MetaMask Guide**: https://metamask.io/faqs/
- **Ethers.js Docs**: https://docs.ethers.org/
- **Web3 Best Practices**: https://web3.university/
- **DUSK Docs**: https://docs.dusk.network/

## 🎉 You're Ready!

Your DUSK Lending Platform web interface is ready to use!

**Local testing:**
```bash
npx http-server web -p 8080 -c-1
```

**Share with others:**
Deploy to GitHub Pages or Vercel and share the link!

---

**Happy Testing! 🚀**
