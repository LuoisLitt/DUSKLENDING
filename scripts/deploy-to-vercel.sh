#!/bin/bash

echo "🚀 Deploying DUSK Lending Platform to dusklend.io"
echo "=================================================="
echo ""

# Check if vercel is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Navigate to web directory
cd "$(dirname "$0")/../web" || exit

echo "📝 Current directory: $(pwd)"
echo ""

# Check if contracts are deployed to testnet
if [ -f "../deployments/dusk-testnet.json" ]; then
    echo "✅ Testnet contracts found"

    # Ask if user wants to update config
    read -p "Update web config with testnet addresses? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📝 Updating web configuration..."
        cd ..
        HARDHAT_NETWORK=dusk-testnet node scripts/update-web-config.js
        cd web
    fi
else
    echo "⚠️  Warning: No testnet deployment found"
    echo "   You may want to deploy contracts first:"
    echo "   npx hardhat run scripts/deploy.js --network dusk-testnet"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "🌐 Deploying to Vercel..."
echo ""

# Deploy to Vercel
vercel --prod

echo ""
echo "============================================================"
echo "✅ Deployment Complete!"
echo "============================================================"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Add custom domain in Vercel:"
echo "   → Visit: https://vercel.com/dashboard"
echo "   → Select your project"
echo "   → Settings → Domains"
echo "   → Add: dusklend.io and www.dusklend.io"
echo ""
echo "2. Configure GoDaddy DNS:"
echo "   → Go to: https://dcc.godaddy.com/"
echo "   → My Products → DNS"
echo "   → Add A record: @ → 76.76.21.21"
echo "   → Add CNAME: www → cname.vercel-dns.com"
echo ""
echo "3. Wait for DNS propagation (5-30 minutes)"
echo ""
echo "4. Your site will be live at: https://dusklend.io"
echo ""
echo "============================================================"
echo ""
echo "📖 Full guide: DEPLOY_TO_DUSKLEND_IO.md"
echo ""
