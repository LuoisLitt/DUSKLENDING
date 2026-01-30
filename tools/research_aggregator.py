#!/usr/bin/env python3
"""
Dusk Network Research Aggregator
=================================
Searches for trending content around tokenization, privacy, and institutional
crypto adoption, then compiles a briefing with Dusk-relevant talking points.

Usage:
    python3 tools/research_aggregator.py                # Full briefing (all topics)
    python3 tools/research_aggregator.py --topic privacy # Single topic
    python3 tools/research_aggregator.py --trending      # Crypto trends only
    python3 tools/research_aggregator.py --json          # Output as JSON
    python3 tools/research_aggregator.py --save          # Save to file in tools/briefings/

No API keys required. Uses public RSS feeds + web scraping.
"""

import argparse
import hashlib
import json
import os
import random
import re
import sys
import textwrap
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote_plus, urlparse

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SEARCH_CATEGORIES = {
    "tokenization": {
        "label": "Tokenization & RWA",
        "terms": [
            "tokenization real world assets blockchain",
            "RWA tokenization securities",
            "security token offering 2025 2026",
            "on-chain securities settlement",
            "tokenized bonds equities blockchain",
            "digital securities regulation",
            "MiCA tokenization compliance",
            "DLT pilot regime securities",
            "tokenized assets institutional",
            "blockchain securities exchange",
        ],
        "dusk_angle": (
            "$DUSK is purpose-built for regulated tokenization. "
            "NPEX (licensed Dutch exchange) is deploying on DuskEVM to tokenize "
            "€200M+ in equities and bonds under MTF, ECSP and broker-dealer licences. "
            "The XSC token standard embeds regulatory rules directly into assets."
        ),
    },
    "privacy": {
        "label": "Privacy & Zero-Knowledge",
        "terms": [
            "zero knowledge proof blockchain finance",
            "privacy preserving blockchain compliance",
            "confidential transactions regulation",
            "ZK proof institutional adoption",
            "privacy blockchain KYC AML",
            "GDPR blockchain privacy",
            "selective disclosure blockchain",
            "shielded transactions compliant",
            "zero knowledge identity verification",
            "privacy DeFi regulated",
        ],
        "dusk_angle": (
            "$DUSK uses dual transaction models: Phoenix (shielded/UTXO) and "
            "Moonlight (transparent/account-based). Citadel provides ZK-based "
            "KYC/AML — privacy-preserving identity that satisfies GDPR, MiCA, "
            "and MiFID II without exposing user data on-chain."
        ),
    },
    "institutions": {
        "label": "Institutional Adoption",
        "terms": [
            "institutional crypto adoption 2025 2026",
            "banks blockchain adoption",
            "institutional DeFi regulated",
            "traditional finance blockchain integration",
            "enterprise blockchain settlement",
            "financial institutions digital assets",
            "regulated DeFi institutional",
            "blockchain capital markets",
            "on-chain settlement finality",
            "ETF tokenization blockchain",
        ],
        "dusk_angle": (
            "$DUSK is the only L1 where the entire chain operates under a "
            "regulatory umbrella via NPEX's MTF, ECSP and broker licences. "
            "Succinct Attestation consensus provides deterministic finality — "
            "critical for institutional settlement. Chainlink CCIP integration "
            "enables cross-chain composability for tokenized securities."
        ),
    },
    "trending": {
        "label": "Crypto Trends",
        "terms": [
            "crypto news today",
            "blockchain latest developments",
            "DeFi trending news",
            "cryptocurrency regulation update",
            "Web3 latest news",
            "crypto market analysis",
            "Layer 1 blockchain comparison",
            "crypto institutional news",
        ],
        "dusk_angle": (
            "$DUSK launched mainnet in January 2025 after 6 years of development. "
            "Key 2026 milestones: cross-chain bridge deployment, NPEX dApp integration, "
            "DuskPay B2B settlement platform, and Hyperstaking for programmable staking."
        ),
    },
}

