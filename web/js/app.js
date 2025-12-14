// Global variables
let provider;
let signer;
let userAddress;
let duskContract;
let usdtContract;
let lendingPoolContract;

// Initialize on page load
window.addEventListener('load', async () => {
    await checkMetaMask();
    setupEventListeners();
});

// Check if MetaMask is installed
async function checkMetaMask() {
    console.log('=== Wallet Detection ===');
    console.log('window.ethereum exists:', typeof window.ethereum !== 'undefined');

    if (typeof window.ethereum !== 'undefined') {
        console.log('Ethereum provider detected!');
        console.log('Provider details:', {
            isMetaMask: window.ethereum.isMetaMask,
            chainId: window.ethereum.chainId,
            selectedAddress: window.ethereum.selectedAddress
        });

        if (window.ethereum.isMetaMask) {
            console.log('✅ MetaMask is installed and ready!');
        } else {
            console.log('⚠️ Non-MetaMask wallet detected');
        }
    } else {
        console.log('❌ No Ethereum provider found');
        showStatus('Please install MetaMask to use this app', 'error');
    }
    console.log('=======================');
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('connectWallet').addEventListener('click', connectWallet);
}

// Connect wallet
async function connectWallet() {
    try {
        console.log('Connect Wallet button clicked!');
        console.log('window.ethereum exists:', typeof window.ethereum !== 'undefined');
        console.log('window.ethereum object:', window.ethereum);

        if (typeof window.ethereum === 'undefined') {
            alert('MetaMask is not installed!\n\nPlease install MetaMask from https://metamask.io/download/');
            showStatus('Please install MetaMask browser extension', 'error');
            return;
        }

        // Check if MetaMask is the provider
        if (window.ethereum.isMetaMask) {
            console.log('MetaMask detected!');
        } else {
            console.log('Warning: ethereum provider exists but might not be MetaMask');
        }

        console.log('Requesting accounts...');
        showStatus('Opening MetaMask... Please check your browser extension popup', 'info');

        // Request account access with better error handling
        let accounts;
        try {
            // First, try to check if already connected
            accounts = await window.ethereum.request({ method: 'eth_accounts' });

            // If no accounts, request access
            if (!accounts || accounts.length === 0) {
                console.log('No accounts found, requesting access...');
                accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
            } else {
                console.log('Already connected accounts found:', accounts);
            }
        } catch (requestError) {
            console.error('Error requesting accounts:', requestError);

            // Try fallback method using ethereum.enable() (deprecated but sometimes works)
            try {
                console.log('Trying fallback connection method...');
                accounts = await window.ethereum.enable();
                console.log('Fallback method succeeded!');
            } catch (fallbackError) {
                console.error('Fallback also failed:', fallbackError);

                if (requestError.code === 4001) {
                    showStatus('Connection rejected by user', 'error');
                } else if (requestError.code === -32002) {
                    showStatus('Connection request already pending. Please check MetaMask popup and approve/reject it first.', 'error');
                } else {
                    showStatus('MetaMask error. Try: 1) Refresh page 2) Lock/unlock MetaMask 3) Restart browser', 'error');
                }
                return;
            }
        }

        console.log('Accounts received:', accounts);
        userAddress = accounts[0];

        // Setup provider and signer
        provider = new ethers.providers.Web3Provider(window.ethereum);
        signer = provider.getSigner();

        // Check network
        const network = await provider.getNetwork();
        console.log('Connected to network:', network);

        // Update UI
        updateNetworkInfo(network);
        updateWalletInfo();

        // Initialize contracts
        await initializeContracts();

        // Load data
        await loadPoolData();
        await loadUserData();

        showStatus('Wallet connected successfully!', 'success');

        // Listen for account changes
        window.ethereum.on('accountsChanged', handleAccountsChanged);
        window.ethereum.on('chainChanged', handleChainChanged);

    } catch (error) {
        console.error('Error connecting wallet:', error);
        showStatus('Error connecting wallet: ' + error.message, 'error');
    }
}

