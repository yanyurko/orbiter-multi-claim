from web3 import Web3
from eth_account.messages import encode_defunct
from utils.network import Network
from utils.utils import read_json, TokenAmount, AIRDROP_CONTRACT_ABI, ERC_ABI
from typing import Optional


class Client:
    default_abi = read_json(AIRDROP_CONTRACT_ABI)
    erc20_abi = read_json(ERC_ABI)
    contract_address = Web3.to_checksum_address('0x13dFDd3a9B39323F228Daf73B62C23F7017E4679')
    obt_address = Web3.to_checksum_address('0x514D8E8099286a13486Ef6C525C120f51C239B52')

    def __init__(self, private_key: str, network: Network):
        self.private_key = private_key
        self.network = network
        self.w3 = Web3(Web3.HTTPProvider(endpoint_uri=self.network.rpc_url))
        self.address = Web3.to_checksum_address(self.w3.eth.account.from_key(self.private_key).address)

    def verify_merkle_proof(self, proof: str):
        return str(self.w3.eth.contract(
            address=Web3.to_checksum_address(Client.contract_address),
            abi=Client.default_abi
        ).functions.merkleRoots(proof).call())

    def sign_message(self):
        message = "Orbiter Airdrop"
        message_to_sign = encode_defunct(text=message)
        signed_message = self.w3.eth.account.sign_message(message_to_sign, private_key=self.private_key)
        return signed_message.signature.hex()

    def claim(self, root: str, amount: TokenAmount, proof: list[str]):
        print(f'{self.address} | claiming {amount.Ether} OBT')

        contract = self.w3.eth.contract(
            address=Client.contract_address,
            abi=Client.default_abi
        )
        data = contract.encode_abi("claim", args=[root, amount.Wei, proof])
        return self.send_transaction(
            to=Client.contract_address,
            data=data
        )

    def transfer_token(self, to: str, amount: Optional[TokenAmount] = None):
        contract = self.w3.eth.contract(
            address=Client.obt_address,
            abi=Client.erc20_abi
        )

        if not amount:
            amount = int(contract.functions.balanceOf(self.address).call())

        data = contract.encode_abi("transfer", args=[to, amount])
        return self.send_transaction(
            to=Client.obt_address,
            data=data
        )

    def send_transaction(self, to, data=None, from_=None, value: Optional[TokenAmount] = None):
        if not from_:
            from_ = self.address

        tx_params = {
            'chainId': self.network.chain_id,
            'nonce': self.w3.eth.get_transaction_count(self.address),
            'from': Web3.to_checksum_address(from_),
            'to': Web3.to_checksum_address(to)
        }

        if data:
            tx_params['data'] = data

        last_block = self.w3.eth.get_block('latest')
        max_priority_fee_per_gas = self.w3.eth.max_priority_fee
        base_fee = int(last_block['baseFeePerGas'] * 1.1)
        max_fee_per_gas = base_fee + max_priority_fee_per_gas

        tx_params['maxPriorityFeePerGas'] = max_priority_fee_per_gas
        tx_params['maxFeePerGas'] = max_fee_per_gas

        if value:
            tx_params['value'] = value.Wei

        try:
            tx_params['gas'] = self.w3.eth.estimate_gas(tx_params)
        except Exception as err:
            print(f'{self.address} | unable to estimate gas | {err}')
            tx_params['gas'] = 200000
        signed_tx = self.w3.eth.account.sign_transaction(tx_params, self.private_key)
        return self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    def verify_tx(self, tx_hash) -> bool:
        if not tx_hash:
            return False
        try:
            if self.w3.eth.wait_for_transaction_receipt(tx_hash)['status']:
                print(f'{self.address} | transaction was submitted | {tx_hash.hex()}')
                return True
            else:
                print(f'{self.address} | transaction failed')
        except Exception as err:
            print(f'{self.address} | unexpected error | {err}')
        return False
