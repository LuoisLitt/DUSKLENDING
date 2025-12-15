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

# ============== REAL DUSK CONTENT ==============
DUSK_FACTS = [
    "Dusk mainnet is LIVE - the first privacy-preserving blockchain for regulated finance",
    "Hyperstaking on Dusk allows smart contracts to implement custom staking logic - like Account Abstraction for staking",
    "Zedger protocol focuses on privacy-preserving compliant asset tokenization and management",
    "NPEX has tokenized $300M+ in assets on Dusk - real world financial products on-chain",
    "Citadel is Dusk's ZK-powered KYC/AML tool that reconciles privacy with regulatory compliance",
    "Dusk uses PlonK proof system and Poseidon hash - the most advanced ZK cryptography available",
    "Succinct Attestation consensus allows infinite scalability of verifiers on Dusk",
    "Kadcast makes block propagation 10x more efficient than conventional blockchain methods",
    "Dusk VM is a ZK-friendly virtual machine that handles privacy computations at scale",
    "Transactions on Dusk are private but auditable - institutions get confidentiality AND compliance",
    "Dusk is MiCA-ready and integrating with custodian banks for institutional regulated finance",
    "Privacy within a shared state - what no other blockchain has achieved",
    "One-block sync to network, no state bloat, web wallet with ZKP computations in-browser",
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
]

INSTITUTIONAL_PROBLEMS = [
    "Institutions can't put $100M+ deals on transparent blockchains - they need confidentiality",
    "Regulators demand auditability but privacy seems impossible - Dusk solves both",
    "Traditional blockchains expose all transaction data - deal-breaker for real finance",
    "KYC/AML creates friction while blockchain transparency violates GDPR",
    "MEV and front-running make public chains unsuitable for institutional trading",
]

DUSK_ADVANTAGES = [
    "Private transactions that regulators can still audit - the only way forward",
    "MiCA compliance baked into the protocol from day one",
    "Custodian bank integration for trust-minimized clearance and settlement",
    "$300M+ in real assets already tokenized on mainnet via NPEX",
    "Full on-chain issuance, clearance & settlement - the complete solution",
    "Privacy without sacrificing the unified liquidity of public blockchains",
]