// Handle account changes
function handleAccountsChanged(accounts) {
    if (accounts.length === 0) {
        showStatus('Please connect to MetaMask', 'info');
        location.reload();
    } else {
        location.reload();
    }
}

// Handle chain changes
function handleChainChanged() {
    location.reload();
}

// Update network info
function updateNetworkInfo(network) {
    document.getElementById('networkName').textContent = network.name || 'Unknown';
    document.getElementById('chainId').textContent = network.chainId;

    // Update network status color
    const statusEl = document.getElementById('networkStatus');
    if (network.chainId === 745 || network.chainId === 31337) {
        statusEl.style.borderLeft = '4px solid #48bb78';
    } else {
        statusEl.style.borderLeft = '4px solid #f56565';
        showStatus('Please switch to DuskEVM Testnet (Chain ID: 745) or Hardhat (31337)', 'error');
    }
}

// Update wallet info
function updateWalletInfo() {
    document.getElementById('connectWallet').classList.add('hidden');
    document.getElementById('walletInfo').classList.remove('hidden');
    document.getElementById('walletAddress').textContent =
        userAddress.slice(0, 6) + '...' + userAddress.slice(-4);
}

// Initialize contracts
async function initializeContracts() {
    const network = await provider.getNetwork();
    let addresses;

    // Determine which network we're on
    if (network.chainId === 31337) {
        CURRENT_NETWORK = 'hardhat';
        addresses = CONTRACT_ADDRESSES.hardhat;
    } else if (network.chainId === 745) {
        CURRENT_NETWORK = 'duskTestnet';
        addresses = CONTRACT_ADDRESSES.duskTestnet;

        // Check if addresses are configured
        if (!addresses.DuskLendingPool) {
            showStatus('Contracts not deployed on DuskEVM Testnet yet. Please deploy first.', 'error');
            return;
        }
    } else {
        showStatus('Unsupported network. Please switch to DuskEVM Testnet or Hardhat.', 'error');
        return;
    }

    // Initialize contract instances
    duskContract = new ethers.Contract(addresses.MockDUSK, DUSK_ABI, signer);
    usdtContract = new ethers.Contract(addresses.MockUSDT, USDT_ABI, signer);
    lendingPoolContract = new ethers.Contract(addresses.DuskLendingPool, LENDING_POOL_ABI, signer);

    console.log('Contracts initialized:', addresses);
}

// Load pool data
async function loadPoolData() {
    try {
        const duskPrice = await lendingPoolContract.duskPriceUSD();
        const totalLiquidity = await lendingPoolContract.totalUsdtLiquidity();
        const totalBorrowed = await lendingPoolContract.totalUsdtBorrowed();

        // Update UI
        const priceInDollars = parseFloat(ethers.utils.formatUnits(duskPrice, 8));
        document.getElementById('duskPrice').textContent = `$${priceInDollars.toFixed(2)}`;
        document.getElementById('totalLiquidity').textContent =
            parseFloat(ethers.utils.formatUnits(totalLiquidity, 6)).toFixed(2) + ' USDT';

        const available = totalLiquidity.sub(totalBorrowed);
        document.getElementById('availableBorrow').textContent =
            parseFloat(ethers.utils.formatUnits(available, 6)).toFixed(2) + ' USDT';

    } catch (error) {
        console.error('Error loading pool data:', error);
    }
}

