from brownie import (
    accounts, ERC20KP3ROracle, UniswapV2Oracle, ProxyOracle, CoreOracle,
    CurveOracle, WERC20, UbeswapV1Oracle
)
from brownie import interface
from .utils import *

def main():
    deployer = accounts.load('gh')

    core_oracle_addr = '0x0286530271720D1B4538e92c7Cc0922D68A053f2'
    proxy_oracle_addr = '0x4cf091fd046B6f21Dd5bdf490Fb274315e77f028'
    celo_addr = '0xf194afdf50b03e69bd7d057c1aa9e10c9954e4c9'
    ube_addr = '0xbe413cdfdad27e71cf533882c760a91ecd02ab27'
    btc_addr = '0xd629eb00deced2a080b7ec630ef6ac117e614f1b'
    mcusd_addr = '0x64defa3544c695db8c535d289d843a189aa26b98'
    mceur_addr = '0xa8d0e6799ff3fd19c6459bf02689ae09c4d78ba7'
    scelo_addr = '0x2879bfd5e7c4ef331384e908aaa3bd3014b703fa'
    ube_router_addr = '0xE3D8bd6Aed4F159bc8000a9cD47CffDb95F96121'

    core_oracle = CoreOracle.at(core_oracle_addr)
    proxy_oracle = ProxyOracle.at(proxy_oracle_addr)
    celo = interface.IERC20Ex(celo_addr)
    ube = interface.IERC20Ex(ube_addr)
    btc = interface.IERC20Ex(btc_addr)
    mcusd = interface.IERC20Ex(mcusd_addr)
    mceur = interface.IERC20Ex(mceur_addr)
    scelo = interface.IERC20Ex(scelo_addr)
    ube_router = interface.IUniswapV2Router02(ube_router_addr)

    uni_oracle = UniswapV2Oracle.deploy(core_oracle, {'from': deployer})
    ubeswap_oracle = UbeswapV1Oracle.deploy({'from': deployer})

    ubeswap_oracle.addPair(celo_addr, ube_addr)
    ubeswap_oracle.addPair(mcusd_addr, btc_addr)
    ubeswap_oracle.addPair(celo_addr, mcusd_addr)
    ubeswap_oracle.addPair(scelo_addr, celo_addr)
    ubeswap_oracle.addPair(celo_addr, mceur_addr)

    kp3r_oracle = ERC20KP3ROracle.deploy(ubeswap_oracle, {'from': deployer})

    ube_factory_address = ube_router.factory({'from': deployer})
    ube_factory = interface.IUniswapV2Factory(ube_factory_address)

    celo_ube_lp = ube_factory.getPair(celo, ube)
    mcusd_btc_lp = ube_factory.getPair(mcusd, btc)
    celo_mcusd_lp = ube_factory.getPair(celo, mcusd)
    scelo_celo_lp = ube_factory.getPair(scelo, celo)
    celo_mceur_lp = ube_factory.getPair(celo, mceur)


    core_oracle.setRoute([
        celo_addr,
        ube_addr,
        btc_addr,
        mcusd_addr,
        mceur_addr,
        scelo_addr,
        celo_ube_lp,
        mcusd_btc_lp,
        celo_mcusd_lp,
        scelo_celo_lp,
        celo_mceur_lp,
    ], [
        kp3r_oracle,
        kp3r_oracle,
        kp3r_oracle,
        kp3r_oracle,
        kp3r_oracle,
        kp3r_oracle,
        uni_oracle,
        uni_oracle,
        uni_oracle,
        uni_oracle,
        uni_oracle,
    ], {'from': deployer})

    proxy_oracle.setTokenFactors([
        celo_addr,
        ube_addr,
        btc_addr,
        mcusd_addr,
        mceur_addr,
        scelo_addr,
        celo_ube_lp,
        mcusd_btc_lp,
        celo_mcusd_lp,
        scelo_celo_lp,
        celo_mceur_lp,
    ], [
        [13000, 7800, 10250],
        [13000, 7800, 10250],
        [13000, 7800, 10250],
        [11000, 9000, 10250],
        [11000, 9000, 10250],
        [13000, 7800, 10250],
        [50000, 7800, 10250],
        [50000, 7800, 10250],
        [50000, 7800, 10250],
        [50000, 7800, 10250],
        [50000, 7800, 10250],
    ], {'from': deployer})

    werc20 = WERC20.deploy({'from': deployer})

    proxy_oracle.setWhitelistERC1155(
        [werc20],
        True,
        {'from': deployer},
    )

    print('Done!')