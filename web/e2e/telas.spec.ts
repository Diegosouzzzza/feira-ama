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

test("configuração salva a região de inspeção (ROI) e o comando da coleta a inclui", async ({ page, request }) => {
  await page.goto("/configuracao");
  await page.getByRole("tab", { name: "Tucumã" }).click();
  await takeControl(page);

  await page.getByLabel("Recortar a imagem").check();
  await page.getByLabel("Da esquerda").fill("20");
  await page.getByLabel("Do topo").fill("10");
  await page.getByLabel("Largura").fill("85"); // 20 + 85 > 100: overflow
  await expect(page.getByText("Posição + largura não pode passar de 100%.")).toBeVisible();
  await page.getByLabel("Largura").fill("60");
  await page.getByLabel("Altura").fill("80");
  await expect(page.getByRole("button", { name: "Salvar configuração" })).toBeEnabled();
  await page.getByRole("button", { name: "Salvar configuração" }).click();
  await expect(page.getByText("Configuração salva.", { exact: false }).last()).toBeVisible();

  const saved = await (await request.get("/api/products/tucuma/config")).json();
  expect(saved.roi).toEqual({ x: 0.2, y: 0.1, width: 0.6, height: 0.8 });

  const captured = await request.post("/api/dataset/capture", {
    headers: await page.evaluate(() => ({ "X-Control-Token": JSON.parse(localStorage.getItem("av-control") ?? "{}").token })),
    data: { product_id: "tucuma", physical_sample_id: "ROI-1", collection_session: "e2e", label: "A" },
  });
  expect(captured.ok()).toBeTruthy();
  const exported = await request.post("/api/dataset/export", {
    headers: await page.evaluate(() => ({ "X-Control-Token": JSON.parse(localStorage.getItem("av-control") ?? "{}").token })),
    data: { product_id: "tucuma" },
  });
  const command = (await exported.json()).command as string;
  expect(command).toContain("--roi 0.2,0.1,0.6,0.8");

  // Leave it unchecked so the station tests that follow see the full frame again.
  await page.getByLabel("Recortar a imagem").uncheck();
  await page.getByRole("button", { name: "Salvar configuração" }).click();
  await expect(page.getByText("Configuração salva.", { exact: false }).last()).toBeVisible();
});

test("configuração faz backup, baixa e apaga, e limpa fotos antigas", async ({ page, request }) => {
  await page.goto("/configuracao");
  await takeControl(page);

  const section = page.locator('section[aria-labelledby="backups-title"]');
  await expect(section.getByText("Nenhum backup ainda.")).toBeVisible();

  await section.getByRole("button", { name: "Fazer backup agora" }).click();
  await expect(section.getByText("Nenhum backup ainda.")).toBeHidden();
  const row = section.locator("li").first();
  await expect(row).toContainText("inspeções");
  const downloadHref = await row.getByRole("link", { name: "Baixar" }).getAttribute("href");
  expect(downloadHref).toMatch(/\/api\/backups\/backup-.*\.zip\/file/);
  const download = await request.get(downloadHref!);
  expect(download.status()).toBe(200);
  expect(download.headers()["content-type"]).toBe("application/zip");

  await row.getByRole("button", { name: /Apagar backup de/ }).click();
  await expect(section.getByText("Nenhum backup ainda.")).toBeVisible();

  await section.getByRole("button", { name: "Limpar fotos antigas" }).click();
  await expect(page.getByText(/foto\(s\) de inspeções antigas apagada|Nenhuma foto antiga para apagar/)).toBeVisible();
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
  await expect(log.getByText("CONFIG_CHANGED").first()).toBeVisible();
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
