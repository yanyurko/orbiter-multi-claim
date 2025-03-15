import json
import sys
import os
from decimal import Decimal
from pathlib import Path


if getattr(sys, 'frozen', False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

ABI_DIR = os.path.join(ROOT_DIR, 'abi')
AIRDROP_CONTRACT_ABI = os.path.join(ABI_DIR, 'claim.json')
ERC_ABI = os.path.join(ABI_DIR, 'erc20.json')
PRIVATE_KEYS_PATH = os.path.join(ROOT_DIR, 'private_keys.txt')


class TokenAmount:
    def __init__(self, amount, decimals, wei):
        if wei:
            self.Wei: int = amount
            self.Ether: int = int(Decimal(str(amount)) / 10 ** decimals)
        else:
            self.Wei: int = int(Decimal(str(amount)) * 10 ** decimals)
            self.Ether: int = amount


def read_json(path: str, encoding=None):
    return json.load(open(path, encoding=encoding))


def read_private_keys():
    with open(PRIVATE_KEYS_PATH, 'r') as file:
        return file.read().splitlines()
