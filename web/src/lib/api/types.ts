import type { components } from "./schema";

type Schemas = components["schemas"];

export type ApiErrorBody = Schemas["ApiErrorBody"];
export type ErrorCode = Schemas["ErrorCode"];
export type SystemStatus = Schemas["SystemStatus"];
export type MachineState = Schemas["MachineState"];
export type FaultCode = Schemas["FaultCode"];
export type Grade = Schemas["Grade"];
export type Destination = Schemas["Destination"];
export type AutoDecision = Schemas["AutoDecision"];
export type ProductOut = Schemas["ProductOut"];
export type LotOut = Schemas["LotOut"];
export type LotSummary = Schemas["LotSummary"];
export type LotCreate = Schemas["LotCreate"];
export type CycleOut = Schemas["CycleOut"];
export type InspectionOut = Schemas["InspectionOut"];
export type MachineCommandRequest = Schemas["MachineCommandRequest"];
export type MachineCommandResult = Schemas["MachineCommandResult"];
export type WsEvent = Schemas["WsEvent"];
export type WsEventType = WsEvent["type"];
export type WsEventOf<T extends WsEventType> = Extract<WsEvent, { type: T }>;
