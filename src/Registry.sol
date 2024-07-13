// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

error Registry__TooLittleETH();

contract Registry {
    uint256 public PRICE_PER_CONTRACT_SCAN = 1 gwei;

    struct Subscription {
        address[] scope;
        uint256 scans;
    }
    mapping(bytes32 protocolId => Subscription subscription) public protocolMapping;

    event ProtocolAdded(bytes32 protocolId);

    function registerProtocol(bytes32 _protocolId, address[] calldata _scope, uint256 _scans) external payable {
        uint256 price = getPrice(_scope.length, _scans);
        if (msg.value < price) revert Registry__TooLittleETH();

        protocolMapping[_protocolId] = Subscription(_scope, _scans);

        emit ProtocolAdded(_protocolId);
    }

    function getSubscription(bytes32 protocolId) external view returns (address[] memory scope, uint256 scans) {
        Subscription storage subscription = protocolMapping[protocolId];
        return (subscription.scope, subscription.scans);
    }

    function isSubscribed(bytes32 protocolId) public view returns (bool) {
        return (protocolMapping[protocolId].scans > 0);
    }

    function getPrice(uint256 _scopeSize, uint256 _scans) public view returns (uint256 price) {
        return (_scans * _scopeSize * PRICE_PER_CONTRACT_SCAN);
    }
}
