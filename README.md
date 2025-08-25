
# Multi-chain token list standard. 

## TLDR

In this repo you may find tokenlists aggregated from various trusted providers, such as sushiswap or 1inch. We only list a token
if it appeared in 2 or more different tokenlists. So we believe that if 2 or more providers list a token, than it is
most likely not a scam.

## Usage example
If you want to use tokenlist in your dApp — simply download json with needed chain tokens. Head for raw link like 

https://raw.githubusercontent.com/nufi-official/tokenlists/main/tokenlists/ethereum.json (Ethereum tokenlist)

or 

https://raw.githubusercontent.com/nufi-official/tokenlists/main/tokenlists/bsc.json (Binance Smart Chain Tokenlist)

## Providers

We collect tokenlists from github repos or open APIs from various platforms, currently:
- [CoinGecko](https://www.coingecko.com/)
- [1inch](https://app.1inch.io/)
- [Uniswap](https://uniswap.org/)
- [Sushiswap](https://www.sushi.com/)
- [OpenOcean](https://openocean.finance/)
- [SolanaLabs](https://solanalabs.com/)
- [ElkFinance](https://elk.finance/)
- [OneSol](https://1sol.io/)
- [QuickSwap](https://quickswap.exchange/#/swap)
- [FuseSwap](https://beta.fuseswap.com/#/swap)
- [TrisolarisLabs](https://www.trisolaris.io/#/swap)
- [Rubic](https://app.rubic.exchange/)

Feel free to add new provider if you think it is trusted and if it has opensource tokenlists, on github 
or in API.

## Chains with trusted tokens

Here are chains presented in our tokenlists with current token count. You can find out more in `/tokenlists` folder.
Token counts are approximate and may vary as providers update their tokenlists.

- Ethereum, 5907 tokens
- Polygon, 1663 tokens
- Bsc, 1506 tokens
- Solana, 636 tokens
- Avax, 539 tokens
- 101, 507 tokens
- Arbitrum, 417 tokens
- Ftm, 378 tokens
- Gnosis, 371 tokens
- Optimism, 347 tokens
- 8453, 215 tokens
- Heco, 197 tokens
- Aurora, 108 tokens
- Cronos, 86 tokens
- Moonbeam, 86 tokens
- Bitcoin, 83 tokens
- Moonriver, 82 tokens
- Harmony, 76 tokens
- Celo, 76 tokens
- Okex, 48 tokens
- Evmos, 23 tokens
- Fuse, 23 tokens
- 80094, 15 tokens
- Astar, 15 tokens
- Boba, 14 tokens
- Telos, 10 tokens
- Kcc, 9 tokens
- 130, 5 tokens

Testnets:

- Rinkeby
- Ropsten
- Goerli
- Mumbai
- Sepolia
- etc.

## How are tokenlists formed

We collect many tokenlists from many providers, then we aggregate them by chains and tokens addresses. 
For each token we check whether it is listed in 2 or more tokenlists from different providers. If so, 
we add it to our trusted tokenlist.


## Run aggregation script yourself
Install requirements
```$ pip3 install -r requirements.txt```
Run the script from repo root folder
```python3 aggregate_tokens.py```

## Generate readme.md based on aggregated data
```bash
python generate_readme.py
```


## Contribute
Feel free to open issues and PRs with tokens, chains or providers that you want to add.

Developed by [Via.Exchange](https://Via.Exchange) team, forked and modified by [Nu.Fi](https://nu.fi).
