/** Filters of the Histórico screen and the query string shared by the list and the CSV. */

export const ALL = "all";

export interface Filters {
  product: string;
  lot: string;
  grade: string;
  outcome: string;
  from: string; // yyyy-mm-dd, local day
  to: string;
}

export const EMPTY: Filters = { product: ALL, lot: "", grade: ALL, outcome: ALL, from: "", to: "" };

function localDay(day: string, offsetDays = 0): string {
  const date = new Date(`${day}T00:00:00`);
  date.setDate(date.getDate() + offsetDays);
  return date.toISOString();
}

/** Query string shared by the listing and the CSV download. */
export function filterParams(filters: Filters): URLSearchParams {
  const params = new URLSearchParams();
  if (filters.product !== ALL) params.set("product_id", filters.product);
  if (/^\d+$/.test(filters.lot)) params.set("lot_id", filters.lot);
  if (filters.grade !== ALL) params.set("grade", filters.grade);
  if (filters.outcome !== ALL) params.set("outcome", filters.outcome);
  if (filters.from) params.set("from", localDay(filters.from));
  if (filters.to) params.set("to", localDay(filters.to, 1)); // the whole end day
  return params;
}
