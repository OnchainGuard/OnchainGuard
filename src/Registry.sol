// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

error Registry__TooLittleETH();

contract Registry {
    uint256 public PRICE_PER_DAY = 0.01 ether;
    struct Subscription {
        address[] scope;
        uint256 expiration;
    }
    mapping(bytes32 protocolId => Subscription subscription) public protocolMapping;

    event ProtocolAdded(bytes32 protocolId);

    function registerProtocol(bytes32 _protocolId, address[] calldata _scope, uint256 _duration) external payable {
        if (msg.value < PRICE_PER_DAY * _duration) revert Registry__TooLittleETH();

        protocolMapping[_protocolId] = Subscription(_scope, block.timestamp + _duration);

        emit ProtocolAdded(_protocolId);
    }

    function getSubscription(bytes32 protocolId) external view returns (address[] memory scope, uint256 expiration) {
        Subscription storage subscription = protocolMapping[protocolId];
        return (subscription.scope, subscription.expiration);
    }

    function isSubscribed(bytes32 protocolId) external view returns (bool) {
        return (block.timestamp <= protocolMapping[protocolId].expiration);
    }
}
