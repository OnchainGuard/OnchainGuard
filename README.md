# OnchainGuard

![Banner](/assets/banner-ethglobal.png)

An onchain static analyzer for blockchain smart contracts.

> This project has been built during ETHGlobal Brussels. More information [here](https://ethglobal.com/events/brussels).

- Watch the demo video and project page here 👉 [video](https://ethglobal.com/showcase/onchainguard-ki7x6)

## How does it work

![Banner](/assets/workflow.png)

## Deployed smart contracts (alphabetically)

### Arbitrum
- OnchainGuard.sol : [here](https://sepolia.arbiscan.io/address/0xf295e28a89835416804366998caa314c345da77c#contracts)
- BuggyContract.sol (for tests) : [here](https://sepolia.arbiscan.io/address/0xcacc69e073b2dcaa41eafeae7204c2887c6cba31#code)

### Linea
- OnchainGuard.sol : [here](https://sepolia.lineascan.build/address/0x404CB427F1406b3fd456910e7036f5db81e9C1C0#readContract)
- BuggyContract.sol (for tests) : [here](https://sepolia.lineascan.build/address/0xf295e28a89835416804366998caa314c345da77c#code)

### Scroll
- OnchainGuard.sol : [here](https://sepolia.scrollscan.com/address/0xf295e28a89835416804366998caa314c345da77c)
- BuggyContract.sol (for tests) : [here](https://sepolia.scrollscan.com/address/0x404cb427f1406b3fd456910e7036f5db81e9c1c0)

### Zircuit
- OnchainGuard.sol : [here](https://explorer.zircuit.com/address/0x404CB427F1406b3fd456910e7036f5db81e9C1C0)
- BuggyContract.sol (for tests) : [here](https://explorer.zircuit.com/address/0x115F615622d506960e15EA2C218753E55087cED2)

## See all the proofs of the passed scans of your project thanks to a SubGraph
Deployed subgraph : [here](https://testnet.thegraph.com/explorer/subgraphs/8cYbuHVxDpAzXwZqmXaeEVnrLaE6JURvDniY41jBMxTe?view=About&chain=arbitrum-sepolia)

## Coverage

```bash
Ran 1 test suite in 228.73ms (228.12ms CPU time): 8 tests passed, 0 failed, 0 skipped (8 total tests)
| File             | % Lines        | % Statements   | % Branches     | % Funcs       |
|------------------|----------------|----------------|----------------|---------------|
| src/Registry.sol | 96.67% (29/30) | 92.86% (39/42) | 80.00% (16/20) | 100.00% (9/9) |
| Total            | 96.67% (29/30) | 92.86% (39/42) | 80.00% (16/20) | 100.00% (9/9) |
```
