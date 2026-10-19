import { afterEach, describe, expect, it, vi } from "vitest";
import { ApiError, apiGet } from "./client";

afterEach(() => vi.unstubAllGlobals());

describe("apiGet", () => {
  it("prefixes /api and returns parsed JSON", async () => {
    const fetchMock = vi.fn().mockResolvedValue(new Response('{"status":"ok"}', { status: 200 }));
    vi.stubGlobal("fetch", fetchMock);

    await expect(apiGet("/health")).resolves.toEqual({ status: "ok" });
    expect(fetchMock.mock.calls[0]?.[0]).toBe("/api/health");
  });

  it("maps network failure to SERVICE_UNREACHABLE", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("Failed to fetch")));

    await expect(apiGet("/health")).rejects.toMatchObject({
      status: 0,
      code: "SERVICE_UNREACHABLE",
    });
  });

  it("uses the API error code and message when present", async () => {
    const body = JSON.stringify({ code: "INVALID_STATE", message: "Máquina em movimento" });
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(body, { status: 409 })));

    const error = await apiGet("/machine/start").catch((e: unknown) => e);
    expect(error).toBeInstanceOf(ApiError);
    expect(error).toMatchObject({ status: 409, code: "INVALID_STATE", message: "Máquina em movimento" });
  });
});
