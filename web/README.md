# 🌐 DUSK Lending Platform - Web Interface

A beautiful, user-friendly web interface for the DUSK Lending Platform.

## ✨ Features

- 💳 **MetaMask Integration** - Connect your wallet with one click
- 📊 **Real-time Stats** - Live pool statistics and your position
- 💰 **All Operations** - Deposit, Borrow, Repay, Withdraw, Supply
- 🎨 **Beautiful UI** - Modern, responsive design
- 🔔 **Transaction Feedback** - Clear success/error messages
- 📱 **Mobile Friendly** - Works on all devices
- ⚡ **Fast** - No backend needed, direct blockchain interaction

## 🚀 Quick Start

### 1. Deploy Contracts

```bash
# Start Hardhat node
npx hardhat node

# In another terminal, deploy contracts
npx hardhat run scripts/deploy.js --network localhost
```

### 2. Update Web Config

```bash
HARDHAT_NETWORK=localhost node scripts/update-web-config.js
```

### 3. Start Web Server

```bash
npx http-server web -p 8080 -c-1
```

### 4. Open in Browser

Navigate to: **http://localhost:8080**

### 5. Configure MetaMask

Add Hardhat Network to MetaMask:
- Network Name: `Hardhat Local`
- RPC URL: `http://localhost:8545`
- Chain ID: `31337`
- Currency Symbol: `ETH`

Import test account:
- Private Key: `0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80`

## 📖 How to Use

### Connect Wallet

1. Click "Connect Wallet" button
2. Approve MetaMask connection
3. Your address and balances will appear

### Get Test Tokens

1. Click "Get Tokens" button
2. Receive 1,000 DUSK and 10,000 USDT
3. Balances update automatically

### Deposit DUSK as Collateral

1. Enter amount in "Deposit DUSK" card
2. Click "Deposit" button
3. Approve transaction in MetaMask
4. Wait for confirmation

### Borrow USDT

1. Check "Max Borrow" in your position
2. Enter amount in "Borrow USDT" card
3. Click "Borrow" button
4. Approve transaction
5. USDT appears in your wallet

### Repay USDT Loan

1. Enter amount in "Repay USDT" card
2. Click "Repay" button
3. Approve USDT spending (first time)
4. Confirm repayment transaction

### Withdraw DUSK

1. Repay all debt first (or maintain healthy position)
2. Enter amount in "Withdraw DUSK" card
3. Click "Withdraw" button
4. DUSK returns to your wallet

## 🎯 Understanding the Interface

### Pool Statistics

- **DUSK Price** - Current price ($0.50 default)
- **Total USDT Liquidity** - Total USDT in pool
- **Available to Borrow** - USDT available for borrowing
- **Borrow APR** - Annual interest rate (5%)

### Your Position

- **DUSK Collateral** - Your deposited DUSK
- **USDT Borrowed** - Total USDT you borrowed
- **Health Factor** - Position safety indicator
  - ∞ (infinity) = No debt, perfectly safe
  - > 1.5 = Safe (green)
  - 1.2-1.5 = Warning (orange)
  - < 1.2 = Danger (red)
- **Max Borrow** - Maximum USDT you can borrow

## 🔐 Security

### Built-in Safety

- ✅ All transactions require MetaMask approval
- ✅ No private keys stored or transmitted
- ✅ Direct blockchain interaction (no backend)
- ✅ Open source code
- ✅ Health factor warnings

### Best Practices

1. **Test with small amounts first**
2. **Monitor health factor** - keep above 1.5
3. **Don't borrow maximum** - leave safety margin
4. **Repay before withdrawing**
5. **Use testnet only** - not for real assets

## 🛠 Technical Details

### Technology Stack

- **HTML5** - Structure
- **CSS3** - Styling with gradients and animations
- **JavaScript (ES6+)** - Logic and interaction
- **Ethers.js v5** - Ethereum/EVM interaction
- **MetaMask** - Wallet connection

### Contract Interaction

All operations call smart contract functions directly:
- `depositDusk()` - Deposit DUSK as collateral
- `withdrawDusk()` - Withdraw DUSK collateral
- `borrowUsdt()` - Borrow USDT
- `repayUsdt()` - Repay USDT loan
- `supplyUsdt()` - Supply USDT to pool

### Network Support

- ✅ Hardhat Local (Chain ID: 31337)
- ✅ DuskEVM Testnet (Chain ID: 745)
- Auto-detects current network

## 📁 File Structure

```
web/
├── index.html          # Main HTML file
├── css/
│   └── style.css       # Styles and animations
├── js/
│   ├── config.js       # Network and contract config
│   └── app.js          # Main application logic
└── README.md           # This file
```

## 🎨 Customization

### Change Colors

Edit `css/style.css`:
```css
background: linear-gradient(135deg, #YOUR_COLOR 0%, #YOUR_COLOR 100%);
```

### Update Branding

Edit `index.html`:
```html
<h1>🌙 Your Platform Name</h1>
```

### Add Features

Edit `js/app.js` to add:
- Transaction history
- Price charts
- Liquidation bot
- Notifications
- Analytics

## 🐛 Troubleshooting

### "Please install MetaMask"
→ Install [MetaMask browser extension](https://metamask.io/)

### "Unsupported network"
→ Switch MetaMask to Hardhat (31337) or DuskEVM Testnet (745)

### "Contract not deployed"
→ Deploy contracts first:
```bash
npx hardhat run scripts/deploy.js --network localhost
```

### Balances not updating
→ Refresh page or reconnect wallet

### Transaction fails
→ Check:
- Sufficient balance
- Correct approvals
- Valid amounts
- Network gas

## 🌐 Deploy to Production

See [WEB_HOSTING.md](../WEB_HOSTING.md) for full instructions.

**Quick Deploy to GitHub Pages:**
```bash
# Update config for testnet
HARDHAT_NETWORK=dusk-testnet node scripts/update-web-config.js

# Push to GitHub
git add web/
git commit -m "Add web interface"
git push

# Enable Pages in repo settings
```

## 📊 Performance

- **Load Time**: < 1 second
- **No Backend**: Direct blockchain calls
- **Lightweight**: ~50KB total
- **No Dependencies**: Only ethers.js CDN

## 🎯 Roadmap

Future enhancements:
- [ ] Transaction history
- [ ] Price charts
- [ ] Multiple collateral types
- [ ] Liquidation notifications
- [ ] Dark mode toggle
- [ ] Multi-language support
- [ ] Mobile app (React Native)

## 📚 Learn More

- [Ethers.js Documentation](https://docs.ethers.org/)
- [MetaMask Documentation](https://docs.metamask.io/)
- [DUSK Network](https://dusk.network/)
- [AAVE v3 Protocol](https://docs.aave.com/)

## 🤝 Contributing

Contributions welcome! Ideas:
- UI/UX improvements
- Additional features
- Bug fixes
- Documentation
- Translations

## 📄 License

MIT License - Same as parent project

---

**Built with ❤️ for the DUSK Network ecosystem**
