const ZONE = "America/Manaus";

const timeFormat = new Intl.DateTimeFormat("pt-BR", {
  timeZone: ZONE,
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
});

const dateTimeFormat = new Intl.DateTimeFormat("pt-BR", {
  timeZone: ZONE,
  day: "2-digit",
  month: "2-digit",
  hour: "2-digit",
  minute: "2-digit",
});

const integer = new Intl.NumberFormat("pt-BR");
const percent = new Intl.NumberFormat("pt-BR", { style: "percent", maximumFractionDigits: 0 });
const percentPrecise = new Intl.NumberFormat("pt-BR", {
  style: "percent",
  minimumFractionDigits: 1,
  maximumFractionDigits: 1,
});

export function formatTime(iso: string | null | undefined): string {
  return iso ? timeFormat.format(new Date(iso)) : "—";
}

export function formatDateTime(iso: string | null | undefined): string {
  return iso ? dateTimeFormat.format(new Date(iso)) : "—";
}

export function formatInt(value: number): string {
  return integer.format(value);
}

export function formatPercent(value: number | null | undefined, precise = false): string {
  if (value === null || value === undefined) return "—";
  return (precise ? percentPrecise : percent).format(value);
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  const units = ["KB", "MB", "GB", "TB"];
  let value = bytes / 1024;
  let unit = 0;
  while (value >= 1024 && unit < units.length - 1) {
    value /= 1024;
    unit++;
  }
  return `${value.toLocaleString("pt-BR", { maximumFractionDigits: value < 10 ? 1 : 0 })} ${units[unit]}`;
}
