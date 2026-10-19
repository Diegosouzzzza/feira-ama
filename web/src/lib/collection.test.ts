import { describe, expect, it } from "vitest";
import { nextPiece } from "./collection";

describe("nextPiece", () => {
  it("increments the trailing number keeping its width", () => {
    expect(nextPiece("T-0007")).toBe("T-0008");
    expect(nextPiece("T-0099")).toBe("T-0100");
    expect(nextPiece("C-9")).toBe("C-10");
  });

  it("starts a numbered series when there is none", () => {
    expect(nextPiece("tucuma-grande")).toBe("tucuma-grande-2");
  });
});