// Load user data
async function loadUserData() {
    try {
        // Get balances
        const duskBalance = await duskContract.balanceOf(userAddress);
        const usdtBalance = await usdtContract.balanceOf(userAddress);

        document.getElementById('duskBalance').textContent =
            parseFloat(ethers.utils.formatEther(duskBalance)).toFixed(2);
        document.getElementById('usdtBalance').textContent =
            parseFloat(ethers.utils.formatUnits(usdtBalance, 6)).toFixed(2);

        // Get position data
        const userData = await lendingPoolContract.users(userAddress);
        const totalDebt = await lendingPoolContract.getUserDebt(userAddress);
        const healthFactor = await lendingPoolContract.getHealthFactor(userAddress);
        const maxBorrow = await lendingPoolContract.getMaxBorrowAmount(userAddress);

        // Update UI
        document.getElementById('userCollateral').textContent =
            parseFloat(ethers.utils.formatEther(userData.duskCollateral)).toFixed(2) + ' DUSK';
        document.getElementById('userDebt').textContent =
            parseFloat(ethers.utils.formatUnits(totalDebt, 6)).toFixed(2) + ' USDT';

        // Health factor
        const maxUint = ethers.BigNumber.from('0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff');
        if (healthFactor.eq(maxUint)) {
            document.getElementById('healthFactor').textContent = '∞';
        } else {
            const hf = parseFloat(ethers.utils.formatEther(healthFactor)).toFixed(2);
            document.getElementById('healthFactor').textContent = hf;

            // Color code health factor
            const hfEl = document.getElementById('healthFactor');
            if (parseFloat(hf) < 1.2) {
                hfEl.style.color = '#f56565';
            } else if (parseFloat(hf) < 1.5) {
                hfEl.style.color = '#ed8936';
            } else {
                hfEl.style.color = '#48bb78';
            }
        }

        document.getElementById('maxBorrow').textContent =
            parseFloat(ethers.utils.formatUnits(maxBorrow, 6)).toFixed(2) + ' USDT';

    } catch (error) {
        console.error('Error loading user data:', error);
    }
}

// Get faucet tokens
async function getFaucetTokens() {
    try {
        showStatus('Requesting faucet tokens...', 'info');

        // Get DUSK
        const duskTx = await duskContract.faucet();
        await duskTx.wait();

        // Get USDT
        const usdtTx = await usdtContract.faucet();
        await usdtTx.wait();

        showStatus('Received 1,000 DUSK and 10,000 USDT!', 'success');
        await loadUserData();

    } catch (error) {
        console.error('Error getting faucet tokens:', error);
        showStatus('Error: ' + error.message, 'error');
    }
}

// Deposit DUSK
async function depositDusk() {
    try {
        const amount = document.getElementById('depositAmount').value;
        if (!amount || parseFloat(amount) <= 0) {
            showStatus('Please enter a valid amount', 'error');
            return;
        }

        showStatus('Depositing DUSK...', 'info');

        const amountWei = ethers.utils.parseEther(amount);

        // Approve
        const approveTx = await duskContract.approve(lendingPoolContract.address, amountWei);
        await approveTx.wait();

        // Deposit
        const depositTx = await lendingPoolContract.depositDusk(amountWei);
        await depositTx.wait();

        showStatus(`Successfully deposited ${amount} DUSK!`, 'success');
        document.getElementById('depositAmount').value = '';
        await loadUserData();
        await loadPoolData();

    } catch (error) {
        console.error('Error depositing:', error);
        showStatus('Error: ' + error.message, 'error');
    }
}

// Borrow USDT
async function borrowUsdt() {
    try {
        const amount = document.getElementById('borrowAmount').value;
        if (!amount || parseFloat(amount) <= 0) {
            showStatus('Please enter a valid amount', 'error');
            return;
        }

        showStatus('Borrowing USDT...', 'info');

        const amountUsdt = ethers.utils.parseUnits(amount, 6);

        const borrowTx = await lendingPoolContract.borrowUsdt(amountUsdt);
        await borrowTx.wait();

        showStatus(`Successfully borrowed ${amount} USDT!`, 'success');
        document.getElementById('borrowAmount').value = '';
        await loadUserData();
        await loadPoolData();

    } catch (error) {
        console.error('Error borrowing:', error);
        showStatus('Error: ' + error.message, 'error');
    }
}

