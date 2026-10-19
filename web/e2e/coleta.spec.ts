import { expect, test } from "@playwright/test";

test("coleta: fotografa com atalho, revisa e exporta o manifesto", async ({ page }) => {
  await page.goto("/coleta");
  await expect(page.getByRole("heading", { name: "Coleta de fotos" })).toBeVisible();
  await expect(page.getByRole("img", { name: "Imagem ao vivo da câmera da bancada" })).toBeVisible();

  await page.getByRole("button", { name: "Operar a estação" }).first().click();
  await page.getByLabel("Seu nome").fill("Equipe E2E");
  await page.getByRole("dialog").getByRole("button", { name: "Operar a estação" }).click();

  await page.getByLabel("Etiqueta da peça física").fill("E2E-01");
  await page.getByRole("button", { name: "Fotografar como Classe A" }).click();
  await expect(page.getByText("Última foto: peça E2E-01, classe A")).toBeVisible();

  await page.getByRole("button", { name: "Próxima peça" }).click();
  await expect(page.getByLabel("Etiqueta da peça física")).toHaveValue("E2E-02");
  await page.getByRole("heading", { name: "Coleta de fotos" }).click(); // leave the field: shortcuts on
  await page.keyboard.press("0");
  await expect(page.getByText("Última foto: peça E2E-02, sem rótulo")).toBeVisible();

  // Pending filter shows the unlabeled photo; label it C from the review grid.
  const review = page.locator('section[aria-labelledby="review-title"]');
  await expect(review.getByText("E2E-02")).toBeVisible();
  await review.getByRole("button", { name: "Rotular como Classe C" }).click();
  await expect(review.getByText("Nenhuma foto neste filtro.")).toBeVisible();
  await expect(page.getByText("1 foto de 1 peça")).toHaveCount(2); // classes A and C

  await page.getByRole("button", { name: "Exportar para treinamento" }).click();
  const dialog = page.getByRole("dialog");
  await expect(dialog.getByText("2 fotos de 2 peças físicas", { exact: false })).toBeVisible();
  await expect(dialog.getByText("manifest-tucuma.csv", { exact: false }).first()).toBeVisible();
  await dialog.getByRole("button", { name: "Fechar" }).click();

  // Hand the station back so the operation tests start from a free control lock.
  await page.evaluate(async () => {
    const saved = JSON.parse(localStorage.getItem("av-control") ?? "{}") as { token?: string };
    await fetch("/api/control/release", { method: "POST", headers: { "X-Control-Token": saved.token ?? "" } });
  });
});
