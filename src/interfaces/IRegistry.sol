// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

struct Subscription {
    address[] scope;
    uint256 scans;
    address admin;
}
