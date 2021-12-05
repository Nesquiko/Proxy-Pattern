from brownie.network.contract import Contract, ProjectContract
from scripts.util import get_account, encode_function_data
from brownie import network, Box, ProxyAdmin, TransparentUpgradeableProxy, project


def deploy_box():
    account = get_account()
    print(f"Deploying to {network.show_active()}.")
    print(f"With account {account}.")

    box = Box.deploy(
        {"from": account},
        publish_source=True,
    )

    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=True)

    initializer = box.store, 843
    box_encoded_initializer_function = encode_function_data(*initializer)

    proxy: ProjectContract = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
        publish_source=True,
    )

    print(f"Proxy was deployed at {proxy}, contract is now upgreadable!")

    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    print(f"Retrieving value from box proxy, value is {proxy_box.retrieve()}.")
