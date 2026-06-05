"""
src/utils/logging.py
Logger estructurado para el proyecto AVAL.
Cada decisión de crédito deja un registro en audit_decisions.jsonl.
"""

import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def get_logger(name: str) -> logging.Logger:
    """
    Retorna un logger configurado para el módulo especificado.
    
    Uso: logger = get_logger(__name__)
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, log_level, logging.INFO))

        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


class AuditLogger:
    """
    Registra cada decisión crediticia en un archivo JSONL inmutable.
    
    Cada línea es un JSON independiente. Se puede auditar con:
        cat logs/audit_decisions.jsonl | python -m json.tool
        jq '.decision' logs/audit_decisions.jsonl
    
    Un auditor de SBS puede reconstruir cualquier decisión
    con solo este archivo y el modelo versionado.
    """

    def __init__(self, log_path: str | Path | None = None):
        if log_path is None:
            project_root = Path(__file__).parent.parent.parent
            log_path = project_root / "logs" / "audit_decisions.jsonl"

        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log_decision(
        self,
        applicant_id: str,
        score_raw: float,
        score_calibrated: float,
        decision: str,
        threshold_applied: float,
        shap_factors: list[dict[str, Any]],
        agent_explanation: str,
        model_version: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Registra una decisión crediticia completa.
        
        Args:
            applicant_id: Identificador del solicitante.
            score_raw: Score del modelo sin calibrar (logit).
            score_calibrated: Probabilidad de default calibrada [0, 1].
            decision: 'APPROVED' | 'REJECTED' | 'MANUAL_REVIEW'
            threshold_applied: Umbral de corte usado en esta decisión.
            shap_factors: Top features con su contribución SHAP.
                Formato: [{"feature": "...", "description": "...", "shap_value": 0.12}, ...]
            agent_explanation: Texto generado por el agente LangChain.
            model_version: Versión/hash del modelo usado (para reproducibilidad).
            metadata: Datos adicionales (horario, canal, versión de API, etc.)
        """
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "applicant_id": applicant_id,
            "decision": decision,
            "score": {
                "raw": round(score_raw, 6),
                "calibrated": round(score_calibrated, 6),
                "threshold": threshold_applied,
            },
            "shap_factors": shap_factors,
            "agent_explanation": agent_explanation,
            "model_version": model_version,
            "metadata": metadata or {},
        }

        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")