from pathlib import Path
from typing import Any


def _pct(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.1f}%".replace(".", ",")


def _ms(value: float | None) -> str:
    return "—" if value is None else f"{value:.1f} ms".replace(".", ",")


MIN_DEFECT_REJECTION = 0.90
MIN_AUTOMATIC_COVERAGE = 0.70


def readiness(metrics: dict[str, Any]) -> list[str]:
    """Why the model is NOT ready for bench trials (empty = ready), using the plan targets."""
    policy = metrics["test"]["policy"]
    problems = []
    false_approval = policy["defective_false_approval_rate"]
    if false_approval is not None and false_approval > metrics["max_false_approval_target"]:
        problems.append(
            f"B/C aprovadas por engano no teste: {_pct(false_approval)} "
            f"(meta ≤ {_pct(metrics['max_false_approval_target'])})"
        )
    rejected = policy["defective_rejected_rate"]
    if rejected is not None and rejected < MIN_DEFECT_REJECTION:
        problems.append(
            f"B/C rejeitadas automaticamente: {_pct(rejected)} "
            f"(meta ≥ {_pct(MIN_DEFECT_REJECTION)})"
        )
    coverage = policy["automatic_coverage"]
    if coverage is not None and coverage < MIN_AUTOMATIC_COVERAGE:
        problems.append(
            f"só {_pct(coverage)} das peças decididas sem o operador "
            f"(mínimo {_pct(MIN_AUTOMATIC_COVERAGE)}): o modelo ainda não separa as classes"
        )
    if not metrics["validation"]["policy"].get("target_met", False):
        problems.append("nenhum limiar atingiu a meta de falsa aprovação na validação")
    return problems


def write_report(path: Path, manifest: dict[str, Any], metrics: dict[str, Any]) -> None:
    test = metrics["test"]
    policy = test["policy"]
    val_policy = metrics["validation"]["policy"]
    sizes = metrics["split_sizes"]
    order = test["class_order"]
    problems = readiness(metrics)
    lines = [
        f"# Relatório do modelo {manifest['model_id']}",
        "",
        f"Produto: **{manifest['product_id']}** · Arquitetura: {manifest['architecture']} · "
        f"Dataset: {manifest['dataset_version']}",
        "",
        "> As métricas valem para estas fotos e esta bancada. A confiança mostrada na tela é um",
        "> escore do modelo, não uma taxa de acerto. Validar com peças reais antes da feira.",
        "",
        "## Parecer",
        "",
        *(
            [
                "**Pronto para ensaio na bancada**: as metas do plano foram atingidas no teste.",
                "Isso ainda não substitui o ensaio com peças reais e o destino físico observado.",
            ]
            if not problems
            else ["**Ainda não está pronto.** Motivos:", "", *[f"- {p}" for p in problems]]
        ),
        "",
        "## Dados",
        "",
        "| Partição | Peças físicas | Fotos |",
        "|---|---|---|",
        *[
            f"| {name} | {sizes[name]['pieces']} | {sizes[name]['photos']} |"
            for name in ("train", "val", "test")
        ],
        "",
        "Todas as fotos de uma mesma peça ficam na mesma partição.",
        "",
        "## Resultado operacional no teste (limiar congelado)",
        "",
        f"Limiar escolhido na validação: **{policy['threshold']:.2f}** ".replace(".", ",")
        + f"(meta de falsa aprovação de B/C ≤ {_pct(metrics['max_false_approval_target'])}; "
        f"{'atingida' if val_policy.get('target_met') else 'NÃO atingida'} na validação).",
        "",
        "| Indicador | Valor |",
        "|---|---|",
        "| B/C encaminhadas automaticamente aos rejeitados | "
        f"{_pct(policy['defective_rejected_rate'])} |",
        f"| B/C aprovadas por engano | {_pct(policy['defective_false_approval_rate'])} "
        f"({policy['defective_false_approvals']} de {policy['defective_total']}) |",
        f"| A rejeitadas por engano | {_pct(policy['good_wrongly_rejected_rate'])} |",
        f"| Enviadas para revisão | {_pct(policy['review_rate'])} |",
        f"| Decisões automáticas | {_pct(policy['automatic_coverage'])} |",
        f"| Latência da inferência (p50 / p95) | {_ms(test['latency_ms']['p50'])} / "
        f"{_ms(test['latency_ms']['p95'])} |",
        "",
        "## Classificação no teste (sem limiar)",
        "",
        f"Acurácia {_pct(test['accuracy'])} · F1 macro {test['macro_f1']:.3f}",
        "",
        "| Real \\ Previsto | " + " | ".join(order) + " |",
        "|---|" + "---|" * len(order),
        *[
            f"| {order[i]} | " + " | ".join(str(v) for v in row) + " |"
            for i, row in enumerate(test["confusion"])
        ],
        "",
        "| Classe | Precisão | Recall | F1 | Suporte |",
        "|---|---|---|---|---|",
        *[
            f"| {g} | {_pct(m['precision'])} | {_pct(m['recall'])} | "
            f"{m['f1']:.3f} | {m['support']} |"
            for g, m in test["per_class"].items()
        ],
        "",
        "## Treinamento",
        "",
        f"Épocas: {metrics['training']['epochs']} (melhor: {metrics['training']['best_epoch']}) · "
        f"Pré-treinado: {'sim' if metrics['training']['pretrained'] else 'não'} · "
        f"Dispositivo: {metrics['training']['device']} · "
        f"Diferença máxima PyTorch × ONNX: {metrics['export_max_prob_diff']:.2e}",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
