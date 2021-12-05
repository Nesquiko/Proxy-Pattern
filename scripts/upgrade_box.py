from brownie import BoxV2, TransparentUpgradeableProxy, ProxyAdmin
from brownie.network.contract import Contract, ProjectContract
from scripts.util import get_account, upgrade, encode_function_data


def upgrade_box():
    account = get_account()
    box_v2: ProjectContract = BoxV2.deploy({"from": account})

    proxy: ProjectContract = TransparentUpgradeableProxy[-1]
    proxy_admin: ProjectContract = ProxyAdmin[-1]

    initializer = box_v2.store, 333

    tx = upgrade(account, proxy, box_v2.address, proxy_admin, *initializer)
    tx.wait(1)

    print(f"Proxy has been updated!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    print(
        f"UPDATED - Retrieving value from box proxy, value is {proxy_box.retrieve()}."
    )

    print("Incrementing stored value...")
    proxy_box.increment({"from": account})

    print(
        f"UPDATED - Retrieving value from box proxy, value is {proxy_box.retrieve()}."
    )
