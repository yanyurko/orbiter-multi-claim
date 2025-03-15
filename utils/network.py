from config import RPC_URL


class Network:
    def __init__(self,
                 name,
                 chain_id,
                 rpc_url,
                 explorer,
                 symbol,
                 decimals
                 ):
        self.name = name
        self.chain_id = chain_id
        self.rpc_url = rpc_url
        self.explorer = explorer
        self.symbol = symbol
        self.decimals = decimals


Base = Network(
    name='Base',
    chain_id=8453,
    rpc_url=RPC_URL,
    explorer='https://basescan.org/',
    symbol='ETH',
    decimals=18
)
