import {
  assert,
  describe,
  test,
  clearStore,
  beforeAll,
  afterAll
} from "matchstick-as/assembly/index"
import { Bytes } from "@graphprotocol/graph-ts"
import { ProtocolAdded } from "../generated/schema"
import { ProtocolAdded as ProtocolAddedEvent } from "../generated/Registry/Registry"
import { handleProtocolAdded } from "../src/registry"
import { createProtocolAddedEvent } from "./registry-utils"

// Tests structure (matchstick-as >=0.5.0)
// https://thegraph.com/docs/en/developer/matchstick/#tests-structure-0-5-0

describe("Describe entity assertions", () => {
  beforeAll(() => {
    let protocolId = Bytes.fromI32(1234567890)
    let newProtocolAddedEvent = createProtocolAddedEvent(protocolId)
    handleProtocolAdded(newProtocolAddedEvent)
  })

  afterAll(() => {
    clearStore()
  })

  // For more test scenarios, see:
  // https://thegraph.com/docs/en/developer/matchstick/#write-a-unit-test

  test("ProtocolAdded created and stored", () => {
    assert.entityCount("ProtocolAdded", 1)

    // 0xa16081f360e3847006db660bae1c6d1b2e17ec2a is the default address used in newMockEvent() function
    assert.fieldEquals(
      "ProtocolAdded",
      "0xa16081f360e3847006db660bae1c6d1b2e17ec2a-1",
      "protocolId",
      "1234567890"
    )

    // More assert options:
    // https://thegraph.com/docs/en/developer/matchstick/#asserts
  })
})
