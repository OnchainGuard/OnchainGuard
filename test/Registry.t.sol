// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "src/Registry.sol";
import "forge-std/Test.sol";

contract RegistryTest is Test {
    Registry registry;
    bytes32 protocolId;
    
    uint256 SCANS = 100;

    address alice = makeAddr("alice");
    address operator = makeAddr("operator");
    address protocolAdmin = makeAddr("protocol admin");

    function setUp() public {
        vm.prank(operator);
        registry = new Registry();

        protocolId = keccak256("SAMPLE PROTOCOL");
    }

    function _registerSampleProtocol() internal returns (address[] memory, uint256) {
        address[] memory scope = new address[](2);
        scope[0] = address(0);
        scope[1] = address(1);

        uint256 pricePerContractScan = registry.PRICE_PER_CONTRACT_SCAN();
        uint256 price = SCANS * scope.length * pricePerContractScan;

        registry.registerProtocol{ value: price }(protocolId, scope, SCANS, protocolAdmin);

        return (scope, SCANS);
    }

    function _registerSampleProtocol(address[] memory _scope, uint256 _scans) internal returns (address[] memory, uint256) {
        uint256 pricePerContractScan = registry.PRICE_PER_CONTRACT_SCAN();
        uint256 price = _scans * _scope.length * pricePerContractScan;

        registry.registerProtocol{ value: price }(protocolId, _scope, _scans, protocolAdmin);

        return (_scope, _scans);
    }

    function test_registerProtocol() public {
        _registerSampleProtocol();

        (address[] memory scopeRegistry, uint256 scansRegistry, address admin) = registry.getSubscription(protocolId);
        assertEq(scansRegistry, 100);
        assertEq(scopeRegistry[0], address(0));
        assertEq(scopeRegistry[1], address(1));
        assertEq(admin, protocolAdmin);

        assertEq(registry.operator(), operator);
    }

    function test_onlyOperator() public {
        _registerSampleProtocol();

        bytes32[] memory proofs = new bytes32[](1);
        bytes32[] memory protocolIds = new bytes32[](1);
        protocolIds[0] = protocolId;
        proofs[0] = "";

        vm.expectRevert(Registry__OnlyOperator.selector);
        vm.prank(alice);
        registry.postScan(protocolIds, proofs);
    }

    function test_onlyProtocolAdmin() public {
        _registerSampleProtocol();

        address[] memory newScope = new address[](1);
        newScope[0] = address(0);

        uint256 newScans = 21;

        vm.expectRevert(Registry__OnlyProtocolAdmin.selector);
        vm.prank(alice);
        registry.updateSubscription(protocolId, newScope, newScans);
    }

    function test_subscription() public {
        address[] memory scope = new address[](2);
        scope[0] = address(0);
        scope[1] = address(1);

        bytes32[] memory proofs = new bytes32[](1);
        bytes32[] memory protocolIds = new bytes32[](1);
        protocolIds[0] = protocolId;
        proofs[0] = "";

        _registerSampleProtocol(scope, 1);

        assertTrue(registry.isSubscribed(protocolId));

        vm.prank(operator);
        registry.postScan(protocolIds, proofs);

        (, uint256 scansRemaining, ) = registry.getSubscription(protocolId);
        assertEq(scansRemaining, 0);

        vm.prank(operator);
        registry.postScan(protocolIds, proofs);

        (address[] memory scopeAfterDeletion, uint256 scansAfterDeletion, address adminAfterDeletion) = registry.getSubscription(protocolId);
        assertEq(scopeAfterDeletion.length, 0);
        assertEq(scansAfterDeletion, 0);
        assertEq(adminAfterDeletion, address(0));
    }

    function test_postScanInputHandling() public {
        _registerSampleProtocol();

        bytes32[] memory proofs = new bytes32[](2);
        bytes32[] memory protocolIds = new bytes32[](1);
        protocolIds[0] = protocolId;
        proofs[0] = "";
        proofs[1] = "";

        vm.expectRevert(Registry__ArrayLengthsMismatch.selector);
        vm.prank(operator);
        registry.postScan(protocolIds, proofs);
    }
}
