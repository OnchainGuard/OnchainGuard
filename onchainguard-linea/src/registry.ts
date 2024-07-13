import {
  ProtocolAdded as ProtocolAddedEvent,
  ProtocolRemoved as ProtocolRemovedEvent,
  ProtocolScanned as ProtocolScannedEvent
} from "../generated/Registry/Registry"
import {
  ProtocolAdded,
  ProtocolRemoved,
  ProtocolScanned
} from "../generated/schema"

export function handleProtocolAdded(event: ProtocolAddedEvent): void {
  let entity = new ProtocolAdded(
    event.transaction.hash.concatI32(event.logIndex.toI32())
  )
  entity.protocolId = event.params.protocolId

  entity.blockNumber = event.block.number
  entity.blockTimestamp = event.block.timestamp
  entity.transactionHash = event.transaction.hash

  entity.save()
}

export function handleProtocolRemoved(event: ProtocolRemovedEvent): void {
  let entity = new ProtocolRemoved(
    event.transaction.hash.concatI32(event.logIndex.toI32())
  )
  entity.protocolId = event.params.protocolId

  entity.blockNumber = event.block.number
  entity.blockTimestamp = event.block.timestamp
  entity.transactionHash = event.transaction.hash

  entity.save()
}

export function handleProtocolScanned(event: ProtocolScannedEvent): void {
  let entity = new ProtocolScanned(
    event.transaction.hash.concatI32(event.logIndex.toI32())
  )
  entity.protocolId = event.params.protocolId
  entity.proof = event.params.proof

  entity.blockNumber = event.block.number
  entity.blockTimestamp = event.block.timestamp
  entity.transactionHash = event.transaction.hash

  entity.save()
}
