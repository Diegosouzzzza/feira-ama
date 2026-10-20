import type { ApiErrorBody } from "./types";

export class ApiError extends Error {
  readonly status: number;
  readonly code: string | undefined;
  readonly recovery: string | null;

  constructor(status: number, message: string, code?: string, recovery: string | null = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.recovery = recovery;
  }
}

async function request<T>(path: string, init: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`/api${path}`, init);
  } catch {
    throw new ApiError(
      0,
      "Serviço local indisponível",
      "SERVICE_UNREACHABLE",
      "Verifique se o AmazonVision está em execução.",
    );
  }
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as Partial<ApiErrorBody> | null;
    throw new ApiError(
      response.status,
      body?.message ?? `Erro ${response.status}`,
      body?.code,
      body?.recovery ?? null,
    );
  }
  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}

export function apiGet<T>(path: string, init?: RequestInit): Promise<T> {
  return request<T>(path, { ...init, headers: { Accept: "application/json" } });
}

function send<T>(method: string, path: string, body: unknown, token: string | null | undefined): Promise<T> {
  const headers: Record<string, string> = {
    Accept: "application/json",
    "Content-Type": "application/json",
  };
  if (token) headers["X-Control-Token"] = token;
  return request<T>(path, {
    method,
    headers,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
}

export function apiPost<T>(path: string, body?: unknown, token?: string | null): Promise<T> {
  return send<T>("POST", path, body, token);
}

export function apiPatch<T>(path: string, body: unknown, token?: string | null): Promise<T> {
  return send<T>("PATCH", path, body, token);
}

export function apiPut<T>(path: string, body: unknown, token?: string | null): Promise<T> {
  return send<T>("PUT", path, body, token);
}

export function apiDelete<T>(path: string, token?: string | null): Promise<T> {
  return send<T>("DELETE", path, undefined, token);
}
