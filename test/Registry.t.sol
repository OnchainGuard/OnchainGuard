// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "src/Registry.sol";
import "forge-std/Test.sol";

contract RegistryTest is Test {
    Registry registry;
    bytes32 protocolId;
    
    uint256 SCANS = 100;

    function setUp() public {
        registry = new Registry();
        protocolId = keccak256("SAMPLE PROTOCOL");
    }

    function _registerSampleProtocol() internal returns (address[] memory, uint256) {
        address[] memory scope = new address[](2);
        scope[0] = address(0);
        scope[1] = address(1);

        uint256 pricePerContractScan = registry.PRICE_PER_CONTRACT_SCAN();
        uint256 price = SCANS * scope.length * pricePerContractScan;

        registry.registerProtocol{ value: price }(protocolId, scope, SCANS);

        return (scope, SCANS);
    }

    function test_registerProtocol() public {
        _registerSampleProtocol();

        (address[] memory scopeRegistry, uint256 scansRegistry) = registry.getSubscription(protocolId);
        assertEq(scansRegistry, 100);
        assertEq(scopeRegistry[0], address(0));
        assertEq(scopeRegistry[1], address(1));
    }

    function test_subscription() public {
        _registerSampleProtocol();

        assertTrue(registry.isSubscribed(protocolId));
    }
}