# Dusk knowledge base for generating relevant talking points
DUSK_KNOWLEDGE = {
    "overview": (
        "Dusk is a privacy-focused Layer-1 blockchain for regulated financial markets. "
        "It enables institutions to launch and operate markets while maintaining compliance, "
        "user confidentiality, and execution speed."
    ),
    "privacy_tech": (
        "Phoenix provides shielded UTXO transactions; Moonlight provides transparent "
        "account-based transactions. Users choose per transaction. Citadel enables "
        "ZK-based KYC/AML — proving compliance without revealing personal data."
    ),
    "consensus": (
        "Succinct Attestation: permissionless committee-based PoS with 3 phases "
        "(Proposal, Validation, Ratification). Delivers deterministic finality "
        "suitable for financial settlement — no reorgs under normal conditions."
    ),
    "architecture": (
        "DuskDS handles consensus, settlement and privacy. DuskEVM is a fully "
        "EVM-equivalent execution layer (OP Stack + EIP-4844). DuskVM is a "
        "ZK-friendly WASM virtual machine for privacy smart contracts."
    ),
    "npex": (
        "NPEX is a licensed Dutch stock exchange (MTF + ECSP + broker licences from AFM). "
        "Deploying on DuskEVM to tokenize €200M+ in equities and bonds. "
        "Licences extend to the entire chain — every Dusk app gains regulatory coverage."
    ),
    "chainlink": (
        "Chainlink CCIP for cross-chain transfers of tokenized assets. "
        "Chainlink DataLink for on-chain NPEX market data. "
        "Chainlink Data Streams for low-latency price feeds."
    ),
    "tokenomics": (
        "Fixed supply of 500M $DUSK tokens. 36-year emission schedule with "
        "4-year reduction cycles. MiCA-compliant tokenomics design."
    ),
    "2026_roadmap": (
        "Q1 2026: Two-way cross-chain bridge. 2026: NPEX dApp on DuskEVM, "
        "DuskPay B2B settlement, Hyperstaking for programmable staking logic."
    ),
    "zedger": (
        "Zedger Asset Protocol: privacy-preserving compliant asset tokenization, "
        "issuance, clearance and settlement. Full on-chain lifecycle management."
    ),
    "regulations": (
        "Built for MiCA, MiFID II, DORA, GDPR, and DLT Pilot Regime compliance. "
        "Only blockchain with protocol-level regulatory umbrella via licensed exchange."
    ),
}

# RSS feed sources for crypto news
RSS_FEEDS = [
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("CoinTelegraph", "https://cointelegraph.com/rss"),
    ("The Block", "https://www.theblock.co/rss.xml"),
    ("Decrypt", "https://decrypt.co/feed"),
    ("CryptoSlate", "https://cryptoslate.com/feed/"),
    ("Bitcoin Magazine", "https://bitcoinmagazine.com/feed"),
]

# Google News RSS search
GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

# Cache directory
CACHE_DIR = Path(__file__).parent / ".cache"
BRIEFING_DIR = Path(__file__).parent / "briefings"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------


