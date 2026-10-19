export class ApiError extends Error {
  readonly status: number;
  readonly code: string | undefined;

  constructor(status: number, message: string, code?: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
  }
}

export async function apiGet<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`/api${path}`, { ...init, headers: { Accept: "application/json" } });
  } catch {
    throw new ApiError(0, "Serviço local indisponível", "SERVICE_UNREACHABLE");
  }
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as {
      code?: string;
      message?: string;
    } | null;
    throw new ApiError(response.status, body?.message ?? `Erro ${response.status}`, body?.code);
  }
  return (await response.json()) as T;
}
