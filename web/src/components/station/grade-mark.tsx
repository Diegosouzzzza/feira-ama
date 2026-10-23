import { Check, X } from "lucide-react";
import type { InspectionOut } from "@/lib/api/types";
import { GRADE, type Tone } from "@/lib/labels";
import { cn } from "@/lib/utils";
import { TONE } from "./tone";

/** Inconclusive pieces keep the review tone even after the operator decides. */
export function inspectionTone(inspection: InspectionOut): Tone {
  if (inspection.auto_decision === "REVIEW") return "review";
  return inspection.predicted_grade ? GRADE[inspection.predicted_grade].tone : "review";
}

const SIZES = {
  sm: { box: "size-9 text-xl rounded-sm", icon: "size-5" },
  md: { box: "size-20 text-5xl rounded-md", icon: "size-10" },
  lg: { box: "size-16 text-4xl rounded-lg sm:size-20 sm:text-5xl", icon: "size-8 sm:size-10" },
  xl: {
    box: "size-24 text-7xl rounded-lg sm:size-32 sm:text-[5.5rem]",
    icon: "size-12 sm:size-16",
  },
  feira: {
    box: "size-[clamp(8rem,15vh,12rem)] text-[clamp(6rem,12vh,9.5rem)] rounded-xl",
    icon: "size-[clamp(4rem,8vh,6rem)]",
  },
} as const;

/** The grade letter as a solid block; text elsewhere always carries the meaning.
 *  Inconclusive pieces show "?" while undecided, then the person's call (✓ approved,
 *  ✕ rejected) on the review colour; never the model's guess, which would read as a
 *  confirmed class. */
export function GradeMark({
  inspection,
  size = "md",
  variant = "solid",
  className,
}: {
  inspection: InspectionOut;
  size?: keyof typeof SIZES;
  /** solid: white on the class colour (over photos, far away); soft: tint + coloured mark. */
  variant?: "solid" | "soft";
  className?: string;
}) {
  const tone = TONE[inspectionTone(inspection)];
  const review = inspection.auto_decision === "REVIEW";
  const decidedByOperator = review && inspection.decided_by === "operator";
  return (
    <span
      aria-hidden
      className={cn(
        "font-display inline-grid shrink-0 place-items-center",
        variant === "solid" ? cn("text-white", tone.solid) : cn(tone.soft, tone.text),
        SIZES[size].box,
        className,
      )}
    >
      {decidedByOperator ? (
        inspection.final_decision === "APPROVED" ? (
          <Check className={SIZES[size].icon} strokeWidth={variant === "solid" ? 3 : 2.25} />
        ) : (
          <X className={SIZES[size].icon} strokeWidth={variant === "solid" ? 3 : 2.25} />
        )
      ) : review ? (
        "?"
      ) : (
        (inspection.predicted_grade ?? "?")
      )}
    </span>
  );
}
