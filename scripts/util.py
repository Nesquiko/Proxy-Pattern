from brownie import network, accounts, config
from brownie.network.contract import ProjectContract
from brownie.project.main import new
import eth_utils


NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]


def get_account(number=None):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if number:
        return accounts[number]
    if network.show_active() in config["networks"]:
        account = accounts.add(config["wallets"]["from_key"])
        return account
    return None


def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        eth_utils.to_bytes(hexstr="0x")

    return initializer.encode_input(*args)


def upgrade(
    account,
    proxy: ProjectContract,
    new_impl_address: ProjectContract,
    proxy_admin=None,
    initializer=None,
    *args
):
    tx = None

    if proxy_admin:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            tx = proxy_admin.upgradeAndCall(
                proxy.address,
                new_impl_address.address,
                encoded_function_call,
                {"from": account},
            )
        else:
            tx = proxy_admin.upgrade(
                proxy.address, new_impl_address.address, {"from": account}
            )

    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            tx = proxy_admin.upgradeToAndCall(
                new_impl_address.address, encoded_function_call, {"from": account}
            )
        else:
            tx = proxy.upgradeTo(new_impl_address.address, {"from": account})

    return tx
