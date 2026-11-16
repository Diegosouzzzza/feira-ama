import { toast } from "sonner";
import { ApiError } from "@/lib/api/client";

/** Show what went wrong and what to do, in the interface's voice. */
export function notifyError(error: unknown): void {
  if (error instanceof ApiError) {
    toast.error(error.message, { description: error.recovery ?? undefined });
    return;
  }
  toast.error("A ação não foi concluída.", { description: "Tente de novo em alguns segundos." });
}
