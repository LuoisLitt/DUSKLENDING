# ⚡ Quick Deploy to dusklend.io

## 🚀 Deploy in 3 Commands

```bash
# 1. Run the deploy script
./scripts/deploy-to-vercel.sh

# 2. Add domain in Vercel (visit dashboard)
https://vercel.com/dashboard

# 3. Configure GoDaddy DNS
A record: @ → 76.76.21.21
CNAME: www → cname.vercel-dns.com
```

**That's it!** Wait 30 minutes for DNS propagation.

---

## 📋 Detailed Steps

### Step 1: Deploy to Vercel

```bash
cd /home/user/DUSKLENDING
./scripts/deploy-to-vercel.sh
```

Or manually:
```bash
npm install -g vercel
cd web
vercel login
vercel --prod
```

### Step 2: Add Custom Domain

1. Visit https://vercel.com/dashboard
2. Select your project
3. Go to **Settings** → **Domains**
4. Add `dusklend.io`
5. Add `www.dusklend.io`

Vercel will show DNS configuration needed.

### Step 3: Configure GoDaddy

1. Login to GoDaddy: https://dcc.godaddy.com/
2. Go to **My Products** → **DNS**
3. **Delete any existing A or CNAME records for @ and www**
4. Add these records:

**A Record (Root Domain):**
```
Type: A
Name: @
Value: 76.76.21.21
TTL: 600 seconds
```

**CNAME Record (WWW):**
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
TTL: 600 seconds
```

5. Save changes

### Step 4: Wait

DNS propagation takes 5-30 minutes (sometimes up to 48 hours).

Check status: https://www.whatsmydns.net/#A/dusklend.io

### Step 5: Verify

Visit **https://dusklend.io** - your site should be live! 🎉

---

## ✅ Before You Deploy

### Option A: Deploy with Local Contracts (Testing)

Your site will work with Hardhat local network:
- Users need to add Hardhat network to MetaMask
- Good for testing before testnet

```bash
./scripts/deploy-to-vercel.sh
```

### Option B: Deploy with DuskEVM Testnet (Production-Ready)

**Recommended for public use:**

1. **Get testnet DUSK:**
   - Join Discord: https://discord.gg/dusk
   - Use faucet: `!dusk YOUR_ADDRESS`

2. **Deploy contracts to testnet:**
   ```bash
   npx hardhat run scripts/deploy.js --network dusk-testnet
   ```

3. **Update web config:**
   ```bash
   HARDHAT_NETWORK=dusk-testnet node scripts/update-web-config.js
   ```

4. **Set default network to testnet:**
   Edit `web/js/config.js`:
   ```javascript
   let CURRENT_NETWORK = 'duskTestnet'; // Change from 'hardhat'
   ```

5. **Commit changes:**
   ```bash
   git add web/js/config.js
   git commit -m "Configure for DuskEVM testnet"
   git push
   ```

6. **Deploy:**
   ```bash
   ./scripts/deploy-to-vercel.sh
   ```

---

## 🔧 Troubleshooting

**Site not loading?**
→ Wait for DNS propagation (up to 48 hours)

**"Invalid Configuration" in Vercel?**
→ Check GoDaddy DNS settings match exactly

**SSL certificate error?**
→ Wait 15 minutes for auto-provisioning

**Need help?**
→ See full guide: `DEPLOY_TO_DUSKLEND_IO.md`

---

## 📞 Quick Links

- **Vercel Dashboard:** https://vercel.com/dashboard
- **GoDaddy DNS:** https://dcc.godaddy.com/
- **DNS Checker:** https://www.whatsmydns.net/
- **Full Deploy Guide:** [DEPLOY_TO_DUSKLEND_IO.md](./DEPLOY_TO_DUSKLEND_IO.md)

---

**Your site will be live at: https://dusklend.io** 🌐
