import asyncio
import json
import logging
from collections import defaultdict

from coingecko_ids import CHAIN_ID_TO_NATIVE_COIN_COINGECKO_ID
from common import (
    Address,
    ChainId,
    NATIVE_ADDR_0x0,
    NATIVE_ADDR_0xe,
    NATIVE_MATIC_ADDR,
    Token,
    CHAIN_NAMES_BY_ID,
)
from token_list_providers import (
    CoinGeckoTokenLists,
    Lifinance,
    OneInchTokenLists,
    RubicLists,
    tokenlists_providers,
)

TOKENLISTS_FOLDER = "tokenlists"

ALL_TOKENS_FOLDER = "all_tokens"

log = logging.getLogger(__name__)


def merge_tokens(
    old_tokens: dict[int, dict[Address, Token]],
    new_tokens: dict[int, dict[Address, Token]],
) -> dict[int, dict[Address, Token]]:
    merged_tokens = {
        int(k): {a: t for a, t in v.items()} for k, v in old_tokens.items()
    }

    for chain_id, tokens in new_tokens.items():
        if merged_tokens.get(chain_id) is None:
            merged_tokens[chain_id] = {}

        for _, token in tokens.items():
            addr = token.address
            if merged_tokens[chain_id].get(addr) is not None:
                current_listed_in = merged_tokens[chain_id][addr].listedIn
                current_listed_in.extend(token.listedIn)
                merged_tokens[chain_id][addr].listedIn = list(set(current_listed_in))
            else:
                merged_tokens[chain_id][addr] = token

    return merged_tokens


def filter_ignored_tokens(
    tokens: dict[int, dict[Address, Token]]
) -> dict[int, dict[Address, Token]]:
    # {chain_id: set(addresses)}
    IGNORE_LIST = {
        # bsc scam coins (all addresses have some balance)
        56: set(
            [
                "0x683e9dCf085E5efCc7925858aAcE94D4b8882024",
                "0xD22202d23fE7dE9E3DbE11a2a88F42f4CB9507cf",
                "0x5CA42204cDaa70d5c773946e69dE942b85CA6706",
            ]
        ),
        42161: set(["walc.near"]),
    }

    filtered = {
        k: {
            a: t
            for a, t in v.items()
            if k not in IGNORE_LIST or a not in IGNORE_LIST[k]
        }
        for k, v in tokens.items()
    }

    return filtered


async def collect_trusted_tokens() -> dict[int, list[Token]]:
    data = await asyncio.gather(
        *[provider.get_tokenlists() for provider in tokenlists_providers]
    )
    provider_data: dict[str, dict[str, list[Token]]] = {}
    for prov in data:
        provider_data |= prov

    res: dict[int, dict[Address, Token]] = defaultdict(dict)
    for provider_name, tokens_by_chains in provider_data.items():
        for _chain_id, tokens in tokens_by_chains.items():
            chain_id = int(_chain_id)
            if chain_id == 101:  # solana
                chain_id = -1
            for token in tokens:
                addr = Address(token.address.lower())
                if token.chainId == 101:
                    token.chainId = ChainId(-1)
                if addr == NATIVE_ADDR_0xe or addr == NATIVE_MATIC_ADDR:
                    addr = NATIVE_ADDR_0x0
                    token.address = NATIVE_ADDR_0x0
                if addr == NATIVE_ADDR_0x0:
                    token.coingeckoId = CHAIN_ID_TO_NATIVE_COIN_COINGECKO_ID.get(
                        token.chainId
                    )
                if addr in res[chain_id]:
                    # 1inch has best token logos
                    if provider_name == OneInchTokenLists.name:
                        res[chain_id][addr].logoURI = token.logoURI
                    # coingecko and lifinance have worst token logos
                    elif provider_name not in (
                        Lifinance.name,
                        CoinGeckoTokenLists.name,
                        RubicLists.name,
                    ) and (
                        "tokens.1inch.io" not in (res[chain_id][addr].logoURI or [])
                    ):
                        res[chain_id][addr].logoURI = token.logoURI
                    if provider_name not in res[chain_id][addr].listedIn:
                        res[chain_id][addr].listedIn.append(provider_name)

                else:
                    res[chain_id][addr] = token
                    res[chain_id][addr].listedIn.append(provider_name)

    old_tokens: dict[int, dict[Address, Token]] = {}
    with open(f"{ALL_TOKENS_FOLDER}/all.json", "r", encoding="utf-8") as f:
        old_tokens = {
            int(k): {t.address: t for t in [Token(**t) for t in v]}
            for k, v in json.load(f).items()
        }

    new_tokens = {
        int(k): {t.address: t for _, t in v.items()}
        for k, v in res.items()
        if len(v) > 0
    }

    merged_tokens = merge_tokens(old_tokens, new_tokens)

    filtered_tokens = filter_ignored_tokens(merged_tokens)

    all_tokens = {
        k: list(sorted(v.values(), key=lambda x: x.address, reverse=True))
        for k, v in filtered_tokens.items()
        if len(v) > 0
    }

    trusted = {k: [t for t in v if len(t.listedIn) > 1] for k, v in all_tokens.items()}

    # trusted tokens
    for chain_id, tokens in trusted.items():
        filename = (
            f"{TOKENLISTS_FOLDER}/{CHAIN_NAMES_BY_ID.get(str(chain_id), chain_id)}.json"
        )
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([t.dict() for t in tokens], f, ensure_ascii=False, indent=4)
    with open(f"{TOKENLISTS_FOLDER}/all.json", "w", encoding="utf-8") as f:
        json.dump(
            {k: [t.dict() for t in v] for k, v in trusted.items()},
            f,
            ensure_ascii=False,
            indent=4,
        )

    # all tokens found
    for chain_id, tokens in all_tokens.items():
        filename = (
            f"{ALL_TOKENS_FOLDER}/{CHAIN_NAMES_BY_ID.get(str(chain_id), chain_id)}.json"
        )
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([t.dict() for t in tokens], f, ensure_ascii=False, indent=4)
    with open(f"{ALL_TOKENS_FOLDER}/all.json", "w", encoding="utf-8") as f:
        json.dump(
            {k: [t.dict() for t in v] for k, v in all_tokens.items()},
            f,
            ensure_ascii=False,
            indent=4,
        )

    log.info("Succesfully collected trusted tokens")
    return trusted


if __name__ == "__main__":
    asyncio.run(collect_trusted_tokens())
