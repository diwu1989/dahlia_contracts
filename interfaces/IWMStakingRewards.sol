// SPDX-License-Identifier: MIT

pragma solidity 0.6.12;

import 'OpenZeppelin/openzeppelin-contracts@3.4.0/contracts/token/ERC1155/IERC1155.sol';

import './IERC20Wrapper.sol';

interface IWMStakingRewards is IERC1155, IERC20Wrapper {
  /// @dev Mint ERC1155 token for the given ERC20 token.
  function mint(uint amount) external returns (uint id);

  /// @dev Burn ERC1155 token to redeem ERC20 token back.
  function burn(uint id, uint amount) external returns (uint);

  function getReward() external view returns (address[] calldata);

  function depth() external view returns (uint);
}