// Repay USDT
async function repayUsdt() {
    try {
        const amount = document.getElementById('repayAmount').value;
        if (!amount || parseFloat(amount) <= 0) {
            showStatus('Please enter a valid amount', 'error');
            return;
        }

        showStatus('Repaying USDT...', 'info');

        const amountUsdt = ethers.utils.parseUnits(amount, 6);

        // Approve
        const approveTx = await usdtContract.approve(lendingPoolContract.address, amountUsdt);
        await approveTx.wait();

        // Repay
        const repayTx = await lendingPoolContract.repayUsdt(amountUsdt);
        await repayTx.wait();

        showStatus(`Successfully repaid ${amount} USDT!`, 'success');
        document.getElementById('repayAmount').value = '';
        await loadUserData();
        await loadPoolData();

    } catch (error) {
        console.error('Error repaying:', error);
        showStatus('Error: ' + error.message, 'error');
    }
}

// Withdraw DUSK
async function withdrawDusk() {
    try {
        const amount = document.getElementById('withdrawAmount').value;
        if (!amount || parseFloat(amount) <= 0) {
            showStatus('Please enter a valid amount', 'error');
            return;
        }

        showStatus('Withdrawing DUSK...', 'info');

        const amountWei = ethers.utils.parseEther(amount);

        const withdrawTx = await lendingPoolContract.withdrawDusk(amountWei);
        await withdrawTx.wait();

        showStatus(`Successfully withdrew ${amount} DUSK!`, 'success');
        document.getElementById('withdrawAmount').value = '';
        await loadUserData();
        await loadPoolData();

    } catch (error) {
        console.error('Error withdrawing:', error);
        showStatus('Error: ' + error.message, 'error');
    }
}

// Supply USDT
async function supplyUsdt() {
    try {
        const amount = document.getElementById('supplyAmount').value;
        if (!amount || parseFloat(amount) <= 0) {
            showStatus('Please enter a valid amount', 'error');
            return;
        }

        showStatus('Supplying USDT...', 'info');

        const amountUsdt = ethers.utils.parseUnits(amount, 6);

        // Approve
        const approveTx = await usdtContract.approve(lendingPoolContract.address, amountUsdt);
        await approveTx.wait();

        // Supply
        const supplyTx = await lendingPoolContract.supplyUsdt(amountUsdt);
        await supplyTx.wait();

        showStatus(`Successfully supplied ${amount} USDT!`, 'success');
        document.getElementById('supplyAmount').value = '';
        await loadUserData();
        await loadPoolData();

    } catch (error) {
        console.error('Error supplying:', error);
        showStatus('Error: ' + error.message, 'error');
    }
}

// Add DuskEVM Testnet to MetaMask
async function addDuskNetwork() {
    try {
        if (typeof window.ethereum === 'undefined') {
            alert('Please install MetaMask first!');
            return;
        }

        showStatus('Adding DuskEVM Testnet to MetaMask...', 'info');

        await window.ethereum.request({
            method: 'wallet_addEthereumChain',
            params: [{
                chainId: '0x2E9', // 745 in hex
                chainName: 'DuskEVM Testnet',
                nativeCurrency: {
                    name: 'DUSK',
                    symbol: 'DUSK',
                    decimals: 18
                },
                rpcUrls: ['https://rpc.testnet.evm.dusk.network'],
                blockExplorerUrls: null
            }]
        });

        showStatus('DuskEVM Testnet added successfully!', 'success');

    } catch (error) {
        console.error('Error adding network:', error);
        if (error.code === 4001) {
            showStatus('Network addition rejected by user', 'error');
        } else {
            showStatus('Error adding network: ' + error.message, 'error');
        }
    }
}

// Show status message
function showStatus(message, type = 'info') {
    const statusEl = document.getElementById('statusMessage');
    statusEl.textContent = message;
    statusEl.className = `status-message ${type}`;
    statusEl.classList.remove('hidden');

    // Auto hide after 5 seconds
    setTimeout(() => {
        statusEl.classList.add('hidden');
    }, 5000);
}
