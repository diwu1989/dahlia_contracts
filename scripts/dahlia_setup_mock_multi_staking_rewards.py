from brownie import (
    accounts,
    interface,
    network,
    MockERC20,
    MockStakingRewards,
    MockMoolaStakingRewards,
    WMoolaStakingRewards,
    ProxyOracle,
)
import json

network.gas_limit(8000000)

def main():
    deployer = accounts.load('dahlia_admin')

    with open('scripts/dahlia_addresses.json', 'r') as f:
        addr = json.load(f)

    alfajores_addr = addr.get('alfajores')

    celo = interface.IERC20Ex(alfajores_addr.get('celo'))
    cusd = interface.IERC20Ex(alfajores_addr.get('cusd'))
    ceur = interface.IERC20Ex(alfajores_addr.get('ceur'))
    mock = interface.IERC20Ex(alfajores_addr.get('mock'))
    celo_cusd_staking = MockStakingRewards.at(alfajores_addr.get('celo_cusd_staking'))
    celo_ceur_staking = MockStakingRewards.at(alfajores_addr.get('celo_ceur_staking'))
    cusd_ceur_staking = MockStakingRewards.at(alfajores_addr.get('cusd_ceur_staking'))
    ufactory = interface.IUniswapV2Factory(alfajores_addr.get('ufactory'))
    proxy_oracle = ProxyOracle.at(alfajores_addr.get('proxy_oracle'))

    celo_cusd_lp = ufactory.getPair(celo, cusd)
    celo_ceur_lp = ufactory.getPair(celo, ceur)
    cusd_ceur_lp = ufactory.getPair(cusd, ceur)

    mock2 = MockERC20.deploy('Mother', 'MOM', 18, {'from': deployer})

    # mock.mint(celo_cusd_staking, 1000*10**18, {'from': deployer})
    # mock.mint(celo_ceur_staking, 1000*10**18, {'from': deployer})
    # mock.mint(cusd_ceur_staking, 1000*10**18, {'from': deployer})

    # celo_cusd_staking.setRewardsDuration(60*60*24*7, {'from': deployer})
    # celo_ceur_staking.setRewardsDuration(60*60*24*7, {'from': deployer})
    # cusd_ceur_staking.setRewardsDuration(60*60*24*7, {'from': deployer})

    # celo_cusd_staking.notifyRewardAmount(500*10**18, {'from': deployer})
    # celo_ceur_staking.notifyRewardAmount(500*10**18, {'from': deployer})
    # cusd_ceur_staking.notifyRewardAmount(500*10**18, {'from': deployer})

    celo_cusd_multi_staking = MockMoolaStakingRewards.deploy(deployer, deployer, mock2, celo_cusd_staking, [mock], celo_cusd_lp, {'from': deployer})
    celo_ceur_multi_staking = MockMoolaStakingRewards.deploy(deployer, deployer, mock2, celo_ceur_staking, [mock], celo_ceur_lp, {'from': deployer})
    cusd_ceur_multi_staking = MockMoolaStakingRewards.deploy(deployer, deployer, mock2, cusd_ceur_staking, [mock], cusd_ceur_lp, {'from': deployer})

    mock2.mint(celo_cusd_multi_staking, 1000*10**18, {'from': deployer})
    mock2.mint(celo_ceur_multi_staking, 1000*10**18, {'from': deployer})
    mock2.mint(cusd_ceur_multi_staking, 1000*10**18, {'from': deployer})

    celo_cusd_multi_staking.setRewardsDuration(60*60*24*7, {'from': deployer})
    celo_ceur_multi_staking.setRewardsDuration(60*60*24*7, {'from': deployer})
    cusd_ceur_multi_staking.setRewardsDuration(60*60*24*7, {'from': deployer})

    celo_cusd_multi_staking.notifyRewardAmount(100*10**18, {'from': deployer})
    celo_ceur_multi_staking.notifyRewardAmount(100*10**18, {'from': deployer})
    cusd_ceur_multi_staking.notifyRewardAmount(100*10**18, {'from': deployer})

    celo_cusd_wmstaking = WMoolaStakingRewards.deploy(
        celo_cusd_multi_staking,
        celo_cusd_lp,
        mock2,
        2,
        {'from': deployer}
    )

    celo_ceur_wmstaking = WMoolaStakingRewards.deploy(
        celo_ceur_multi_staking,
        celo_ceur_lp,
        mock2,
        2,
        {'from': deployer}
    )

    cusd_ceur_wmstaking = WMoolaStakingRewards.deploy(
        cusd_ceur_multi_staking,
        cusd_ceur_lp,
        mock2,
        2,
        {'from': deployer}
    )

    proxy_oracle.setWhitelistERC1155(
        [celo_cusd_wmstaking, celo_ceur_wmstaking, cusd_ceur_wmstaking],
        True,
        {'from': deployer},
    )

    addr.get('alfajores').update({
        'mock2': mock2.address,
        'celo_cusd_mstaking': celo_cusd_multi_staking.address,
        'celo_ceur_mstaking': celo_ceur_multi_staking.address,
        'cusd_ceur_mstaking': cusd_ceur_multi_staking.address,
        'celo_cusd_wmstaking': celo_cusd_wmstaking.address,
        'celo_ceur_wmstaking': celo_ceur_wmstaking.address,
        'cusd_ceur_wmstaking': cusd_ceur_wmstaking.address,
    })

    print(json.dumps(addr, indent=4), file=open('scripts/dahlia_addresses.json', 'w'))