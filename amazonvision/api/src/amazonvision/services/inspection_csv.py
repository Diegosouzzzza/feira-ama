"""Inspection history as CSV for spreadsheets (Excel pt-BR: ";" separator, decimal comma)."""

import csv
import io
import json
import sqlite3
from collections.abc import Iterable

from amazonvision.core.clock import from_db

HEADER = (
    "inspecao",
    "data_hora_local",
    "lote",
    "produto",
    "modelo",
    "classe_prevista",
    "confianca",
    "escore_A",
    "escore_B",
    "escore_C",
    "limiar",
    "decisao_automatica",
    "motivo_revisao",
    "decisao_final",
    "decidido_por",
    "latencia_ms",
    "situacao_ciclo",
    "imagem_sha256",
)

_DECISION = {"APPROVED": "Aprovado", "REJECTED": "Rejeitado", "REVIEW": "Revisão"}
_REASON = {
    "LOW_CONFIDENCE": "Confiança baixa",
    "AMBIGUOUS": "Classes empatadas",
    "INVALID_IMAGE": "Imagem inválida",
}
_DECIDED_BY = {"auto": "Automático", "operator": "Operador"}
_CYCLE = {"running": "Em andamento", "completed": "Concluído", "aborted": "Interrompido"}
_FORMULA_START = ("=", "+", "-", "@", "\t", "\r")


def safe_cell(value: str) -> str:
    """A cell that starts like a formula is shown as text, never executed by the spreadsheet."""
    return "'" + value if value.startswith(_FORMULA_START) else value


def _number(value: float | None, digits: int) -> str:
    return "" if value is None else f"{value:.{digits}f}".replace(".", ",")


def _row(r: sqlite3.Row) -> list[str]:
    scores = json.loads(r["scores_json"]) if r["scores_json"] else {}
    values = [
        str(r["id"]),
        from_db(r["captured_at"]).astimezone().strftime("%d/%m/%Y %H:%M:%S"),
        str(r["lot_id"]),
        r["product_id"],
        r["model_id"] or "",
        r["predicted_grade"] or "",
        _number(r["confidence"], 3),
        *(_number(scores.get(g), 3) for g in ("A", "B", "C")),
        _number(r["policy_threshold"], 2),
        _DECISION.get(r["auto_decision"], r["auto_decision"]),
        _REASON.get(r["review_reason"] or "", r["review_reason"] or ""),
        _DECISION.get(r["final_decision"] or "", r["final_decision"] or ""),
        _DECIDED_BY.get(r["decided_by"] or "", r["decided_by"] or ""),
        _number(r["latency_ms"], 1),
        _CYCLE.get(r["cycle_status"], r["cycle_status"]),
        r["image_sha256"],
    ]
    return [safe_cell(v) for v in values]


def render(rows: Iterable[sqlite3.Row]) -> bytes:
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=";", lineterminator="\r\n")
    writer.writerow(HEADER)
    for r in rows:
        writer.writerow(_row(r))
    return ("﻿" + buffer.getvalue()).encode("utf-8")  # BOM: Excel reads it as UTF-8
