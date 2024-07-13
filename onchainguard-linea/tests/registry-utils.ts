import { newMockEvent } from "matchstick-as"
import { ethereum, Bytes } from "@graphprotocol/graph-ts"
import {
  ProtocolAdded,
  ProtocolRemoved,
  ProtocolScanned
} from "../generated/Registry/Registry"

export function createProtocolAddedEvent(protocolId: Bytes): ProtocolAdded {
  let protocolAddedEvent = changetype<ProtocolAdded>(newMockEvent())

  protocolAddedEvent.parameters = new Array()

  protocolAddedEvent.parameters.push(
    new ethereum.EventParam(
      "protocolId",
      ethereum.Value.fromFixedBytes(protocolId)
    )
  )

  return protocolAddedEvent
}

export function createProtocolRemovedEvent(protocolId: Bytes): ProtocolRemoved {
  let protocolRemovedEvent = changetype<ProtocolRemoved>(newMockEvent())

  protocolRemovedEvent.parameters = new Array()

  protocolRemovedEvent.parameters.push(
    new ethereum.EventParam(
      "protocolId",
      ethereum.Value.fromFixedBytes(protocolId)
    )
  )

  return protocolRemovedEvent
}

export function createProtocolScannedEvent(
  protocolId: Bytes,
  proof: Bytes
): ProtocolScanned {
  let protocolScannedEvent = changetype<ProtocolScanned>(newMockEvent())

  protocolScannedEvent.parameters = new Array()

  protocolScannedEvent.parameters.push(
    new ethereum.EventParam(
      "protocolId",
      ethereum.Value.fromFixedBytes(protocolId)
    )
  )
  protocolScannedEvent.parameters.push(
    new ethereum.EventParam("proof", ethereum.Value.fromFixedBytes(proof))
  )

  return protocolScannedEvent
}
