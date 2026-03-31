from typing import NewType, Optional, TypedDict

from pydantic import BaseModel, Field, validator
from web3 import Web3

CHAIN_NAMES_BY_ID = {
    "1": "ethereum",
    "10": "optimism",
    "100": "gnosis",
    "-1": "solana",
    "137": "polygon",
    "42161": "arbitrum",
    "43114": "avax",
    "56": "bsc",
    "-3": "bitcoin",
}

Address = NewType("Address", str)

ChainId = NewType("ChainId", int)


class Token(BaseModel):
    symbol: str
    name: str
    address: Address
    decimals: int = Field(..., alias="tokenDecimal")
    chainId: ChainId
    logoURI: Optional[str]
    coingeckoId: Optional[str]
    listedIn: list[str] = []

    class Config:
        allow_population_by_field_name = True

    def __init__(self, **data):
        super().__init__(
            logoURI=(
                data.pop("logoURI", None)
                or data.pop("logo", None)
                or data.pop("icon", None)
                or data.pop("image", None)
            ),
            **data,
        )

    # if logo.startswith('//'):
    # logo = 'ht

    @validator("address")
    def addr_checksum(cls, v: str):
        v = v.strip()
        if Web3.is_address(v):
            if "#" in v:
                v = v.split("#")[0]
            return Web3.to_checksum_address(v)
        return v


NATIVE_ADDR_0xe = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
NATIVE_ADDR_0x0 = Address("0x0000000000000000000000000000000000000000")

NATIVE_MATIC_ADDR = "0x0000000000000000000000000000000000001010"
