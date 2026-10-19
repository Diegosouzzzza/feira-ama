import type { Tone } from "@/lib/labels";

export const TONE: Record<Tone, { text: string; soft: string; solid: string; border: string }> = {
  a: { text: "text-grade-a", soft: "bg-grade-a-soft", solid: "bg-grade-a", border: "border-grade-a" },
  b: { text: "text-grade-b", soft: "bg-grade-b-soft", solid: "bg-grade-b", border: "border-grade-b" },
  c: { text: "text-grade-c", soft: "bg-grade-c-soft", solid: "bg-grade-c", border: "border-grade-c" },
  review: { text: "text-review", soft: "bg-review-soft", solid: "bg-review", border: "border-review" },
  fault: { text: "text-fault", soft: "bg-fault-soft", solid: "bg-fault", border: "border-fault" },
  neutral: {
    text: "text-muted-foreground",
    soft: "bg-muted",
    solid: "bg-muted-foreground",
    border: "border-border",
  },
};
