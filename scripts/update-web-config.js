const fs = require('fs');
const path = require('path');

async function main() {
    console.log('📝 Updating web interface configuration...\n');

    // Get network from command line or use hardhat
    const network = process.env.HARDHAT_NETWORK || 'hardhat';
    const deploymentFile = path.join(__dirname, '../deployments', `${network}.json`);

    if (!fs.existsSync(deploymentFile)) {
        console.error('❌ Deployment file not found:', deploymentFile);
        console.log('Please deploy contracts first with:');
        console.log(`  npx hardhat run scripts/deploy.js --network ${network}`);
        process.exit(1);
    }

    // Read deployment info
    const deployment = JSON.parse(fs.readFileSync(deploymentFile, 'utf8'));
    console.log('✅ Found deployment:', network);
    console.log('   Deployer:', deployment.deployer);
    console.log('   Contracts:');
    console.log('     MockDUSK:', deployment.contracts.MockDUSK);
    console.log('     MockUSDT:', deployment.contracts.MockUSDT);
    console.log('     DuskLendingPool:', deployment.contracts.DuskLendingPool);

    // Update web config
    const configFile = path.join(__dirname, '../web/js/config.js');
    let config = fs.readFileSync(configFile, 'utf8');

    // Determine which network config to update
    const networkKey = network === 'localhost' ? 'hardhat' : 'duskTestnet';

    // Replace contract addresses
    const addressesRegex = new RegExp(
        `${networkKey}:\\s*{[^}]*MockDUSK:\\s*"[^"]*",[^}]*MockUSDT:\\s*"[^"]*",[^}]*DuskLendingPool:\\s*"[^"]*"[^}]*}`,
        's'
    );

    const newAddresses = `${networkKey}: {
        MockDUSK: "${deployment.contracts.MockDUSK}",
        MockUSDT: "${deployment.contracts.MockUSDT}",
        DuskLendingPool: "${deployment.contracts.DuskLendingPool}"
    }`;

    config = config.replace(addressesRegex, newAddresses);

    // Write updated config
    fs.writeFileSync(configFile, config);
    console.log('\n✅ Updated web/js/config.js with contract addresses');

    // Display instructions
    console.log('\n📖 Next steps:');
    console.log('1. Start the web server:');
    console.log('   npx http-server web -p 8080 -c-1');
    console.log('2. Open browser: http://localhost:8080');
    console.log('3. Connect your MetaMask wallet');
    console.log(`4. Make sure MetaMask is on ${network} network`);
    console.log('\n🌐 Or deploy to GitHub Pages - see WEB_HOSTING.md');
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });
