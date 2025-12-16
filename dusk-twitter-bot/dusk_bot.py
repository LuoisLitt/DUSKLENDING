#!/usr/bin/env python3
"""
Dusk Network Twitter Growth Bot
Full automated posting with real Dusk content
"""

import tweepy
import time
import random
import json
import sys
import os
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============== CONFIGURATION ==============
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Growth Settings
DAILY_FOLLOW_LIMIT = int(os.getenv("DAILY_FOLLOW_LIMIT", "50"))
ANALYTICS_FILE = os.getenv("ANALYTICS_FILE", "dusk_twitter_analytics.json")

# ============== REAL DUSK CONTENT (Updated 2025) ==============
DUSK_FACTS = [
    "Dusk mainnet launched January 7, 2025 - the first privacy-preserving blockchain for regulated finance",
    "Hyperstaking on Dusk allows smart contracts to implement custom staking logic - like Account Abstraction for staking",
    "Zedger enables privacy-preserving asset issuance, clearance, and settlement - fully operational in 2025",
    "NPEX has tokenized $300M+ in assets on Dusk - real world financial products on-chain",
    "Citadel is Dusk's ZK-powered KYC/AML tool that reconciles privacy with regulatory compliance",
    "Dusk uses PlonK proof system and Poseidon hash - the most advanced ZK cryptography available",
    "Succinct Attestation consensus allows infinite scalability of verifiers on Dusk",
    "Kadcast makes block propagation 10x more efficient than conventional blockchain methods",
    "Dusk VM is a ZK-friendly virtual machine that handles privacy computations at scale",
    "Transactions on Dusk are private but auditable - institutions get confidentiality AND compliance",
    "Dusk is MiCA-ready and integrating with custodian banks for institutional regulated finance",
    "Privacy within a shared state - what no other blockchain has achieved",
    "DuskPay is launching - a privacy-first payment platform partnering with stablecoin issuers",
    "Lightspeed L2 brings EVM compatibility while settling on Dusk's privacy-preserving Layer 1",
    "Dusk partnered with 21X as a trade participant - bringing institutional regulated trading on-chain",
    "One-block sync to network, no state bloat, web wallet with ZKP computations in-browser",
    "DuskEVM combines Ethereum tools with privacy features for seamless institutional onboarding",
    "Zero-knowledge proofs on Dusk maintain privacy during cross-chain transfers",
]

DUSK_TECH_DETAILS = [
    "zero-knowledge proofs that maintain auditability for regulators",
    "PlonK proof system combined with Poseidon hash for maximum security",
    "Succinct Attestation consensus - proof-of-stake with complete state finality",
    "Kadcast protocol for 10x more efficient data propagation",
    "Hyperstaking - programmable staking with custom smart contract logic",
    "Citadel - privacy-preserving digital identity without revealing personal data",
    "Zedger Asset protocol for compliant tokenization and issuance",
    "privacy-preserving smart contracts that institutions actually want",
    "Dusk VM optimized for ZK proofs and high-throughput privacy transactions",
    "DuskEVM - combining EVM compatibility with native privacy features",
    "Lightspeed L2 for Ethereum interoperability with Dusk settlement",
    "DuskPay integration for privacy-first stablecoin payments",
]

INSTITUTIONAL_PROBLEMS = [
    "Institutions can't put $100M+ deals on transparent blockchains - they need confidentiality",
    "Regulators demand auditability but privacy seems impossible - Dusk solves both",
    "Traditional blockchains expose all transaction data - deal-breaker for real finance",
    "KYC/AML creates friction while blockchain transparency violates GDPR",
    "MEV and front-running make public chains unsuitable for institutional trading",
    "Compliance requirements like MiCA and DORA make most blockchains unusable for regulated finance",
    "TradFi institutions need privacy for competitive deals but regulators need transparency",
]

DUSK_ADVANTAGES = [
    "Private transactions that regulators can still audit - the only way forward",
    "MiCA compliance baked into the protocol from day one",
    "Custodian bank integration for trust-minimized clearance and settlement",
    "$300M+ in real assets already tokenized on mainnet via NPEX",
    "Full on-chain issuance, clearance & settlement - the complete solution",
    "Privacy without sacrificing the unified liquidity of public blockchains",
    "21X partnership brings regulated institutional trading to DeFi",
    "DuskEVM allows Ethereum devs to build privacy-preserving dApps instantly",
    "Native stablecoin support through DuskPay for seamless payments",
]

# ============== RWA MARKET FACTS (2025 News) ==============
RWA_MARKET_FACTS = [
    "RWA tokenization market hit $35.78B in November 2025 - private credit leads at $17B",
    "BlackRock's BUIDL fund holds $2.9B in tokenized US Treasuries - 44% market share",
    "RWA market projected to reach $16-30 trillion by 2030 according to BCG",
    "Franklin Templeton's tokenized MMF now accepted as loan collateral by DBS Bank",
    "JPMorgan and Franklin Templeton deploying capital into tokenized infrastructure in 2025",
    "UBS, KKR, and major banks moved from pilots to production-level tokenization in 2025",
    "Tokenized assets could unlock $230 trillion in collateral currently sitting idle",
    "On-chain capital markets reaching $33B+ as institutions embrace blockchain settlement",
    "Private credit tokenization is the fastest growing RWA category at ~$17 billion",
    "Major institutions choosing privacy-preserving chains for tokenized securities",
]

STABLECOIN_FACTS = [
    "Stablecoin market cap surpassed $300B in 2025 - up from $204B in early 2025",
    "USDT and USDC account for 93% of stablecoin market - $145B and $60.2B respectively",
    "Stablecoin transaction volume hit $4 trillion between January-July 2025",
    "GENIUS Act passed July 2025 - first US federal stablecoin regulatory framework",
    "MiCA regulation forcing EU exchanges to delist non-compliant stablecoins",
    "Binance delisted USDT, DAI, TUSD in EU due to MiCA compliance requirements",
    "All US stablecoin issuers now require federal licensing and 100% reserve backing",
    "Stablecoin volumes up 83% year-over-year - highest ever annual transaction volume",
    "Privacy-preserving stablecoins becoming essential for institutional DeFi",
    "Stablecoins reaching mainstream adoption with $300B+ market cap in 2025",
]

TOKENIZATION_TRENDS = [
    "Securities tokenization enabling 24/7 trading and instant settlement in 2025",
    "Real estate tokenization unlocking fractional ownership for retail investors",
    "Tokenized bonds reducing underwriting costs and improving time-to-market",
    "World Economic Forum: tokenization transforming the entire future of finance",
    "Europe's MiCA framework attracting tokenization projects with clear regulations",
    "Tokenized government bonds gaining traction for on-chain trading ease",
    "Major banks issuing digital-native bonds directly on blockchain platforms",
    "Asset tokenization enabling fractionalization - making TradFi accessible to all",
    "On-chain capital markets dissolving barriers between global financial systems",
    "Regulatory clarity in 2025 accelerating institutional tokenization adoption",
]

# ============== VIRAL PARAPHRASE TEMPLATES ==============
PARAPHRASE_STYLES = [
    "{fact}\n\nThis is what the future of finance looks like. 🔮 #DeFi #RWA #DUSK",
    "GM to everyone building the future of regulated DeFi 🌅\n\n{fact}\n\n#Blockchain #Privacy",
    "Imagine: {advantage}\n\nYou don't have to imagine. It's live on @DuskFoundation.\n\n#Web3 #Crypto",
    "Thread on why {tech_detail} matters 🧵\n\nBut honestly? Just watch what @DuskFoundation is building.\n\n$DUSK",
    "The market doesn't understand {fact} yet.\n\nThey will. #Crypto #RWA",
    "Quick reminder: {fact}\n\nMainnet is live. Institutions are building. The future is now. 🚀",
    "Everyone: 'When RWA adoption?'\n\n{fact}\n\nIt's already happening. #DuskNetwork #TradFi",
    "Can't stop thinking about {fact}\n\nThis changes everything for institutional adoption. 💡",
    "Hot take that's not really hot: {advantage}\n\n@DuskFoundation proved it. #Blockchain",
]

# ============== ENHANCED TWEET TEMPLATES (Optimized for Reach) ==============
TWEET_TEMPLATES = {
    "hot_takes": [
        "Unpopular opinion: {statement}\n\nMost RWA projects will fail because of this. #DUSK #RWA #Crypto",
        "Everyone is building 'RWA chains' but missing the obvious: {problem}\n\n@DuskFoundation gets it. #DeFi",
        "Hot take: Transparent blockchains for securities = DOA\n\n{fact}\n\nThis is why $DUSK is different. #Blockchain",
        "While everyone talks about tokenization, {fact}\n\nThis changes everything. #RWA #Web3",
        "Controversial but true: 90% of RWA projects can't handle real institutional capital.\n\nWhy? {problem} #TradFi",
        "The elephant in the room: {problem}\n\nEvery RWA project ignores this. Except @DuskFoundation. #Crypto",
    ],
    "dusk_milestones": [
        "🚨 MAINNET MILESTONE: {fact}\n\nThis is what real institutional blockchain looks like. $DUSK #RWA",
        "Major @DuskFoundation update: {fact}\n\nThe infrastructure for regulated DeFi is here. #Blockchain",
        "While other chains talk, Dusk delivers: {fact}\n\nReal adoption, real assets, real privacy. #DeFi #Privacy",
        "Game-changing tech: {tech_detail}\n\nOnly possible on @DuskFoundation. #Privacy #Compliance #Web3",
        "From zero to hero: {fact}\n\n2025 is Dusk's year. Don't say you weren't told. $DUSK #Crypto",
        "Just launched: {fact}\n\nTradFi meets DeFi. The future is here. 🚀 #DuskNetwork",
    ],
    "education_tech": [
        "Let's talk about {tech_detail}\n\nThis is the unlock for institutional RWAs. 🧵 #Crypto #Privacy",
        "Privacy vs Compliance - the false dilemma.\n\n{fact}\n\nProblem solved. #DUSK #Blockchain",
        "Why institutions need privacy: {problem}\n\nHow Dusk solves it: {advantage} #RWA #DeFi",
        "Tech breakdown: {tech_detail}\n\nThis is why $DUSK is built different from other L1s. #Web3",
        "Real talk about RWA infrastructure: {fact}\n\nNot speculation. Real working tech. #TradFi #Blockchain",
        "Here's what makes {tech_detail} revolutionary:\n\nInstitutions finally have what they need. @DuskFoundation 💡",
    ],
    "engagement_bait": [
        "Reply with 🔥 if you're bullish on privacy-preserving RWAs\n\nBonus: Why or why not? 👇 #DUSK #RWA",
        "Quick poll:\n\nWhich matters more for institutional adoption?\n\n1️⃣ Privacy\n2️⃣ Speed\n3️⃣ Fees\n4️⃣ Compliance\n\nComment your take 👇 #DeFi",
        "Finish this: 'The biggest barrier to RWA adoption is _____'\n\nBest answer gets retweeted. #DUSK #Crypto",
        "Question for the real ones:\n\nWill transparent blockchains ever work for institutional securities?\n\nLet's discuss 🧵 #RWA",
        "Tag someone who needs to understand why {fact} matters for the future of finance. #Blockchain",
        "Hot or not: {statement}\n\nDefend your position 👇 #DeFi #Privacy",
        "GM! ☀️\n\nWhat's your biggest question about privacy-preserving blockchain?\n\nDrop it below 👇 @DuskFoundation #Web3",
    ],
    "fomo_urgency": [
        "RIGHT NOW: {fact}\n\nInstitutional DeFi is happening. Are you paying attention? 👀 #DUSK #RWA",
        "In 6 months everyone will wish they understood this today:\n\n{fact}\n\nYou're early. $DUSK #Crypto",
        "Since mainnet launch: {fact}\n\nThe revolution won't be televised. You're seeing it live. #DUSK #DeFi",
        "While you were sleeping: {fact}\n\nThe infrastructure is being built. Real. World. Assets. 🏗️ #Blockchain",
        "This week: {fact}\n\nNext week: More institutions onboarding.\n\nDon't miss what's happening. @DuskFoundation #RWA",
    ],
    "social_proof": [
        "Major milestone: {fact}\n\n$300M in real assets. Real custodians. Real adoption. $DUSK #RWA #TradFi",
        "Not hype, not vaporware: {fact}\n\nThis is what actual institutional blockchain looks like. #DeFi",
        "Talked to 3 institutions this week. All asking about the same thing: {advantage}\n\nGuess what they're building on? 👀 #DUSK",
        "When banks and exchanges choose privacy: {fact}\n\nActions speak louder than roadmaps. #Blockchain #TradFi",
        "Real numbers: {fact}\n\nThis is what mass adoption looks like. @DuskFoundation #Crypto #RWA",
    ],
    "problem_solution": [
        "The problem: {problem}\n\nThe solution: {advantage}\n\nThe blockchain: @DuskFoundation\n\n#RWA #DUSK #DeFi",
        "Institutions said: '{problem}'\n\nDusk said: 'Hold my ZK proofs' ✅ {fact} #Blockchain #Privacy",
        "Everyone: {problem}\n\nDusk: {tech_detail}\n\nThis is how you build for real adoption. #Web3 #TradFi",
        "Challenge: {problem}\n\nAnswer: {advantage}\n\nInfrastructure: $DUSK\n\nSimple as that. #RWA #Crypto",
    ],
    "paraphrase": [
        "{fact}\n\nThis is what the future of finance looks like. 🔮 #DeFi #RWA #DUSK",
        "GM to everyone building the future of regulated DeFi 🌅\n\n{fact}\n\n#Blockchain #Privacy",
        "Imagine: {advantage}\n\nYou don't have to imagine. It's live on @DuskFoundation. #Web3 #Crypto",
        "The market doesn't understand {fact} yet.\n\nThey will. 📈 #Crypto #RWA",
        "Quick reminder: {fact}\n\nMainnet is live. Institutions are building. The future is now. 🚀 #DUSK",
        "Everyone: 'When RWA adoption?'\n\n{fact}\n\nIt's already happening. #DuskNetwork #TradFi",
        "Can't stop thinking about {fact}\n\nThis changes everything for institutional adoption. 💡 #DeFi",
        "Not a drill: {fact}\n\n@DuskFoundation is rewriting the rules. #Blockchain #Privacy",
    ],
    "rwa_news": [
        "🚨 RWA Market Update:\n\n{rwa_fact}\n\nBut here's what they're missing: {problem}\n\n@DuskFoundation solves this. #RWA #Tokenization",
        "Breaking: {rwa_fact}\n\nNow imagine this with privacy + compliance.\n\nThat's what @DuskFoundation enables. #DeFi #RWA",
        "The numbers don't lie:\n\n{rwa_fact}\n\nThe question: Which chains can handle this privately?\n\nAnswer: 👀 #DUSK #TradFi",
        "Market insight: {rwa_fact}\n\nMost chains can't handle this level of institutional capital.\n\n@DuskFoundation was built for exactly this. #Blockchain #RWA",
        "{rwa_fact}\n\nMeanwhile, privacy-preserving infrastructure is being built for this exact use case. #DUSK #Tokenization",
        "Everyone's talking about: {rwa_fact}\n\nNobody's talking about the privacy problem.\n\nUntil now. @DuskFoundation #RWA #Privacy",
    ],
    "stablecoin_news": [
        "Stablecoin milestone: {stablecoin_fact}\n\nThe next evolution? Privacy-preserving stablecoins.\n\nDuskPay is coming. 💰 #Stablecoins #DUSK",
        "{stablecoin_fact}\n\nRegulation is here. Privacy is next.\n\n@DuskFoundation is ready. #MiCA #Stablecoins #Compliance",
        "📊 {stablecoin_fact}\n\nNow add:\n✅ Privacy\n✅ Compliance\n✅ Institutional-grade security\n\n= DuskPay #Crypto #Stablecoins",
        "Hot take: {stablecoin_fact}\n\nBut transparent stablecoins expose all your financial activity.\n\nPrivacy matters. @DuskFoundation #DeFi",
        "{stablecoin_fact}\n\nCompliance ✅\nAdoption ✅\nPrivacy ❌\n\nDusk is solving the last piece of the puzzle. #Stablecoins #Privacy",
    ],
    "tokenization_news": [
        "Tokenization update: {tokenization_fact}\n\nThis is massive. But it needs privacy to work at scale.\n\n@DuskFoundation 🔐 #Tokenization #RWA",
        "{tokenization_fact}\n\nProblem: Most chains can't offer both privacy AND regulatory compliance.\n\nSolution: @DuskFoundation #DeFi #Tokenization",
        "The future is here: {tokenization_fact}\n\nNext challenge: Making it private and compliant.\n\nDusk Network. #Blockchain #RWA",
        "{tokenization_fact}\n\nInstitutions need this + privacy.\n\nThat's why they're looking at @DuskFoundation. #Tokenization #TradFi",
        "Market trend: {tokenization_fact}\n\n2026 question: Which blockchain infrastructure will win?\n\nHint: Privacy + compliance wins. #DUSK #RWA",
        "Did you see? {tokenization_fact}\n\nThe race for compliant, privacy-preserving tokenization infrastructure is ON.\n\n@DuskFoundation leading. #DeFi",
    ],
}

# ============== THREAD TEMPLATES WITH REAL DUSK INFO ==============
THREAD_STARTERS = [
    {
        "tweets": [
            "🧵 Why Dusk Mainnet launch is bigger than you think (and why most people are sleeping on it)\n\n7 reasons this changes institutional RWAs:",
            "1/ Dusk is the FIRST blockchain where transactions are private but still auditable.\n\nInstitutions get confidentiality. Regulators get transparency. This seemed impossible. It's not.",
            "2/ Mainnet launched with $300M+ in real assets already tokenized via NPEX.\n\nNot testnet tokens. Real financial products from a regulated exchange. On-chain. Right now.",
            "3/ Hyperstaking unlocks programmable staking - like Account Abstraction but for stakes.\n\nPrivacy-preserving delegation, liquid staking, yield optimization. All possible because of this innovation.",
            "4/ Citadel solves KYC/AML without exposing personal data.\n\nZero-knowledge proofs let users prove compliance without revealing information. GDPR-friendly. MiCA-ready. Game-changer.",
            "5/ Custodian bank integration means institutions can actually use this.\n\nNot 'someday.' Not 'roadmap.' Happening now. Trust-minimized settlement with real custodians.",
            "6/ Compare to other RWA chains:\n\n❌ Transparent = Institutions won't touch it\n❌ Private but not auditable = Regulators say no\n✅ Dusk: Private + Auditable = Only viable path",
            "7/ 2025 roadmap: MiCA CEX, full on-chain settlement, EVM L2.\n\nThe infrastructure for regulated DeFi is being built. You're watching it happen.\n\nFollow @DuskFoundation for updates 🔔"
        ]
    },
    {
        "tweets": [
            "🧵 The technology that makes Dusk different (technical thread)\n\nHow zero-knowledge proofs unlock institutional blockchain:",
            "1/ PlonK proof system + Poseidon hash = State-of-the-art ZK cryptography\n\nThese aren't buzzwords. PlonK is highly efficient for generating and verifying proofs. Poseidon is optimized specifically for ZK circuits.",
            "2/ Succinct Attestation consensus - Proof of Stake with a twist\n\nAchieves complete state finality efficiently. Allows infinite scalability of verifiers. Original research from Dusk's co-founder.",
            "3/ Kadcast protocol makes block propagation 10x more efficient\n\nNovel approach to data distribution. Faster communication, better scalability. No bottlenecks even at high throughput.",
            "4/ Dusk VM - ZK-friendly virtual machine\n\nOptimized for privacy-preserving computations at scale. Handles ZK proofs efficiently. One-block sync. No state bloat.",
            "5/ The result: Privacy within a shared state\n\nNo other blockchain has achieved this. Private spending on public coins. Revolutionary nodes that support this architecture.",
            "6/ Why this matters for RWAs:\n\nInstitutions need confidentiality. Regulators need auditability. Public chains provide liquidity.\n\nDusk is the ONLY chain that delivers all three.",
            "7/ This isn't theoretical. Mainnet is live. NPEX is using it. Banks are integrating.\n\nThe future of regulated DeFi is being built on Dusk.\n\nLearn more: @DuskFoundation"
        ]
    },
    {
        "tweets": [
            "🧵 $300M milestone: What NPEX tokenization on Dusk means\n\nThis is bigger than most realize. Here's why:",
            "1/ NPEX is a REGULATED exchange - not some DeFi experiment\n\nThey manage $300M+ in traditional financial products. Now it's all tokenized on Dusk. On mainnet. Operating with real assets.",
            "2/ This proves institutional demand for privacy-preserving blockchain\n\nNPEX could have used any chain. They chose Dusk. Because confidentiality matters when you're dealing with real money.",
            "3/ Full DLT operations on a regulated exchange\n\nIssuance, clearance, settlement - all on-chain. This is what the future of finance looks like. Not roadmap. Reality.",
            "4/ MiCA compliance from day one\n\nAs MiCA regulations roll out, NPEX is already compliant. Using Citadel for privacy-preserving KYC/AML. Setting the standard.",
            "5/ This is just the beginning\n\nCustodian bank integrations coming. More institutions building. The flywheel is starting to spin.",
            "6/ Why this matters for $DUSK holders:\n\nReal usage. Real value accrual. Real institutional adoption.\n\nNot promises. Actual on-chain activity with real financial assets.",
            "7/ The question isn't IF institutions will tokenize assets.\n\nIt's WHERE they'll do it.\n\nNPEX answered: Dusk.\n\nWho's next? 👀"
        ]
    },
    {
        "tweets": [
            "🧵 Dusk 2025 Roadmap - What's shipping RIGHT NOW\n\nWhile others promise, Dusk delivers. Here's what's live & coming soon:",
            "1/ Mainnet launched January 7, 2025 🎉\n\nAfter 6 years of development, the first privacy-preserving blockchain for regulated finance is LIVE.\n\nReal users. Real transactions. Real privacy. #DUSK",
            "2/ DuskEVM - Ethereum compatibility meets privacy\n\nBuild with familiar EVM tools, deploy on a privacy-first L1. Ethereum devs can now build privacy-preserving dApps without learning new tech. #Web3",
            "3/ Lightspeed L2 - Best of both worlds\n\nEVM-compatible Layer 2 with Dusk settlement. Get Ethereum's ecosystem + Dusk's privacy. Interoperability without compromise. #Blockchain",
            "4/ DuskPay - Privacy-first payments\n\nIntegrated stablecoin payments for the entire ecosystem. Gaming, settlements, transactions - all private by default. Partnering with major stablecoin issuers. #Crypto",
            "5/ 21X Partnership - Institutional trading on-chain\n\nDusk is onboarded as a trade participant. Regulated exchange bringing TradFi onto blockchain. This is what institutional adoption looks like. #TradFi",
            "6/ Hyperstaking - Programmable staking\n\nLike Account Abstraction but for stakes. Custom logic, delegation, liquid staking, yield optimization. Revolutionary staking infrastructure. #DeFi",
            "7/ Citadel & Zedger - Privacy meets compliance\n\nZK KYC/AML + privacy-preserving asset issuance. MiCA-ready, GDPR-friendly, institution-approved. The complete infrastructure package. #RWA",
            "8/ What's next?\n\nCustodian bank integrations expanding. More institutions onboarding. EVM ecosystem growing.\n\nThe infrastructure for regulated DeFi is being built. Right now. @DuskFoundation 🚀"
        ]
    },
    {
        "tweets": [
            "🧵 The RWA Explosion: Why $35B is Just the Beginning\n\nRWA tokenization hit $35.78B in Nov 2025. But here's what most people miss about where this is headed:",
            "1/ The Numbers Don't Lie\n\nRWA market: $35.78B (Nov 2025)\nPrivate credit: ~$17B\nUS Treasuries: ~$7.3B\n\nBut projections say $16-30 TRILLION by 2030.\n\nThat's not a typo. #RWA #Tokenization",
            "2/ BlackRock Leads the Charge\n\nBUILD fund: $2.9B in tokenized US Treasuries\nMarket share: 44%\n\nWhen the world's largest asset manager goes all-in on tokenization, you pay attention. #TradFi #Crypto",
            "3/ From Pilots to Production\n\n2024: Banks ran pilots\n2025: Banks went LIVE\n\nJPMorgan, Franklin Templeton, UBS, KKR - all deploying capital into tokenized infrastructure.\n\nThis isn't experimentation anymore. #Blockchain",
            "4/ Real Utility Emerging\n\nDBS Bank now accepts Franklin Templeton's tokenized MMF as loan collateral.\n\nTokenized assets = Real financial utility\nNot just speculation. Actual TradFi use cases. #DeFi",
            "5/ The $230 Trillion Opportunity\n\nCurrently eligible collateral: $25T\nPotential collateral pool: $230T\n\nTokenization unlocks this trapped capital.\n\nImagine the liquidity. #RWA #Finance",
            "6/ The Privacy Problem\n\nBut here's what NO ONE is talking about:\n\nInstitutions can't tokenize $100M+ deals on transparent blockchains.\n\nConfidentiality isn't optional.\nIt's REQUIRED. #Privacy",
            "7/ Why Privacy-Preserving Chains Win\n\nTransparent chains ❌\n- Expose all deal terms\n- Violate GDPR\n- Enable front-running\n\nPrivacy + Compliance ✅\n- Confidential transactions\n- Regulatory audit trails\n- Institutional-grade security\n\n@DuskFoundation #DUSK",
            "8/ The Inevitable Conclusion\n\n$30T RWA market by 2030 needs:\n✅ Privacy\n✅ Compliance\n✅ Institutional security\n✅ Regulatory auditability\n\nOnly privacy-preserving blockchains can deliver all four.\n\nThe race is on. 🚀 #Blockchain #RWA"
        ]
    }
]

# ============== TARGET ACCOUNTS FOR ENGAGEMENT ==============
TARGET_ACCOUNTS = [
    "DuskFoundation",
    "RWA_xyz",
    "MessariCrypto",
    "OndoFinance",
    "Securitize",
    "polyx",
    "CentrifugeIO",
    "realworldx",
    "MakerDAO",
]

# ============== INITIALIZE ==============
def init_twitter():
    """Initialize Twitter API client with credentials from environment variables"""
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET, BEARER_TOKEN]):
        raise ValueError("Missing required Twitter API credentials in environment variables")

    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_SECRET,
        wait_on_rate_limit=True
    )
    return client

def load_analytics():
    """Load analytics data from JSON file"""
    try:
        with open(ANALYTICS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"total_tweets": 0, "start_date": datetime.now().isoformat()}

def save_analytics(data):
    """Save analytics data to JSON file"""
    with open(ANALYTICS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ============== TWEET GENERATION ==============
def generate_tweet(category=None):
    """Generate a tweet from templates and content pools (optimized for max reach)"""
    if category is None:
        categories = list(TWEET_TEMPLATES.keys())
        # Optimized weights for maximum engagement and reach
        weights = {
            "engagement_bait": 0.20,    # High engagement drives reach
            "rwa_news": 0.15,           # Timely RWA market news
            "paraphrase": 0.15,         # Authentic, shareable content
            "hot_takes": 0.15,          # Controversial = viral potential
            "dusk_milestones": 0.12,    # News-worthy content
            "tokenization_news": 0.10,  # Tokenization trends
            "stablecoin_news": 0.05,    # Stablecoin market updates
            "education_tech": 0.05,     # Educational value
            "fomo_urgency": 0.02,       # Urgency drives action
            "social_proof": 0.01,       # Credibility
            "problem_solution": 0.00,   # Value-add (handled by others)
        }
        category = random.choices(categories, weights=[weights.get(c, 0.01) for c in categories])[0]

    template = random.choice(TWEET_TEMPLATES[category])

    tweet = template.format(
        fact=random.choice(DUSK_FACTS),
        tech_detail=random.choice(DUSK_TECH_DETAILS),
        problem=random.choice(INSTITUTIONAL_PROBLEMS),
        advantage=random.choice(DUSK_ADVANTAGES),
        rwa_fact=random.choice(RWA_MARKET_FACTS),
        stablecoin_fact=random.choice(STABLECOIN_FACTS),
        tokenization_fact=random.choice(TOKENIZATION_TRENDS),
        statement=random.choice([
            "Privacy isn't optional for institutional RWAs",
            "Transparent blockchains can't handle real securities",
            "Without ZK tech, institutional tokenization is dead on arrival",
            "MiCA compliance will separate the real projects from vaporware",
            "TradFi needs DeFi privacy - not transparency"
        ])
    )

    return tweet, category

# ============== THREAD POSTING ==============
def post_thread(client, thread_tweets):
    """Post a thread of tweets as a conversation"""
    tweet_ids = []
    previous_id = None

    for i, tweet_text in enumerate(thread_tweets):
        try:
            if previous_id:
                response = client.create_tweet(text=tweet_text, in_reply_to_tweet_id=previous_id)
            else:
                response = client.create_tweet(text=tweet_text)

            tweet_ids.append(response.data['id'])
            previous_id = response.data['id']
            print(f"  ✓ Thread {i+1}/{len(thread_tweets)} posted")
            time.sleep(3)

        except Exception as e:
            print(f"  ✗ Error on thread tweet {i+1}: {e}")
            break

    return tweet_ids

# ============== ENGAGEMENT ==============
def engage_with_targets(client, limit=5):
    """Engage with target accounts by liking and occasionally retweeting"""
    print("🤝 Engaging with target accounts...")

    for username in random.sample(TARGET_ACCOUNTS, min(3, len(TARGET_ACCOUNTS))):
        try:
            user = client.get_user(username=username)
            if not user.data:
                continue

            tweets = client.get_users_tweets(user.data.id, max_results=5)
            if not tweets.data:
                continue

            tweet = tweets.data[0]

            try:
                client.like(tweet.id)
                print(f"  ✓ Liked @{username}'s tweet")
            except:
                pass

            if random.random() < 0.15:
                try:
                    client.retweet(tweet.id)
                    print(f"  ✓ Retweeted @{username}")
                except:
                    pass

            time.sleep(5)

        except Exception as e:
            print(f"  ⚠️ Skipped @{username}")

    print("✓ Engagement complete\n")

# ============== SCHEDULING (Optimized for Maximum Reach) ==============
def create_schedule(num_posts=20):
    """Create a posting schedule optimized for engagement and reach

    Peak Twitter hours for crypto/tech audience (UTC):
    - Morning: 7-9 AM (US waking up, EU afternoon)
    - Lunch: 12-2 PM (Global lunch break)
    - Evening: 6-9 PM (US peak, EU evening)
    """
    # Peak engagement times (hours in UTC)
    peak_hours = [7, 8, 12, 13, 18, 19, 20]
    good_hours = [9, 10, 14, 15, 16, 21, 22]
    schedule = []

    # Thread times at peak engagement (morning and evening)
    thread_times = [(8, 30, "thread"), (19, 0, "thread")]
    regular_needed = num_posts - 2

    # Prioritize peak hours (3-4 posts)
    for hour in peak_hours:
        if len(schedule) >= regular_needed:
            break
        minute = random.choice([0, 15, 30, 45])  # Scheduled times for consistency
        schedule.append((hour, minute, "regular"))

    # Fill remaining slots in good hours
    for hour in good_hours:
        if len(schedule) >= regular_needed:
            break
        minute = random.choice([10, 25, 40, 55])
        schedule.append((hour, minute, "regular"))

    # Add any remaining posts distributed throughout the day
    remaining_hours = [h for h in range(24) if h not in peak_hours + good_hours]
    while len(schedule) < regular_needed:
        hour = random.choice(remaining_hours)
        minute = random.randint(0, 59)
        schedule.append((hour, minute, "regular"))

    schedule.extend(thread_times)
    return sorted(schedule, key=lambda x: (x[0], x[1]))

# ============== MAIN POSTING ==============
def run_bot(client, num_posts=20):
    """Main bot execution loop (default: 20 posts/day for maximum reach)"""
    schedule = create_schedule(num_posts)
    analytics = load_analytics()

    print("=" * 60)
    print("🚀 DUSK TWITTER BOT - LIVE MODE")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"📊 Total historical tweets: {analytics['total_tweets']}")
    print(f"📝 Scheduled today: {len(schedule)} posts")
    print("=" * 60)

    posted_count = 0

    for hour, minute, post_type in schedule:
        now = datetime.now()
        post_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        if post_time < now:
            print(f"⏭️  Skipped {hour:02d}:{minute:02d} (already passed)")
            continue

        wait_seconds = (post_time - now).total_seconds()

        if wait_seconds > 0:
            print(f"\n⏳ Waiting {wait_seconds/60:.1f} min until {post_time.strftime('%H:%M')}...")
            time.sleep(wait_seconds)

        print(f"\n[{datetime.now().strftime('%H:%M:%S')}]", end=" ")

        if post_type == "thread":
            thread = random.choice(THREAD_STARTERS)
            try:
                tweet_ids = post_thread(client, thread["tweets"])
                print(f"✅ THREAD posted ({len(tweet_ids)} tweets)")
                posted_count += len(tweet_ids)
            except Exception as e:
                print(f"❌ Thread failed: {e}")
        else:
            tweet, category = generate_tweet()
            try:
                response = client.create_tweet(text=tweet)
                print(f"✅ [{category}] Posted")
                posted_count += 1

                if posted_count % 5 == 0:
                    engage_with_targets(client)

            except Exception as e:
                print(f"❌ Error: {e}")

        time.sleep(random.randint(30, 90))

    analytics["total_tweets"] += posted_count
    analytics["last_run"] = datetime.now().isoformat()
    save_analytics(analytics)

    print("\n" + "=" * 60)
    print(f"✅ SESSION COMPLETE")
    print(f"📊 Posted: {posted_count} times today")
    print(f"📈 Total all-time: {analytics['total_tweets']}")
    print("=" * 60)

# ============== CLI ==============
def main():
    """Main entry point for the bot"""
    print("\n" + "=" * 60)
    print("  DUSK NETWORK TWITTER GROWTH BOT")
    print("  Full automation with real Dusk content")
    print("=" * 60)

    if len(sys.argv) > 1 and sys.argv[1] == "preview":
        print("\n📝 PREVIEW MODE - Sample content:\n")
        for i in range(5):
            tweet, cat = generate_tweet()
            print(f"{i+1}. [{cat.upper()}]")
            print(f"{tweet}\n")
        print("Sample thread:")
        for i, t in enumerate(THREAD_STARTERS[0]["tweets"][:3], 1):
            print(f"{i}. {t}\n")
        return

    try:
        client = init_twitter()
        print("\n✅ Twitter API connected")
        print("🚀 Starting automated posting...\n")

        run_bot(client, num_posts=20)

    except KeyboardInterrupt:
        print("\n\n⚠️  Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