def cache_key(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


def fetch_cached(url: str, max_age_hours: int = 2) -> str | None:
    """Fetch URL with simple file-based cache."""
    CACHE_DIR.mkdir(exist_ok=True)
    path = CACHE_DIR / cache_key(url)

    if path.exists():
        age = time.time() - path.stat().st_mtime
        if age < max_age_hours * 3600:
            return path.read_text(encoding="utf-8", errors="replace")

    try:
        resp = SESSION.get(url, timeout=15)
        resp.raise_for_status()
        text = resp.text
        path.write_text(text, encoding="utf-8")
        return text
    except Exception as e:
        print(f"  [warn] Could not fetch {url}: {e}", file=sys.stderr)
        return None


def parse_rss(xml_text: str) -> list[dict]:
    """Parse RSS/Atom feed XML into list of items."""
    items = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items

    # Standard RSS
    for item in root.iter("item"):
        entry = {}
        title_el = item.find("title")
        link_el = item.find("link")
        desc_el = item.find("description")
        pub_el = item.find("pubDate")

        if title_el is not None and title_el.text:
            entry["title"] = clean_html(title_el.text.strip())
        if link_el is not None and link_el.text:
            entry["link"] = link_el.text.strip()
        if desc_el is not None and desc_el.text:
            entry["description"] = clean_html(desc_el.text.strip())[:300]
        if pub_el is not None and pub_el.text:
            entry["published"] = pub_el.text.strip()

        if "title" in entry:
            items.append(entry)

    # Atom fallback
    if not items:
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        for entry_el in root.findall(".//atom:entry", ns):
            entry = {}
            title_el = entry_el.find("atom:title", ns)
            link_el = entry_el.find("atom:link", ns)
            summary_el = entry_el.find("atom:summary", ns)

            if title_el is not None and title_el.text:
                entry["title"] = clean_html(title_el.text.strip())
            if link_el is not None:
                entry["link"] = link_el.get("href", "")
            if summary_el is not None and summary_el.text:
                entry["description"] = clean_html(summary_el.text.strip())[:300]

            if "title" in entry:
                items.append(entry)

    return items


def clean_html(text: str) -> str:
    """Remove HTML tags from text."""
    return re.sub(r"<[^>]+>", "", text).strip()


def relevance_score(text: str, keywords: list[str]) -> int:
    """Score how relevant a text is to given keywords."""
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw.lower() in text_lower)


def pick_dusk_angle(article_title: str, article_desc: str) -> str:
    """Pick the most relevant Dusk talking point for a given article."""
    combined = (article_title + " " + (article_desc or "")).lower()

    scoring = {
        "privacy_tech": ["privacy", "zero knowledge", "zk", "confidential", "shielded", "gdpr"],
        "npex": ["npex", "exchange", "securities", "equities", "bonds", "mtf", "licensed"],
        "chainlink": ["chainlink", "cross-chain", "interoperability", "oracle", "ccip"],
        "consensus": ["consensus", "finality", "settlement", "pos", "proof of stake"],
        "architecture": ["evm", "layer-1", "l1", "virtual machine", "wasm", "smart contract"],
        "tokenomics": ["tokenomics", "supply", "emission", "staking reward"],
        "2026_roadmap": ["roadmap", "2026", "bridge", "duskpay", "hyperstaking"],
        "zedger": ["issuance", "asset protocol", "clearance", "lifecycle"],
        "regulations": ["regulation", "mica", "mifid", "compliance", "kyc", "aml", "dora"],
        "overview": ["blockchain", "defi", "crypto", "institutional", "tokenization", "rwa"],
    }

    best_key = "overview"
    best_score = 0
    for key, terms in scoring.items():
        score = sum(1 for t in terms if t in combined)
        if score > best_score:
            best_score = score
            best_key = key

    return DUSK_KNOWLEDGE[best_key]


# ---------------------------------------------------------------------------
# Data Collection
# ---------------------------------------------------------------------------


def search_google_news(query: str, max_results: int = 5) -> list[dict]:
    """Search Google News RSS for a query."""
    url = GOOGLE_NEWS_RSS.format(query=quote_plus(query))
    xml = fetch_cached(url, max_age_hours=1)
    if not xml:
        return []
    items = parse_rss(xml)
    return items[:max_results]


def fetch_rss_feeds(max_per_feed: int = 10) -> list[dict]:
    """Fetch articles from curated crypto RSS feeds."""
    all_items = []
    for name, url in RSS_FEEDS:
        xml = fetch_cached(url, max_age_hours=2)
        if not xml:
            continue
        items = parse_rss(xml)
        for item in items[:max_per_feed]:
            item["source"] = name
        all_items.extend(items[:max_per_feed])
    return all_items


