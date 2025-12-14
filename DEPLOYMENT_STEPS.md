# 🚀 Live Deployment Steps - Follow These Exactly

You are currently here: `/home/user/DUSKLENDING/web`

## Step 1: Login to Vercel

Run this command:
```bash
vercel login
```

**What will happen:**
```
Vercel CLI 33.0.1
? Log in to Vercel (Use arrow keys)
❯ Continue with GitHub
  Continue with GitLab
  Continue with Bitbucket
  Continue with Email
  Continue with SAML Single Sign-On
```

**What to do:**
- Choose your preferred login method (GitHub is easiest if you have an account)
- Follow the prompts to authenticate
- A browser window will open
- Click "Authorize" in your browser
- Return to terminal when you see "Success!"

---

## Step 2: Deploy Your Site

Run this command:
```bash
vercel --prod
```

**What will happen - Answer these prompts:**

```
? Set up and deploy "~/DUSKLENDING/web"?
```
→ Type: **Y** (Yes)

```
? Which scope do you want to deploy to?
```
→ Select your account name (use arrow keys)

```
? Link to existing project?
```
→ Type: **N** (No)

```
? What's your project's name?
```
→ Type: **dusk-lending** (or any name you like)

```
? In which directory is your code located?
```
→ Press **Enter** (it will use `.` which is correct)

```
Deploying...
✅ Production: https://dusk-lending-xxxxx.vercel.app
```

**IMPORTANT:** Copy this URL! You'll need it.

---

## Step 3: Add Custom Domain (dusklend.io)

Now that your site is deployed, add your custom domain:

### 3A: In Vercel Dashboard

1. **Open browser and go to:**
   ```
   https://vercel.com/dashboard
   ```

2. **Click on your project:** `dusk-lending`

3. **Click:** Settings (tab at top)

4. **Click:** Domains (in left sidebar)

5. **In the input box, type:**
   ```
   dusklend.io
   ```

6. **Click:** Add

7. **Repeat for www:**
   ```
   www.dusklend.io
   ```

8. **Click:** Add

### 3B: You'll see DNS Configuration Needed

Vercel will show something like:
```
⚠️ Invalid Configuration
Configure your DNS records:

A Record
  Name: @
  Value: 76.76.21.21

CNAME Record
  Name: www
  Value: cname.vercel-dns.com
```

**Keep this page open!** You'll need these values for GoDaddy.

---

## Step 4: Configure GoDaddy DNS

### 4A: Login to GoDaddy

1. **Open new browser tab:**
   ```
   https://dcc.godaddy.com/
   ```

2. **Login** with your GoDaddy account

3. **Navigate to:**
   - My Products → Domain Portfolio
   - Click **dusklend.io**
   - Click **DNS** button (or "Manage DNS")

### 4B: Delete Old Records (Important!)

Look for existing records for:
- `@` (A record)
- `www` (CNAME record)

**Delete them if they exist!**
- Click the pencil/edit icon
- Click Delete
- Confirm

### 4C: Add New Records

**Add A Record:**
1. Click **Add** button
2. Select **Type:** A
3. **Name:** @ (type @ symbol)
4. **Value:** 76.76.21.21
5. **TTL:** 600 seconds (or use default)
6. Click **Save**

**Add CNAME Record:**
1. Click **Add** button again
2. Select **Type:** CNAME
3. **Name:** www
4. **Value:** cname.vercel-dns.com
5. **TTL:** 600 seconds (or use default)
6. Click **Save**

### 4D: Save Changes

- Click **Save** or **Save All** at the bottom
- You should see a success message

---

## Step 5: Verify in Vercel

1. **Go back to Vercel dashboard** (from Step 3)

2. **Refresh the Domains page**

3. **You should see:**
   ```
   dusklend.io - Awaiting DNS Propagation
   www.dusklend.io - Awaiting DNS Propagation
   ```

4. **After 5-30 minutes, it will change to:**
   ```
   dusklend.io - Valid Configuration ✓
   www.dusklend.io - Valid Configuration ✓
   ```

---

## Step 6: Wait for DNS Propagation

**How long:** Usually 5-30 minutes, can take up to 48 hours

**Check status:**
- Visit: https://www.whatsmydns.net/#A/dusklend.io
- You should see 76.76.21.21 appearing in different locations

**Or use command line:**
```bash
dig dusklend.io +short
```
Should return: `76.76.21.21`

---

## Step 7: Test Your Site!

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

4. **Test it:**
   - Click "Connect Wallet"
   - Try the platform features

---

## 🎉 You're Live!

Your DUSK Lending Platform is now live at:
- **https://dusklend.io**
- **https://www.dusklend.io**

Both URLs will work!

---

## 🔧 If Something Goes Wrong

### "Site not loading"
→ Wait longer for DNS (up to 48 hours)
→ Check DNS with: https://www.whatsmydns.net/#A/dusklend.io

### "Invalid Configuration" in Vercel
→ Double-check GoDaddy DNS settings
→ Make sure old records are deleted
→ Verify exact values: 76.76.21.21 and cname.vercel-dns.com

### "SSL Certificate Error"
→ Wait 15-30 minutes for auto-provisioning
→ Vercel automatically creates HTTPS certificates

### "Need to redeploy"
```bash
cd /home/user/DUSKLENDING/web
vercel --prod
```

---

## 📝 Summary of Commands

Here's everything in order:

```bash
# You are here: /home/user/DUSKLENDING/web

# 1. Login
vercel login

# 2. Deploy
vercel --prod

# 3. Then configure domain in browser (Vercel + GoDaddy)
```

---

## 🎯 Quick Reference

| What | Where | How |
|------|-------|-----|
| Deploy site | Terminal | `vercel --prod` |
| Add domain | Vercel Dashboard | Settings → Domains |
| Configure DNS | GoDaddy | DNS Management |
| Check DNS | Browser | whatsmydns.net |
| Your site | Browser | https://dusklend.io |

---

**Ready? Start with Step 1 above! 🚀**
