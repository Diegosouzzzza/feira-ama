/** T-0007 → T-0008; a tag without a trailing number gets "-2". */
export function nextPiece(piece: string): string {
  const match = /^(.*?)(\d+)$/.exec(piece);
  if (!match) return `${piece}-2`;
  const [, prefix = "", digits = ""] = match;
  return `${prefix}${String(Number(digits) + 1).padStart(digits.length, "0")}`;
}
