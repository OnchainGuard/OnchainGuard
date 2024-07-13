// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

error Registry__TooLittleETH();
error Registry__OnlyOperator();
error Registry__OnlyProtocolAdmin();

contract Registry {
    uint256 public PRICE_PER_CONTRACT_SCAN = 1 gwei;
    address public operator;

    struct Subscription {
        address[] scope;
        uint256 scans;
        address admin;
    }

    mapping(bytes32 protocolId => Subscription subscription) public protocolMapping;

    event ProtocolAdded(bytes32 protocolId);
    event ProtocolRemoved(bytes32 protocolId);
    event ProtocolScanned(bytes32 protocolId);

    constructor() {
        operator = msg.sender;
    }

    modifier onlyOperator() {
        if (msg.sender != operator) revert Registry__OnlyOperator();
        _;
    }

    modifier onlyProtocolAdmin(bytes32 _protocolId) {
        if (msg.sender != protocolMapping[_protocolId].admin) revert Registry__OnlyProtocolAdmin();
        _;
    }

    function registerProtocol(bytes32 _protocolId, address[] calldata _scope, uint256 _scans, address _admin) external payable {
        uint256 price = getPrice(_scope.length, _scans);
        if (msg.value < price) revert Registry__TooLittleETH();

        protocolMapping[_protocolId] = Subscription(_scope, _scans, _admin);

        emit ProtocolAdded(_protocolId);
    }

    function getSubscription(bytes32 protocolId) external view returns (address[] memory scope, uint256 scans, address admin) {
        Subscription storage subscription = protocolMapping[protocolId];
        return (subscription.scope, subscription.scans, subscription.admin);
    }

    function updateSubscription(bytes32 protocolId, address[] calldata _scope, uint256 _scans) external payable onlyProtocolAdmin(protocolId) {
        uint256 price = getPrice(_scope.length, _scans);
        if (msg.value < price) revert Registry__TooLittleETH();

        Subscription storage subscription = protocolMapping[protocolId];
        subscription.scope = _scope;
        subscription.scans = _scans;
    }

    function isSubscribed(bytes32 protocolId) public view returns (bool) {
        return (protocolMapping[protocolId].scans > 0);
    }

    function getPrice(uint256 _scopeSize, uint256 _scans) public view returns (uint256 price) {
        return (_scans * _scopeSize * PRICE_PER_CONTRACT_SCAN);
    }

    function postScan(bytes32[] calldata _protocolIds) external onlyOperator {
        for (uint256 i = 0; i < _protocolIds.length; i++) {
            // TODO: check if protocol is valid
            if (!isSubscribed(_protocolIds[i])) {
                delete protocolMapping[_protocolIds[i]];

                emit ProtocolRemoved(_protocolIds[i]);
            } else {
                protocolMapping[_protocolIds[i]].scans -= 1;

                // TODO: add proof
                emit ProtocolScanned(_protocolIds[i]);
            }
        }
    }

}