def collect_topic_articles(category: str, max_searches: int = 3) -> list[dict]:
    """Collect articles for a given topic category by rotating search terms."""
    config = SEARCH_CATEGORIES.get(category)
    if not config:
        return []

    terms = config["terms"][:]
    random.shuffle(terms)
    selected_terms = terms[:max_searches]

    all_articles = []
    seen_titles = set()

    for term in selected_terms:
        print(f"  Searching: {term}", file=sys.stderr)
        articles = search_google_news(term, max_results=5)
        for article in articles:
            title_hash = article.get("title", "").lower().strip()
            if title_hash not in seen_titles:
                seen_titles.add(title_hash)
                article["search_term"] = term
                article["category"] = category
                all_articles.append(article)

    return all_articles


def collect_trending() -> list[dict]:
    """Collect trending crypto articles from RSS feeds and filter for relevance."""
    print("  Fetching RSS feeds...", file=sys.stderr)
    articles = fetch_rss_feeds(max_per_feed=8)

    # Score and filter for relevance to our focus topics
    priority_keywords = [
        "tokenization", "rwa", "real world asset", "privacy", "zero knowledge",
        "institutional", "regulation", "compliance", "securities", "defi",
        "settlement", "custody", "exchange", "etf", "stablecoin", "mica",
        "cbdc", "digital asset", "layer 1", "l1", "blockchain", "dusk",
    ]

    for article in articles:
        text = article.get("title", "") + " " + article.get("description", "")
        article["relevance"] = relevance_score(text, priority_keywords)

    articles.sort(key=lambda a: a.get("relevance", 0), reverse=True)
    return articles[:20]


# ---------------------------------------------------------------------------
# Briefing Generation
# ---------------------------------------------------------------------------


def generate_briefing(topics: list[str] | None = None, include_trending: bool = True) -> dict:
    """Generate a full research briefing."""
    if topics is None:
        topics = ["tokenization", "privacy", "institutions"]

    briefing = {
        "generated_at": datetime.now().isoformat(),
        "topics": {},
        "trending": [],
        "dusk_knowledge": DUSK_KNOWLEDGE,
    }

    # Topic-specific research
    for topic in topics:
        if topic not in SEARCH_CATEGORIES:
            continue
        print(f"\n[{SEARCH_CATEGORIES[topic]['label']}]", file=sys.stderr)
        articles = collect_topic_articles(topic, max_searches=3)

        enriched = []
        for article in articles:
            article["dusk_angle"] = pick_dusk_angle(
                article.get("title", ""),
                article.get("description", ""),
            )
            enriched.append(article)

        briefing["topics"][topic] = {
            "label": SEARCH_CATEGORIES[topic]["label"],
            "category_angle": SEARCH_CATEGORIES[topic]["dusk_angle"],
            "articles": enriched,
        }

    # Trending articles
    if include_trending:
        print("\n[Trending Crypto]", file=sys.stderr)
        trending = collect_trending()
        for article in trending:
            article["dusk_angle"] = pick_dusk_angle(
                article.get("title", ""),
                article.get("description", ""),
            )
        briefing["trending"] = trending

    return briefing


