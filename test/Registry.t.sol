// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "src/Registry.sol";
import "forge-std/Test.sol";

contract RegistryTest is Test {
    Registry registry;
    bytes32 protocolId;

    function setUp() public {
        registry = new Registry();
        protocolId = keccak256("SAMPLE PROTOCOL");
    }

    function _registerSampleProtocol() internal returns (address[] memory, uint256) {
        uint256 duration = 30 days;

        address[] memory scope = new address[](2);
        scope[0] = address(0);
        scope[1] = address(1);

        registry.registerProtocol{ value: registry.PRICE_PER_DAY() * duration }(protocolId, scope, duration);

        return (scope, duration);
    }

    function test_registerProtocol() public {
        _registerSampleProtocol();

        (address[] memory scopeRegistry, uint256 expirationRegistry) = registry.getSubscription(protocolId);
        assertEq(expirationRegistry, uint256(block.timestamp + 30 days));
        assertEq(scopeRegistry[0], address(0));
        assertEq(scopeRegistry[1], address(1));
    }

    function test_subscription() public {
        (, uint256 duration) = _registerSampleProtocol();

        assertTrue(registry.isSubscribed(protocolId));
        skip(duration + 1);
        assertFalse(registry.isSubscribed(protocolId));
    }
}
