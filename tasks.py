import requests
from config import *
from client import Client
from utils.network import Base
from utils.utils import TokenAmount, read_private_keys

private_keys = read_private_keys()
main_wallet = Client(MAIN_PRIVATE_KEY, Base)


def top_up_burner_wallets():
    for private_key in private_keys:
        to = Client(private_key, Base)
        try:
            tx_hash = main_wallet.send_transaction(
                to=to.address,
                value=TokenAmount(TOP_UP_AMOUNT, 18, False)
            )
            main_wallet.verify_tx(tx_hash)
        except Exception as e:
            print(f'{to.address} | error | {e}')


def claim_airdrop():
    url = 'https://api.orbiter.finance/task-platform/proof/claim'
    for private_key in private_keys:
        client = Client(private_key, Base)
        token = client.sign_message()
        headers = {
            'token': '0x' + token
        }
        try:
            response = requests.post(url, headers=headers, proxies=PROXY)
            res_data = response.json()

            amount = TokenAmount(int(res_data['data']['amount']), 18, False)
            proof = res_data['data']['proof']
            root = res_data['data']['root']

            tx_hash = client.claim(root, amount, proof)
            client.verify_tx(tx_hash)
        except Exception as e:
            print(f'{client.address} | error | {e}')


def transfer_obt_to_main():
    for private_key in private_keys:
        client = Client(private_key, Base)
        try:
            tx_hash = client.transfer_token(main_wallet.address)
            client.verify_tx(tx_hash)
        except Exception as e:
            print(f'{client.address} | error | {e}')