# ============== ENHANCED TWEET TEMPLATES ==============
TWEET_TEMPLATES = {
    "hot_takes": [
        "Unpopular opinion: {statement}\n\nMost RWA projects will fail because of this. #DUSK #RWA",
        "Everyone is building 'RWA chains' but missing the obvious: {problem}\n\n@DuskFoundation gets it.",
        "Hot take: Transparent blockchains for securities = DOA\n\n{fact}\n\nThis is why $DUSK is different.",
        "While everyone talks about tokenization, {fact}\n\nThis changes everything. #RWA",
        "Controversial but true: 90% of RWA projects can't handle real institutional capital.\n\nWhy? {problem}",
    ],
    "dusk_milestones": [
        "🚨 MAINNET MILESTONE: {fact}\n\nThis is what real institutional blockchain looks like. $DUSK",
        "Major @DuskFoundation update: {fact}\n\nThe infrastructure for regulated DeFi is here.",
        "While other chains talk, Dusk delivers: {fact}\n\nReal adoption, real assets, real privacy.",
        "Game-changing tech: {tech_detail}\n\nOnly possible on @DuskFoundation. #Privacy #Compliance",
        "From zero to hero: {fact}\n\n2025 is Dusk's year. Don't say you weren't told. $DUSK",
    ],
    "education_tech": [
        "🧵 Let's talk about {tech_detail}\n\nThis is the unlock for institutional RWAs:",
        "Privacy vs Compliance - the false dilemma.\n\n{fact}\n\nProblem solved. #DUSK",
        "Why institutions need privacy: {problem}\n\nHow Dusk solves it: {advantage}",
        "Tech breakdown: {tech_detail}\n\nThis is why $DUSK is built different from other L1s.",
        "Real talk about RWA infrastructure: {fact}\n\nNot speculation. Real working tech.",
    ],
    "engagement_bait": [
        "Reply with 🔥 if you're bullish on privacy-preserving RWAs\n\nBonus: Why or why not? 👇",
        "Quick poll:\n\nWhich matters more for institutional adoption?\n\n1️⃣ Privacy\n2️⃣ Speed\n3️⃣ Fees\n4️⃣ Compliance\n\nComment your take 👇",
        "Finish this: 'The biggest barrier to RWA adoption is _____'\n\nBest answer gets retweeted. #DUSK",
        "Question for the real ones:\n\nWill transparent blockchains ever work for institutional securities?\n\nLet's discuss 🧵",
        "Tag someone who needs to understand why {fact} matters for the future of finance.",
        "Hot or not: {statement}\n\nDefend your position 👇",
    ],
    "fomo_urgency": [
        "RIGHT NOW: {fact}\n\nInstitutional DeFi is happening. Are you paying attention?",
        "In 6 months everyone will wish they understood this today:\n\n{fact}\n\nYou're early. $DUSK",
        "48 hours since mainnet launch and {fact}\n\nThe revolution won't be televised. #DUSK",
        "While you were sleeping: {fact}\n\nThe infrastructure is being built. Real. World. Assets.",
        "This week: {fact}\n\nNext week: More institutions onboarding.\n\nDon't miss what's happening. @DuskFoundation",
    ],
    "social_proof": [
        "Major milestone: {fact}\n\n$300M in real assets. Real custodians. Real adoption. $DUSK",
        "Not hype, not vaporware: {fact}\n\nThis is what actual institutional blockchain looks like.",
        "Talked to 3 institutions this week. All asking about the same thing: {advantage}\n\nGuess what they're building on? 👀",
        "When banks and exchanges choose privacy: {fact}\n\nActions speak louder than roadmaps.",
    ],
    "problem_solution": [
        "The problem: {problem}\n\nThe solution: {advantage}\n\nThe blockchain: @DuskFoundation\n\n#RWA #DUSK",
        "Institutions said: '{problem}'\n\nDusk said: 'Hold my ZK proofs' ✅ {fact}",
        "Everyone: {problem}\n\nDusk: {tech_detail}\n\nThis is how you build for real adoption.",
        "Challenge: {problem}\n\nAnswer: {advantage}\n\nInfrastructure: $DUSK\n\nSimple as that.",
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
    """Generate a tweet from templates and content pools"""
    if category is None:
        categories = list(TWEET_TEMPLATES.keys())
        weights = {
            "hot_takes": 0.20,
            "engagement_bait": 0.20,
            "dusk_milestones": 0.20,
            "education_tech": 0.15,
            "fomo_urgency": 0.10,
            "social_proof": 0.08,
            "problem_solution": 0.07,
        }
        category = random.choices(categories, weights=[weights.get(c, 0.01) for c in categories])[0]

    template = random.choice(TWEET_TEMPLATES[category])

    tweet = template.format(
        fact=random.choice(DUSK_FACTS),
        tech_detail=random.choice(DUSK_TECH_DETAILS),
        problem=random.choice(INSTITUTIONAL_PROBLEMS),
        advantage=random.choice(DUSK_ADVANTAGES),
        statement=random.choice([
            "Privacy isn't optional for institutional RWAs",
            "Transparent blockchains can't handle real securities",
            "Without ZK tech, institutional tokenization is dead on arrival"
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

# ============== SCHEDULING ==============
def create_schedule(num_posts=30):
    """Create a posting schedule for the day"""
    prime_hours = [8, 10, 12, 14, 16, 18, 20, 22]
    schedule = []

    # Reserve slots for threads
    thread_times = [(10, 0, "thread"), (19, 30, "thread")]
    regular_needed = num_posts - 2

    for hour in range(24):
        if hour in prime_hours:
            num_in_hour = min(2, regular_needed - len(schedule))
        else:
            num_in_hour = 1 if len(schedule) < regular_needed else 0

        for _ in range(num_in_hour):
            if len(schedule) >= regular_needed:
                break
            minute = random.randint(0, 59)
            schedule.append((hour, minute, "regular"))

    schedule.extend(thread_times)
    return sorted(schedule, key=lambda x: (x[0], x[1]))

# ============== MAIN POSTING ==============
def run_bot(client, num_posts=30):
    """Main bot execution loop"""
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

        run_bot(client, num_posts=30)

    except KeyboardInterrupt:
        print("\n\n⚠️  Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
