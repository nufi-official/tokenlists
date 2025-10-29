from collections import defaultdict

import httpx

from common import Address

CHAIN_ID_TO_NATIVE_COIN_COINGECKO_ID = {
    1: "ethereum",
    3: "ethereum",
    4: "ethereum",
    5: "ethereum",
    56: "binancecoin",
    97: "binancecoin",
    100: "gnosis",
    137: "matic-network",
    80001: "matic-network",
    43114: "avalanche-2",
    43113: "avalanche-2",
    10: "ethereum",
    69: "ethereum",
    42161: "ethereum",
    421611: "ethereum",
    1666600000: "harmony",
    1313161554: "ethereum",
    288: "ethereum",
    59144: "ethereum",
}


def get_coingecko_ids() -> dict[str, dict[Address, str]]:
    chain_id_to_coingecko_platform = {
        "42161": "arbitrum-one",
        "1088": "metis-andromeda",
        "56": "binance-smart-chain",
        "10": "optimistic-ethereum",
        "137": "polygon-pos",
        "43114": "avalanche",
        "100": "xdai",
        "1": "ethereum",
        "-1": "solana",
        "-3": "ordinals",
        "59144": "linea",
        "81457": "blast",
        "5000": "mantle",
        "100": "gnosis",
    }
    coingecko_platform_to_chain_id = {
        v: k for k, v in chain_id_to_coingecko_platform.items()
    }
    coins = httpx.get(
        "https://api.coingecko.com/api/v3/coins/list", params={"include_platform": True}
    ).json()
    res: dict[str, dict[Address, str]] = defaultdict(dict)
    for coin in coins:
        if not coin["id"]:
            continue
        for platform, address in coin.get("platforms", {}).items():
            if platform and address and platform in coingecko_platform_to_chain_id:
                res[coingecko_platform_to_chain_id[platform]][address.lower()] = coin[
                    "id"
                ]
    return res


coingecko_ids = get_coingecko_ids()
