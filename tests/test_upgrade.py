from brownie.network.contract import Contract, ProjectContract
from brownie.exceptions import VirtualMachineError
from scripts.util import encode_function_data, get_account, upgrade
from brownie import Box, BoxV2, ProxyAdmin, TransparentUpgradeableProxy
import pytest


def test_proxy_not_implemented_method():
    account = get_account()
    box: ProjectContract = Box.deploy({"from": account})
    proxy_admin: ProjectContract = ProxyAdmin.deploy({"from": account})
    box_encoded_init = encode_function_data()

    proxy: ProjectContract = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_init,
        {"from": account, "gas_limit": 1000000},
    )
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)

    with pytest.raises(VirtualMachineError):
        proxy_box.increment({"from": account})


def test_proxy_upgrade_without_init_retrieve():
    account = get_account()
    box: ProjectContract = Box.deploy({"from": account})
    box_v2: ProjectContract = BoxV2.deploy({"from": account})

    proxy_admin: ProjectContract = ProxyAdmin.deploy({"from": account})
    box_encoded_init = encode_function_data()

    proxy: ProjectContract = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_init,
        {"from": account, "gas_limit": 1000000},
    )

    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    upgrade(account, proxy, box_v2.address, proxy_admin_contract=proxy_admin)

    assert proxy_box.retrieve() == 0
