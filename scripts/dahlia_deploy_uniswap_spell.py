from brownie import (
    accounts, HomoraBank, UniswapV2SpellV1, WERC20,
)
from brownie import interface
from .utils import *

def main():
    deployer = accounts.load('gh')

    celo_addr = '0xf194afdf50b03e69bd7d057c1aa9e10c9954e4c9'
    ube_addr = '0xbe413cdfdad27e71cf533882c760a91ecd02ab27'
    btc_addr = '0xd629eb00deced2a080b7ec630ef6ac117e614f1b'
    mcusd_addr = '0x64defa3544c695db8c535d289d843a189aa26b98'
    mceur_addr = '0xa8d0e6799ff3fd19c6459bf02689ae09c4d78ba7'
    scelo_addr = '0x2879bfd5e7c4ef331384e908aaa3bd3014b703fa'
    ube_router_addr = '0xE3D8bd6Aed4F159bc8000a9cD47CffDb95F96121'
    werc20_addr = '0x219F5B0BCBCb2B86068DC97BbdF1b4672d19Aa2c'
    dahlia_bank_addr = '0x8772D538785f9dc2a8b1356D4550320E93f4A616'

    celo = interface.IERC20Ex(celo_addr)
    ube = interface.IERC20Ex(ube_addr)
    btc = interface.IERC20Ex(btc_addr)
    mcusd = interface.IERC20Ex(mcusd_addr)
    mceur = interface.IERC20Ex(mceur_addr)
    scelo = interface.IERC20Ex(scelo_addr)
    ube_router = interface.IUniswapV2Router02(ube_router_addr)
    werc20 = WERC20.at(werc20_addr)
    dahlia_bank = HomoraBank.at(dahlia_bank_addr)

    uniswap_spell = UniswapV2SpellV1.deploy(
        dahlia_bank, werc20, ube_router, celo,
        {'from': deployer},
    )

    uniswap_spell.getAndApprovePair(celo, ube, {'from': deployer})
    uniswap_spell.getAndApprovePair(mcusd, btc, {'from': deployer})
    uniswap_spell.getAndApprovePair(celo, mcusd, {'from': deployer})
    uniswap_spell.getAndApprovePair(scelo, celo, {'from': deployer})
    uniswap_spell.getAndApprovePair(celo, mceur, {'from': deployer})

    ube_factory_address = ube_router.factory()
    ube_factory = interface.IUniswapV2Factory(ube_factory_address)
    celo_ube_lp = ube_factory.getPair(celo, ube)
    mcusd_btc_lp = ube_factory.getPair(mcusd, btc)
    celo_mcusd_lp = ube_factory.getPair(celo, mcusd)
    scelo_celo_lp = ube_factory.getPair(scelo, celo)
    celo_mceur_lp = ube_factory.getPair(celo, mceur)

    uniswap_spell.setWhitelistLPTokens([celo_ube_lp, mcusd_btc_lp, celo_mcusd_lp, scelo_celo_lp, celo_mceur_lp], [True, True, True, True, True], {'from': deployer})

    dahlia_bank.setWhitelistSpells([uniswap_spell], [True], {'from': deployer})

    print('Done!')
