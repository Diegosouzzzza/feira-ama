import { expect, test } from "@playwright/test";

// Runs after coleta.spec.ts: two tucumã photos exist in the dataset (E2E-01, E2E-02).
test("concordância: rotula às cegas e mostra a discordância no resumo", async ({ page, request }) => {
  const session = "e2e-criterios";
  await page.goto("/concordancia");
  await expect(page.getByRole("heading", { name: "Teste de concordância" })).toBeVisible();

  await page.getByLabel("Seu nome").fill("Equipe E2E A");
  await page.getByLabel("Rodada").fill(session);
  await expect(page.getByText("Ainda não há duas pessoas")).toBeVisible();

  const next = await (
    await request.get(`/api/dataset/agreement/next?product_id=tucuma&session=${session}&reviewer=Equipe%20E2E%20A`)
  ).json();
  expect(next).not.toBeNull();
  const firstSampleId: number = next.sample.id;

  await page.getByRole("button", { name: "Rotular como Classe A" }).click();
  await expect(page.getByText(/foto[s]? restante/)).toBeVisible();

  // Second reviewer disagrees on the same photo, entirely through the API (stays blind).
  const submitted = await request.post("/api/dataset/agreement/labels", {
    data: { product_id: "tucuma", session, sample_id: firstSampleId, reviewer: "Equipe E2E B", label: "C" },
  });
  expect(submitted.ok()).toBeTruthy();

  await page.reload();
  await expect(page.getByText("Resumo da rodada")).toBeVisible();
  await expect(page.getByText("Equipe E2E A, Equipe E2E B")).toBeVisible();
  await expect(page.getByText("vocês discordaram", { exact: false })).toBeVisible();

  const summary = await (
    await request.get(`/api/dataset/agreement/summary?product_id=tucuma&session=${session}`)
  ).json();
  expect(summary.compared).toBe(1);
  expect(summary.agreed).toBe(0);
  expect(summary.disagreements[0].labels).toEqual({ "Equipe E2E A": "A", "Equipe E2E B": "C" });
});
