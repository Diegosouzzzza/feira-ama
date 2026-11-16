import {
  Activity,
  Boxes,
  Camera,
  History,
  type LucideIcon,
  Menu,
  Presentation,
  Scale,
  ScanLine,
  Settings,
} from "lucide-react";
import { useState } from "react";
import { NavLink, Outlet } from "react-router";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTitle, SheetTrigger } from "@/components/ui/sheet";
import { cn } from "@/lib/utils";

type NavItem = { to: string; label: string; icon: LucideIcon };

const GROUPS: { title: string; items: NavItem[] }[] = [
  {
    title: "Estação",
    items: [
      { to: "/", label: "Operação", icon: ScanLine },
      { to: "/feira", label: "Modo feira", icon: Presentation },
      { to: "/historico", label: "Histórico", icon: History },
    ],
  },
  {
    title: "Modelo",
    items: [
      { to: "/coleta", label: "Coleta", icon: Camera },
      { to: "/concordancia", label: "Concordância", icon: Scale },
      { to: "/modelos", label: "Modelos", icon: Boxes },
    ],
  },
  {
    title: "Sistema",
    items: [
      { to: "/configuracao", label: "Configuração", icon: Settings },
      { to: "/diagnostico", label: "Diagnóstico", icon: Activity },
    ],
  },
];

const ITEM = "flex items-center gap-3 rounded-lg px-3 py-2.5 text-[0.925rem] font-medium transition-colors";
const ITEM_IDLE = "text-muted-foreground hover:bg-muted hover:text-foreground";

function SidebarBrand() {
  return (
    <div className="flex min-w-0 items-center gap-2.5">
      <img src="/favicon.svg" alt="" className="size-8 shrink-0" />
      <p className="font-wide truncate font-semibold tracking-tight">AmazonVision 4.0</p>
    </div>
  );
}

function SidebarBody({ onNavigate }: { onNavigate?: () => void }) {
  return (
    <div className="flex h-full flex-col">
      <div className="flex h-14 shrink-0 items-center px-4">
        <SidebarBrand />
      </div>
      <nav aria-label="Telas" className="flex-1 space-y-5 overflow-y-auto px-3 py-4">
        {GROUPS.map((group) => (
          <div key={group.title}>
            <p className="mb-1.5 px-3 text-xs font-medium text-muted-foreground">{group.title}</p>
            <ul className="space-y-0.5">
              {group.items.map((item) => (
                <li key={item.to}>
                  <NavLink
                    to={item.to}
                    end
                    onClick={onNavigate}
                    className={({ isActive }) => cn(ITEM, isActive ? "bg-primary/10 text-primary" : ITEM_IDLE)}
                  >
                    <item.icon className="size-5 shrink-0" aria-hidden />
                    {item.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </nav>
    </div>
  );
}

/** Menu button for narrow screens; lives inside the top bar so there is a single banner. */
export function MobileNav() {
  const [open, setOpen] = useState(false);
  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" aria-label="Abrir menu" className="-ml-2 md:hidden">
          <Menu className="size-5" />
        </Button>
      </SheetTrigger>
      <SheetContent aria-describedby={undefined}>
        <SheetTitle className="sr-only">Menu de navegação</SheetTitle>
        <SidebarBody onNavigate={() => setOpen(false)} />
      </SheetContent>
    </Sheet>
  );
}

/** Fixed sidebar on wide screens; every team screen renders to its right. */
export function AppLayout() {
  return (
    <>
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-64 flex-col border-r bg-background md:flex">
        <SidebarBody />
      </aside>
      <div className="md:pl-64">
        <Outlet />
      </div>
    </>
  );
}
