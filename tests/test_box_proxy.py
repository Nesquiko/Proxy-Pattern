from brownie.network.contract import Contract, ProjectContract
from brownie.project.main import Project
from scripts.util import encode_function_data, get_account
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy


def test_proxy_retrieve_zero():
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

    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)

    assert proxy_box.retrieve() == 0


def test_proxy_with_init_retrieve_not_zero():
    account = get_account()
    box: ProjectContract = Box.deploy({"from": account})
    proxy_admin: ProjectContract = ProxyAdmin.deploy({"from": account})

    value = 5
    initializer = box.store, value
    box_encoded_init = encode_function_data(*initializer)
    proxy: ProjectContract = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_init,
        {"from": account, "gas_limit": 1000000},
    )

    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)

    assert proxy_box.retrieve() == value


def test_proxy_store_retrieve_not_zero():
    account = get_account()
    box: ProjectContract = Box.deploy({"from": account})
    proxy_admin: ProjectContract = ProxyAdmin.deploy({"from": account})

    value = 5
    box_encoded_init = encode_function_data()
    proxy: ProjectContract = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_init,
        {"from": account, "gas_limit": 1000000},
    )

    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(value, {"from": account})

    assert proxy_box.retrieve() == value
