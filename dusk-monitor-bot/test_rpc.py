#!/usr/bin/env python3
"""Test Alchemy RPC connection"""

from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

rpc_url = os.getenv("ETH_RPC_URL")
print(f"Testing RPC: {rpc_url}")

try:
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    print(f"Connected: {w3.is_connected()}")

    if w3.is_connected():
        block = w3.eth.block_number
        print(f"Current block: {block}")

        # Try to get a few event logs
        contract_address = Web3.to_checksum_address("0x940a2dB1B7008B6C776d4faaCa729d6d4A4AA551")
        erc20_abi = [{
            "anonymous": False,
            "inputs": [
                {"indexed": True, "name": "from", "type": "address"},
                {"indexed": True, "name": "to", "type": "address"},
                {"indexed": False, "name": "value", "type": "uint256"}
            ],
            "name": "Transfer",
            "type": "event"
        }]

        contract = w3.eth.contract(address=contract_address, abi=erc20_abi)

        print(f"\nTesting event logs...")
        from_block = block - 10
        to_block = block

        print(f"Fetching events from block {from_block} to {to_block}...")
        events = contract.events.Transfer.get_logs(
            fromBlock=from_block,
            toBlock=to_block
        )
        print(f"✅ Success! Found {len(events)} transfer events")

except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Type: {type(e).__name__}")
