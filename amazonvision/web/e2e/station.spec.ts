import { type APIRequestContext, expect, type Page, test } from "@playwright/test";

test.describe.configure({ mode: "serial" });

async function eventCount(request: APIRequestContext, type: string): Promise<number> {
  const events = (await (await request.get("/api/diagnostics/events?limit=200")).json()) as { type: string }[];
  return events.filter((e) => e.type === type).length;
}

async function inspected(page: Page): Promise<number> {
  const value = await page.locator("dt", { hasText: "Inspecionadas" }).locator("xpath=following-sibling::dd").innerText();
  return Number(value.replace(/\D/g, ""));
}

test("operador assume, abre lote e inicia; recarregar não duplica nada", async ({ page, request }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Abra um lote para começar" })).toBeVisible();

  await page.getByRole("button", { name: "Operar a estação" }).first().click();
  await page.getByLabel("Seu nome").fill("Equipe E2E");
  await page.getByRole("dialog").getByRole("button", { name: "Operar a estação" }).click();
  await expect(page.getByText("Operando como")).toBeVisible();

  await page.getByRole("combobox", { name: "Produto" }).click();
  await page.getByRole("option", { name: "Castanha-do-pará" }).click();
  await page.getByRole("button", { name: "Abrir lote" }).click();
  await expect(page.getByRole("banner").getByText("Castanha-do-pará", { exact: true })).toBeVisible();

  await page.getByRole("button", { name: "Iniciar" }).click();
  await expect.poll(() => inspected(page), { timeout: 20_000 }).toBeGreaterThanOrEqual(2);
  await expect(page.getByRole("heading", { name: "Últimas peças" })).toBeVisible();
  await expect(page.locator('section[aria-labelledby="recent-heading"] li').first()).toBeVisible();

  const before = await inspected(page);
  await page.reload();
  await expect(page.getByText("Operando como")).toBeVisible();
  await expect.poll(() => inspected(page)).toBeGreaterThanOrEqual(before);
  await expect(page.locator('section[aria-labelledby="recent-heading"] li').first()).toBeVisible();
  expect(await eventCount(request, "MACHINE_START")).toBe(1);
  expect(await eventCount(request, "LOT_OPENED")).toBe(1);
});

test("outra tela só acompanha e vê os mesmos totais", async ({ browser, request }) => {
  const other = await browser.newContext({ baseURL: "http://127.0.0.1:8010", viewport: { width: 1366, height: 768 } });
  const page = await other.newPage();
  await page.goto("/");
  await expect(page.getByText("Controle com")).toBeVisible();
  await expect(page.getByRole("button", { name: "Iniciar" })).toBeDisabled();
  await expect(page.getByRole("button", { name: "Parar" })).toBeDisabled();

  const status = await (await request.get("/api/status")).json();
  await expect.poll(() => inspected(page)).toBeGreaterThanOrEqual(status.active_lot_summary.inspected);
  await other.close();
});

test("modo feira é somente leitura e cabe sem rolagem em Full HD", async ({ browser }) => {
  const context = await browser.newContext({ baseURL: "http://127.0.0.1:8010", viewport: { width: 1920, height: 1080 } });
  const page = await context.newPage();
  await page.goto("/feira");
  await expect(page.getByText("Castanha-do-pará")).toBeVisible();
  await expect(page.getByRole("button", { name: "Iniciar" })).toHaveCount(0);
  await expect(page.getByRole("heading", { name: "Cada foto ocupa o lugar da classe escolhida pela IA" })).toBeVisible();
  await expect(page.getByText("Como a IA votou")).toBeVisible();
  const scroll = await page.evaluate(() => ({
    vertical: document.documentElement.scrollHeight - window.innerHeight,
    horizontal: document.documentElement.scrollWidth - window.innerWidth,
  }));
  expect(scroll.vertical).toBeLessThanOrEqual(0);
  expect(scroll.horizontal).toBeLessThanOrEqual(0);
  await context.close();
});

test("celular não tem rolagem horizontal", async ({ browser }) => {
  const context = await browser.newContext({ baseURL: "http://127.0.0.1:8010", viewport: { width: 375, height: 812 } });
  const page = await context.newPage();
  await page.goto("/");
  await expect(page.getByText("Inspecionadas")).toBeVisible();
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  expect(overflow).toBeLessThanOrEqual(0);
  await context.close();
});

test("outra pessoa assume o controle e para a máquina", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("Controle com")).toBeVisible();
  await page.getByRole("button", { name: "Assumir o controle" }).click();
  await expect(page.getByRole("dialog")).toContainText("O controle está com Equipe E2E");
  await page.getByLabel("Seu nome").fill("Supervisora");
  await page.getByRole("dialog").getByRole("button", { name: "Assumir o controle" }).click();
  await expect(page.getByText("Operando como")).toBeVisible();

  await page.getByRole("button", { name: "Parar" }).click();
  await expect(page.getByRole("heading", { name: "Desarmada" })).toBeVisible({ timeout: 10_000 });
  await expect(page.getByRole("button", { name: "Pausar" })).toBeDisabled();
});
