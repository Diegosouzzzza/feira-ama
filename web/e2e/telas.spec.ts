import { expect, type Page, test } from "@playwright/test";

// Runs after station.spec.ts: a castanha lot is open, the belt is stopped and the control
// lock is held by another screen.
test.describe.configure({ mode: "serial" });

async function takeControl(page: Page) {
  await page.getByRole("button", { name: /Operar a estação|Assumir o controle/ }).first().click();
  await page.getByLabel("Seu nome").fill("Equipe Telas");
  await page.getByRole("dialog").getByRole("button", { name: /Operar a estação|Assumir o controle/ }).click();
  await expect(page.getByRole("dialog")).toBeHidden();
}

test("histórico lista, filtra e oferece o CSV com os mesmos filtros", async ({ page }) => {
  await page.goto("/historico");
  await expect(page.getByRole("heading", { name: /\d+ inspeç/ })).toBeVisible();
  const rows = page.locator("tbody tr");
  await expect(rows.first()).toBeVisible();

  await page.getByRole("combobox", { name: "Produto" }).click();
  await page.getByRole("option", { name: "Tucumã" }).click();
  await expect(page.getByText("Nenhuma inspeção com estes filtros.")).toBeVisible();
  await expect(page.getByRole("link", { name: "Baixar CSV" })).toHaveAttribute("href", /product_id=tucuma/);

  await page.getByRole("button", { name: "Limpar filtros" }).click();
  await rows.first().click();
  await expect(page.getByRole("dialog").getByText("Classe prevista")).toBeVisible();
});

test("configuração salva o perfil liberado e bloqueia o produto com lote aberto", async ({ page }) => {
  await page.goto("/configuracao");
  await expect(page.getByText("Há um lote aberto deste produto.")).toBeVisible(); // castanha
  await page.getByRole("tab", { name: "Tucumã" }).click();
  await takeControl(page);

  const settle = page.getByLabel("Estabilização antes da foto");
  await settle.fill("9000");
  await expect(page.getByText("Use um número inteiro de 0 a 5000.")).toBeVisible();
  await expect(page.getByRole("button", { name: "Salvar configuração" })).toBeDisabled();

  await settle.fill("650");
  await page.getByRole("button", { name: "Salvar configuração" }).click();
  await expect(page.getByText("Configuração salva.", { exact: false })).toBeVisible();
  await expect(page.getByText("Bancada ainda não calibrada")).toBeHidden();
});

test("diagnóstico entra em manutenção, testa motor e servo e registra os eventos", async ({ page }) => {
  await page.goto("/diagnostico");
  await expect(page.getByRole("heading", { name: "Testes manuais" })).toBeVisible();
  await takeControl(page);

  await page.getByRole("button", { name: "Entrar em manutenção" }).click();
  await expect(page.getByText("Os testes movem a esteira")).toBeVisible();
  await page.getByRole("button", { name: "Ligar a esteira" }).click();
  await expect(page.getByText("Motor ligado pelo tempo pedido.")).toBeVisible();
  await page.getByRole("button", { name: "Mover o servo" }).click();
  await expect(page.getByText("Servo movido", { exact: false })).toBeVisible();
  await page.getByRole("button", { name: "Sair da manutenção" }).click();
  await expect(page.getByRole("button", { name: "Entrar em manutenção" })).toBeVisible();

  const log = page.locator('section[aria-labelledby="events-title"]');
  await expect(log.getByText("TEST_SERVO")).toBeVisible();
  await expect(log.getByText("CONFIG_CHANGED")).toBeVisible();
});

test("as telas novas cabem no celular sem rolagem horizontal", async ({ browser }) => {
  const context = await browser.newContext({ baseURL: "http://127.0.0.1:8010", viewport: { width: 375, height: 812 } });
  const page = await context.newPage();
  for (const path of ["/historico", "/coleta", "/configuracao", "/diagnostico"]) {
    await page.goto(path);
    await expect(page.locator("main h1")).toBeVisible();
    await page.waitForTimeout(300);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    expect(overflow, path).toBeLessThanOrEqual(0);
  }
  await context.close();
});
