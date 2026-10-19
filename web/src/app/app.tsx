import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useEffect } from "react";
import { createBrowserRouter, RouterProvider } from "react-router";
import { Toaster } from "@/components/ui/sonner";
import { startRealtime } from "@/lib/realtime/store";
import { FeiraPage } from "@/pages/feira";
import { NaoEncontradaPage } from "@/pages/nao-encontrada";
import { OperacaoPage } from "@/pages/operacao";

const queryClient = new QueryClient({
  defaultOptions: { queries: { refetchOnWindowFocus: false } },
});

const router = createBrowserRouter([
  { index: true, element: <OperacaoPage /> },
  { path: "feira", element: <FeiraPage /> },
  { path: "*", element: <NaoEncontradaPage /> },
]);

export function App() {
  useEffect(() => startRealtime(), []);
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      <Toaster position="top-center" richColors closeButton />
    </QueryClientProvider>
  );
}
