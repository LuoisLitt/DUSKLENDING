# 🌐 Deploy to dusklend.io - Complete Guide

This guide will help you publish your DUSK Lending Platform to **dusklend.io** using your GoDaddy domain.

## 🎯 Best Option: Vercel (Recommended)

Vercel is the easiest and fastest way to deploy your site with a custom domain.

### Step 1: Deploy to Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```
   Follow the prompts to authenticate.

3. **Deploy the website:**
   ```bash
   cd /home/user/DUSKLENDING/web
   vercel --prod
   ```

4. **Answer the prompts:**
   ```
   ? Set up and deploy "~/DUSKLENDING/web"? [Y/n] y
   ? Which scope do you want to deploy to? [Your Account]
   ? Link to existing project? [y/N] n
   ? What's your project's name? dusk-lending
   ? In which directory is your code located? ./
   ? Want to override the settings? [y/N] n
   ```

5. **Note the deployment URL** (e.g., `dusk-lending.vercel.app`)

### Step 2: Add Custom Domain in Vercel

1. **Go to Vercel Dashboard:**
   - Visit: https://vercel.com/dashboard
   - Select your project `dusk-lending`

2. **Add domain:**
   - Click **Settings** → **Domains**
   - Enter: `dusklend.io`
   - Click **Add**
   - Also add: `www.dusklend.io`

3. **Vercel will show you DNS records to configure**

### Step 3: Configure GoDaddy DNS

1. **Login to GoDaddy:**
   - Go to: https://dcc.godaddy.com/
   - Navigate to **My Products** → **DNS**