def format_briefing_text(briefing: dict) -> str:
    """Format briefing as readable text."""
    lines = []
    lines.append("=" * 72)
    lines.append("  DUSK NETWORK — RESEARCH BRIEFING")
    lines.append(f"  Generated: {briefing['generated_at']}")
    lines.append("=" * 72)

    for topic_key, topic_data in briefing.get("topics", {}).items():
        lines.append("")
        lines.append(f"{'─' * 72}")
        lines.append(f"  {topic_data['label'].upper()}")
        lines.append(f"{'─' * 72}")
        lines.append("")
        lines.append(f"  $DUSK Angle: {topic_data['category_angle']}")
        lines.append("")

        articles = topic_data.get("articles", [])
        if not articles:
            lines.append("  No articles found for this topic.")
            continue

        for i, article in enumerate(articles, 1):
            lines.append(f"  [{i}] {article.get('title', 'Untitled')}")
            if article.get("link"):
                lines.append(f"      Link: {article['link']}")
            if article.get("description"):
                desc = textwrap.fill(article["description"], width=64, initial_indent="      ", subsequent_indent="      ")
                lines.append(desc)
            if article.get("search_term"):
                lines.append(f"      Found via: \"{article['search_term']}\"")
            lines.append(f"      $DUSK Talking Point: {article.get('dusk_angle', 'N/A')}")
            lines.append("")

    # Trending section
    trending = briefing.get("trending", [])
    if trending:
        lines.append(f"{'─' * 72}")
        lines.append("  TRENDING CRYPTO NEWS (sorted by relevance)")
        lines.append(f"{'─' * 72}")
        lines.append("")

        for i, article in enumerate(trending[:15], 1):
            rel = article.get("relevance", 0)
            source = article.get("source", "Unknown")
            lines.append(f"  [{i}] [{source}] (relevance: {rel}) {article.get('title', 'Untitled')}")
            if article.get("link"):
                lines.append(f"      Link: {article['link']}")
            if article.get("description"):
                desc = textwrap.fill(article["description"], width=64, initial_indent="      ", subsequent_indent="      ")
                lines.append(desc)
            lines.append(f"      $DUSK Talking Point: {article.get('dusk_angle', 'N/A')}")
            lines.append("")

    # Dusk quick reference
    lines.append(f"{'─' * 72}")
    lines.append("  DUSK QUICK REFERENCE (for crafting replies)")
    lines.append(f"{'─' * 72}")
    lines.append("")
    for key, value in DUSK_KNOWLEDGE.items():
        label = key.replace("_", " ").title()
        wrapped = textwrap.fill(value, width=64, initial_indent=f"  {label}: ", subsequent_indent="    ")
        lines.append(wrapped)
        lines.append("")

    lines.append("=" * 72)
    lines.append("  END OF BRIEFING")
    lines.append("=" * 72)

    return "\n".join(lines)


def format_briefing_json(briefing: dict) -> str:
    """Format briefing as JSON."""
    return json.dumps(briefing, indent=2, default=str)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Dusk Network Research Aggregator — daily briefing tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python3 tools/research_aggregator.py                  # Full briefing
              python3 tools/research_aggregator.py --topic privacy  # Single topic
              python3 tools/research_aggregator.py --trending       # Trends only
              python3 tools/research_aggregator.py --json --save    # Save JSON briefing
              python3 tools/research_aggregator.py --clear-cache    # Clear cached results
        """),
    )
    parser.add_argument(
        "--topic",
        choices=["tokenization", "privacy", "institutions", "trending"],
        help="Focus on a single topic instead of all",
    )
    parser.add_argument(
        "--trending",
        action="store_true",
        help="Only show trending crypto news",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON instead of formatted text",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save briefing to tools/briefings/ directory",
    )
    parser.add_argument(
        "--searches-per-topic",
        type=int,
        default=3,
        help="Number of search term rotations per topic (default: 3)",
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear the cache and exit",
    )

    args = parser.parse_args()

    if args.clear_cache:
        if CACHE_DIR.exists():
            import shutil
            shutil.rmtree(CACHE_DIR)
            print("Cache cleared.", file=sys.stderr)
        else:
            print("No cache to clear.", file=sys.stderr)
        return

    # Determine topics
    if args.trending:
        topics = []
        include_trending = True
    elif args.topic:
        if args.topic == "trending":
            topics = []
            include_trending = True
        else:
            topics = [args.topic]
            include_trending = False
    else:
        topics = ["tokenization", "privacy", "institutions"]
        include_trending = True

    print("Generating research briefing...\n", file=sys.stderr)
    briefing = generate_briefing(topics=topics, include_trending=include_trending)

    if args.json:
        output = format_briefing_json(briefing)
    else:
        output = format_briefing_text(briefing)

    print(output)

    if args.save:
        BRIEFING_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        ext = "json" if args.json else "txt"
        filepath = BRIEFING_DIR / f"briefing_{timestamp}.{ext}"
        filepath.write_text(output, encoding="utf-8")
        print(f"\nSaved to: {filepath}", file=sys.stderr)


if __name__ == "__main__":
    main()
