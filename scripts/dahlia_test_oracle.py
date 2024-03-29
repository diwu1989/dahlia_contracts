from brownie import (
    interface,
    UniswapV2Oracle,
    CoreOracle
)
import json

def main():
    f = open('scripts/dahlia_addresses.json')
    addr = json.load(f)['mainnet']

    celo = interface.IERC20Ex(addr['celo'])
    mcusd = interface.IERC20Ex(addr['mcusd'])
    mceur = interface.IERC20Ex(addr['mceur'])
    core_oracle = CoreOracle.at(addr['core_oracle'])
    uni_oracle = UniswapV2Oracle.at(addr['uni_oracle'])
    ube_factory = interface.IUniswapV2Factory(addr['ube_factory'])

    print("celo:", core_oracle.getCELOPx(celo))
    print("mcusd:", core_oracle.getCELOPx(mcusd))
    print("mceur:", core_oracle.getCELOPx(mceur))


    # print("ube-celo", uni_oracle.getCELOPx(ube_factory.getPair(ube, celo)))
    # print("mcusd-btc", uni_oracle.getCELOPx(ube_factory.getPair(mcusd, btc)))
    # print("celo-mcusd", uni_oracle.getCELOPx(ube_factory.getPair(celo, mcusd)))
    # print("scelo-celo", uni_oracle.getCELOPx(ube_factory.getPair(scelo, celo)))
    # print("celo-mceur", uni_oracle.getCELOPx(ube_factory.getPair(celo, mceur)))