2. **Update DNS records:**

   **For Root Domain (dusklend.io):**
   - Type: `A`
   - Name: `@`
   - Value: `76.76.21.21` (Vercel's IP)
   - TTL: `600 seconds`

   **For WWW subdomain:**
   - Type: `CNAME`
   - Name: `www`
   - Value: `cname.vercel-dns.com`
   - TTL: `600 seconds`

   **Delete any existing A or CNAME records** for @ and www first!

3. **Save changes** (may take up to 48 hours, usually <30 minutes)

### Step 4: Verify in Vercel

1. Return to Vercel Dashboard
2. Domain status should show "Valid Configuration"
3. SSL certificate will be automatically provisioned

### Step 5: Update Your Code (Optional)

Update `web/js/config.js` to use testnet by default:
```javascript
let CURRENT_NETWORK = 'duskTestnet'; // Change from 'hardhat'
```

Then redeploy:
```bash
cd web
vercel --prod
```

---

## 🔷 Alternative Option: Netlify

### Step 1: Deploy to Netlify

1. **Install Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   ```

2. **Login:**
   ```bash
   netlify login
   ```

3. **Deploy:**
   ```bash
   cd /home/user/DUSKLENDING/web
   netlify deploy --prod
   ```

4. **Follow prompts:**
   ```
   ? Create & configure a new site? Yes
   ? Team: [Your Team]
   ? Site name: dusk-lending
   ? Publish directory: .
   ```

5. **Note your site URL** (e.g., `dusk-lending.netlify.app`)

### Step 2: Add Custom Domain in Netlify

1. **Go to Netlify Dashboard:**
   - Visit: https://app.netlify.com/
   - Select your site

2. **Add domain:**
   - Click **Domain Settings** → **Add custom domain**
   - Enter: `dusklend.io`
   - Click **Verify** → **Add domain**

3. **Netlify will show DNS configuration needed**

### Step 3: Configure GoDaddy DNS for Netlify

1. **In GoDaddy DNS settings, add:**

   **For Root Domain:**
   - Type: `A`
   - Name: `@`
   - Value: `75.2.60.5` (Netlify's load balancer IP)
   - TTL: `600 seconds`

   **For WWW:**
   - Type: `CNAME`
   - Name: `www`
   - Value: `dusk-lending.netlify.app` (your Netlify URL)
   - TTL: `600 seconds`

2. **Save and wait for DNS propagation**

---

## 🟦 Option 3: GitHub Pages

### Step 1: Enable GitHub Pages

1. **Push your code to GitHub** (already done!)

2. **Go to GitHub repository settings:**
   - Navigate to: `https://github.com/LuoisLitt/DUSKLENDING/settings/pages`

3. **Configure Pages:**
   - Source: `Deploy from a branch`
   - Branch: `claude/dusk-lending-platform-XP99i`
   - Folder: `/web`
   - Click **Save**

4. **Wait for deployment** (~2 minutes)

5. **Your site will be at:**
   `https://luoislitt.github.io/DUSKLENDING/`

### Step 2: Add Custom Domain in GitHub

1. **In Pages settings:**
   - Custom domain: `dusklend.io`
   - Click **Save**

2. **Check "Enforce HTTPS"** (after DNS propagates)

### Step 3: Configure GoDaddy DNS for GitHub Pages

1. **In GoDaddy DNS, add these records:**

   **Delete any existing A records for @**

   **Add 4 A records for root domain:**
   - Type: `A`, Name: `@`, Value: `185.199.108.153`
   - Type: `A`, Name: `@`, Value: `185.199.109.153`
   - Type: `A`, Name: `@`, Value: `185.199.110.153`
   - Type: `A`, Name: `@`, Value: `185.199.111.153`

   **For WWW:**
   - Type: `CNAME`, Name: `www`, Value: `luoislitt.github.io`

2. **Save and wait for propagation**

---

## 🚀 Quick Start (Recommended: Vercel)

Here's the fastest way to get live:

```bash
# 1. Install Vercel
npm install -g vercel

# 2. Deploy
cd /home/user/DUSKLENDING/web
vercel login
vercel --prod

# 3. Add domain in Vercel dashboard
# Visit: https://vercel.com/dashboard
# Settings → Domains → Add dusklend.io

# 4. Configure GoDaddy DNS
# A record: @ → 76.76.21.21
# CNAME: www → cname.vercel-dns.com

# Done! Wait 5-30 minutes for DNS propagation
```

---

## 🔍 Verify DNS Propagation

Check if DNS changes have propagated:

```bash
# Check A record
dig dusklend.io +short

# Check CNAME
dig www.dusklend.io +short

# Or use online tool:
# https://www.whatsmydns.net/#A/dusklend.io
```

---

## ⚙️ Before Going Live

### 1. Deploy Contracts to DuskEVM Testnet

You need testnet DUSK first!

```bash
# Get testnet DUSK from Discord faucet
# !dusk YOUR_ADDRESS

# Then deploy
npx hardhat run scripts/deploy.js --network dusk-testnet

# Update web config
HARDHAT_NETWORK=dusk-testnet node scripts/update-web-config.js
```

### 2. Update Default Network

Edit `web/js/config.js`:
```javascript
// Change this line:
let CURRENT_NETWORK = 'duskTestnet'; // was 'hardhat'
```

### 3. Test Locally First

```bash
cd web
npx http-server -p 8080 -c-1
# Test at http://localhost:8080
```

### 4. Commit and Redeploy

```bash
git add web/js/config.js
git commit -m "Update to use DuskEVM testnet"
git push

# Then redeploy to Vercel/Netlify
vercel --prod
# or
netlify deploy --prod
```

---

## 📊 Deployment Comparison

| Feature | Vercel | Netlify | GitHub Pages |
|---------|--------|---------|--------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Speed** | Very Fast | Very Fast | Fast |
| **SSL** | Auto (Free) | Auto (Free) | Auto (Free) |
| **Custom Domain** | Easy | Easy | Moderate |
| **Build Time** | Instant | Instant | 2-5 min |
| **Analytics** | Built-in | Built-in | No |
| **CDN** | Global | Global | Global |
| **Price** | Free | Free | Free |
| **Recommended** | ✅ Yes | ✅ Yes | ⚠️ Ok |

**Recommendation:** Use **Vercel** for the best experience.

---

## 🎨 Optional Enhancements

### Add Favicon

Create `web/favicon.ico` and add to `index.html`:
```html
<link rel="icon" href="favicon.ico">
```

### Add Meta Tags for SEO

Add to `web/index.html` `<head>`:
```html
<meta name="description" content="DUSK Lending Platform - Deposit DUSK, Borrow USDT">
<meta property="og:title" content="DUSK Lending Platform">
<meta property="og:description" content="Decentralized lending on DUSK Network">
<meta property="og:url" content="https://dusklend.io">
<meta name="twitter:card" content="summary_large_image">
```

### Add Google Analytics (Optional)

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## 🐛 Troubleshooting

### "DNS_PROBE_FINISHED_NXDOMAIN"
→ DNS not propagated yet, wait 30 minutes

### "NET::ERR_CERT_COMMON_NAME_INVALID"
→ SSL not ready, wait for auto-provisioning (15 minutes)

### Site shows old content
→ Clear browser cache (Ctrl+Shift+R)

### "This site can't be reached"
→ Check DNS records in GoDaddy
→ Use DNS checker: whatsmydns.net

### Vercel shows "Invalid Configuration"
→ Double-check A and CNAME records
→ Remove conflicting DNS records

---

## ✅ Final Checklist

- [ ] Vercel/Netlify account created
- [ ] Website deployed to hosting
- [ ] Custom domain added in hosting dashboard
- [ ] GoDaddy DNS configured (A + CNAME records)
- [ ] Old DNS records removed
- [ ] DNS propagation verified
- [ ] SSL certificate active (https://)
- [ ] Contracts deployed to DuskEVM testnet
- [ ] Web config updated with testnet addresses
- [ ] Default network set to 'duskTestnet'
- [ ] Tested on desktop and mobile
- [ ] MetaMask connection works
- [ ] All transactions work on testnet

---

## 🎉 You're Live!

Once DNS propagates (5-30 minutes), your site will be live at:

**https://dusklend.io** 🚀

Share it with the world!

---

## 📞 Support

- **Vercel Docs:** https://vercel.com/docs
- **Netlify Docs:** https://docs.netlify.com/
- **GoDaddy DNS:** https://www.godaddy.com/help/dns-management-19228
- **DUSK Discord:** https://discord.gg/dusk

---

**Need help? The deployment process is straightforward - just follow the Vercel steps above!**
