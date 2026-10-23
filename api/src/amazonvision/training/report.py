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


def _num(value: float | None) -> str:
    return "—" if value is None else f"{value:.3f}".replace(".", ",")


def write_anomaly_report(path: Path, manifest: dict[str, Any], metrics: dict[str, Any]) -> None:
    """Report of a model trained on good pieces only: what was measured and what was not."""
    test = metrics["test"]
    policy = test["policy"]
    sizes = metrics["split_sizes"]
    edges = metrics["calibration"]
    distances = metrics["distances"]
    known = metrics["known_anomalies"]
    lines = [
        f"# Relatório do modelo {manifest['model_id']}",
        "",
        f"Produto: **{manifest['product_id']}** · Tipo: **detecção de anomalia** "
        f"({manifest['architecture']}) · Dataset: {manifest['dataset_version']}",
        "",
        "> Este modelo aprendeu só como é uma peça **boa**. Na bancada, peça parecida com as",
        "> boas vai para os aprovados (A), peça muito diferente vai para os rejeitados (C) e o",
        "> meio-termo vai para revisão humana. Ele não diz o motivo (mancha, mofo, rachadura):",
        "> só que a peça foge do padrão.",
        "",
        "## Parecer",
        "",
        "**Provisório: não pronto para decidir sozinho.**",
        "",
        "- Nenhuma peça defeituosa real foi medida: não há como saber quantos defeitos ele pega.",
        "- Ele depende do fundo, da luz e da câmera das fotos de treino. **Antes de usar na "
        "bancada, refaça o modelo com 15 a 20 peças boas fotografadas na própria bancada** "
        "(tela Coleta, classe A) e confira os números abaixo de novo.",
        "- Valide com algumas peças ruins de verdade assim que houver: elas devem ir para "
        "rejeitados ou revisão.",
        "",
        "## Dados",
        "",
        "| Partição | Uso | Peças físicas | Fotos |",
        "|---|---|---|---|",
        f"| train | banco de memória das peças boas | {sizes['train']['pieces']} | "
        f"{sizes['train']['photos']} |",
        f"| val | calibração dos limites | {sizes['val']['pieces']} | {sizes['val']['photos']} |",
        f"| test | medição (boas + objetos diferentes) | {sizes['test']['pieces']} | "
        f"{sizes['test']['photos']} |",
        "",
        f"Banco de memória: {metrics['bank']['patches']} retalhos de {metrics['bank']['dims']} "
        f"dimensões; cada foto boa entra girada e espelhada ({metrics['bank']['views_per_photo']} "
        "vistas), porque a peça pode cair em qualquer posição.",
        "",
        "## Calibração",
        "",
        f"Distância das peças boas da validação: mediana {_num(edges['good_median'])}, "
        f"máxima {_num(edges['good_max'])}.",
        "",
        "| Faixa de distância | Decisão |",
        "|---|---|",
        f"| até {_num(edges['approve_edge'])} | aprovada (A) |",
        f"| entre {_num(edges['approve_edge'])} e {_num(edges['reject_edge'])} | revisão humana |",
        f"| acima de {_num(edges['reject_edge'])} | rejeitada (C) |",
        "",
        f"O limite de aprovação deixa passar {_pct(0.95)} das peças boas da validação. O limite de "
        "rejeição é uma estimativa estatística (sem peças ruins para ajustar).",
        "",
        "## Resultado no teste",
        "",
        "| Indicador | Valor |",
        "|---|---|",
        f"| Peças boas rejeitadas por engano | {_pct(policy['good_wrongly_rejected_rate'])} "
        f"(de {policy['good_total']}) |",
        f"| Peças enviadas para revisão | {_pct(policy['review_rate'])} |",
        f"| Latência da inferência (p50 / p95) | {_ms(test['latency_ms']['p50'])} / "
        f"{_ms(test['latency_ms']['p95'])} |",
        f"| Diferença máxima PyTorch × ONNX | {metrics['export_max_prob_diff']:.2e} |",
        "",
        f"Distância no teste: peças boas com mediana {_num(distances['test_good']['median'])} "
        f"e máxima {_num(distances['test_good']['max'])}.",
        "",
    ]
    if known:
        lines += [
            "### Objetos diferentes (não são defeitos reais)",
            "",
            f"Para conferir que o modelo reage ao que é diferente, {known} fotos de outros objetos "
            "foram passadas só no teste. **Isso não mede defeitos do produto**: só mostra que ele "
            "não aprova qualquer coisa.",
            "",
            "| Indicador | Valor |",
            "|---|---|",
            f"| Rejeitados automaticamente | {_pct(policy['defective_rejected_rate'])} |",
            f"| Aprovados por engano | {_pct(policy['defective_false_approval_rate'])} "
            f"({policy['defective_false_approvals']} de {policy['defective_total']}) |",
            f"| Distância (mínima / mediana) | "
            f"{_num(distances['test_known_anomalies']['min'])} / "
            f"{_num(distances['test_known_anomalies']['median'])} |",
            "",
        ]
    lines += [
        "## Como refazer na bancada",
        "",
        "1. Monte a bancada com a luz e o fundo definitivos e configure a região de inspeção.",
        "2. Na tela Coleta, fotografe 15 a 20 peças **boas** (classe A), 3 a 6 fotos cada,",
        "   girando a peça entre as fotos.",
        "3. Exporte o manifesto e rode o comando `anomalia` com o mesmo `--roi` da Configuração.",
        "4. Instale, leia este relatório e ative. Passe algumas peças ruins para conferir.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
