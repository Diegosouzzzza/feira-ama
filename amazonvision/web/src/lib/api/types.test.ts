import { describe, expectTypeOf, it } from "vitest";
import type { MachineState, SystemStatus, WsEvent, WsEventOf } from "./types";

describe("contrato gerado do OpenAPI", () => {
  it("estreita WsEvent pelo campo type", () => {
    const handle = (event: WsEvent) => {
      switch (event.type) {
        case "SNAPSHOT":
          expectTypeOf(event.data).toEqualTypeOf<SystemStatus>();
          return event.data.mode;
        case "CONNECTION_LOST":
          return event.data.component;
        default:
          return event.seq;
      }
    };
    expectTypeOf(handle).returns.not.toBeAny();
  });

  it("expõe os estados da máquina como união literal", () => {
    expectTypeOf<"READY">().toExtend<MachineState>();
    expectTypeOf<"VOANDO">().not.toExtend<MachineState>();
  });

  it("WsEventOf seleciona um evento específico", () => {
    expectTypeOf<WsEventOf<"FAULT">["type"]>().toEqualTypeOf<"FAULT">();
    expectTypeOf<"S1_TIMEOUT">().toExtend<WsEventOf<"FAULT">["data"]["code"]>();
  });
});
