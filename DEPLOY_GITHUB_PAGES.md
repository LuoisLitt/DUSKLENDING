# 🚀 Deploy to dusklend.io using GitHub Pages

This guide shows you how to deploy your DUSK Lending Platform to dusklend.io using GitHub Pages (no CLI login required!).

---

## ✅ Prerequisites Complete

- [x] Domain registered: **dusklend.io** (GoDaddy)
- [x] Code pushed to GitHub
- [x] CNAME file created in `/web` folder

---

## Step 1: Enable GitHub Pages

1. **Open your browser and go to your GitHub repository:**
   ```
   https://github.com/LuoisLitt/DUSKLENDING
   ```

2. **Click on "Settings"** (top menu, far right)

3. **In the left sidebar, scroll down and click "Pages"**

4. **Configure GitHub Pages:**

   **Source:**
   - Select: **Deploy from a branch**

   **Branch:**
   - Branch: **claude/dusk-lending-platform-XP99i**
   - Folder: **/(root)** or **/docs** (choose /(root) first)
   - Click **Save**

5. **Wait 1-2 minutes**
   - GitHub will start building your site
   - You'll see: "Your site is ready to be published at..."

6. **Important: Update the folder path**
   - Since our website is in the `web` folder, we need to adjust
   - Go back to **Settings → Pages**
   - Under "Build and deployment", change:
     - Source: **GitHub Actions** (if available)
     - OR: Keep "Deploy from a branch" and we'll move files

---

## Step 2: Configure for Web Folder (Option A - Recommended)

Since your site is in `/web` folder, let's create a GitHub Actions workflow:

1. **I'll create the workflow file for you** (already done below)

2. **Push the changes** (I'll do this)

3. **GitHub will automatically deploy from the web folder**

---

## Step 2 Alternative: Move Web Files to Root (Option B)

If you prefer to keep it simple without GitHub Actions:

```bash
# Move web files to root
cp -r web/* .
git add .
git commit -m "Move web files to root for GitHub Pages"
git push -u origin claude/dusk-lending-platform-XP99i
```

Then in GitHub Settings → Pages:
- Branch: claude/dusk-lending-platform-XP99i
- Folder: /(root)

---

## Step 3: Configure GoDaddy DNS

1. **Login to GoDaddy:**
   ```
   https://dcc.godaddy.com/
   ```

2. **Navigate to DNS Management:**
   - Click **My Products**
   - Find **dusklend.io**
   - Click **DNS** (or "Manage DNS")

3. **Delete Old Records:**
   - Delete any existing A records for `@`
   - Delete any existing CNAME records for `www`

4. **Add GitHub Pages A Records:**

   Click **Add** and create these 4 A records:

   **A Record 1:**
   ```
   Type: A
   Name: @
   Value: 185.199.108.153
   TTL: 600 seconds
   ```

   **A Record 2:**
   ```
   Type: A
   Name: @
   Value: 185.199.109.153
   TTL: 600 seconds
   ```

   **A Record 3:**
   ```
   Type: A
   Name: @
   Value: 185.199.110.153
   TTL: 600 seconds
   ```

   **A Record 4:**
   ```
   Type: A
   Name: @
   Value: 185.199.111.153
   TTL: 600 seconds
   ```

5. **Add CNAME Record for WWW:**
   ```
   Type: CNAME
   Name: www
   Value: luoislitt.github.io
   TTL: 600 seconds
   ```

6. **Save all changes**

---

## Step 4: Wait for DNS Propagation

**How long:** 5-30 minutes (sometimes up to 48 hours)

**Check status:**
- Visit: https://www.whatsmydns.net/#A/dusklend.io
- You should see the GitHub Pages IPs appearing

**Or use command line:**
```bash
dig dusklend.io +short
```
Should return GitHub Pages IPs.

---

## Step 5: Verify in GitHub

1. **Go back to GitHub:**
   ```
   https://github.com/LuoisLitt/DUSKLENDING/settings/pages
   ```

2. **You should see:**
   ```
   Your site is live at https://dusklend.io/
   ```

3. **If you see a warning about custom domain:**
   - It means DNS hasn't propagated yet
   - Wait and refresh the page

---

## Step 6: Test Your Site!

Once DNS has propagated:

1. **Open browser**

2. **Visit:**
   ```
   https://dusklend.io
   ```

3. **You should see:**
   - Beautiful purple gradient background
   - "🌙 DUSK Lending Platform" header
   - Connect Wallet button
   - All the features!

---

## 🎉 You're Live!

Your DUSK Lending Platform is now live at:
- **https://dusklend.io**
- **https://www.dusklend.io**

---

## 🔧 Troubleshooting

### "404 - File not found"
→ Make sure GitHub Pages is deploying from the correct folder
→ Check that branch is: claude/dusk-lending-platform-XP99i
→ Verify CNAME file exists in the deployed folder

### "Custom domain not working"
→ Wait for DNS propagation (up to 48 hours)
→ Check DNS with: https://www.whatsmydns.net/#A/dusklend.io
→ Verify all 4 A records are correct in GoDaddy

### "SSL certificate error"
→ Wait 15-30 minutes for GitHub to provision HTTPS
→ GitHub automatically creates certificates for custom domains

### "Site loads but without styles"
→ Check if paths in HTML are relative (not absolute)
→ Make sure CSS/JS files are in the correct folder structure

---

## 📝 Quick Reference

| What | Where | Value |
|------|-------|-------|
| GitHub Pages | Settings → Pages | Branch: claude/dusk-lending-platform-XP99i |
| A Records | GoDaddy DNS | 185.199.108-111.153 (4 records) |
| CNAME | GoDaddy DNS | luoislitt.github.io |
| Custom Domain | GitHub Pages | dusklend.io |
| Your Site | Browser | https://dusklend.io |

---

**Your site will be live at: https://dusklend.io** 🌐
