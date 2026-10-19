import { useQuery } from "@tanstack/react-query";
import { apiGet } from "./client";
import type { components } from "./schema";

export type Health = components["schemas"]["HealthResponse"];

export function useHealth() {
  return useQuery({
    queryKey: ["health"],
    queryFn: ({ signal }) => apiGet<Health>("/health", { signal }),
    refetchInterval: 5_000,
    retry: false,
  });
}
