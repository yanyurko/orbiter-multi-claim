from tasks import top_up_burner_wallets, claim_airdrop, transfer_obt_to_main


def main():
    menu = """
    1. Top up burner wallets from main
    2. Claim an airdrop on burner wallets
    3. Transfer all OBT to the main wallet
    """
    print(menu)
    mode = input("Choose an option: ")
    if mode == "1":
        top_up_burner_wallets()
    elif mode == "2":
        claim_airdrop()
    elif mode == "3":
        transfer_obt_to_main()
    else:
        print("Invalid option.")
        return


if __name__ == "__main__":
    main()
