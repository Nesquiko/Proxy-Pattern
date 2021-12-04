import brownie
from scripts.util import get_account
from brownie import network, Box, ProxyAdmin


def main():
    account = get_account()
    print(f"Deploying to {network.show_active()}.")
    print(f"With account {account}.")

    box = Box.deploy({"from": account})

    proxy_admin = ProxyAdmin.deploy({"from": account})
