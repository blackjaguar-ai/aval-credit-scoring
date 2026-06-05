"""
src/utils/config.py
Carga la configuración central del proyecto desde configs/config.yaml.
Un solo punto de entrada. Sin magia, sin globals ocultos.
"""

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

load_dotenv()


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """
    Carga y retorna el config.yaml del proyecto.
    
    Si config_path no se especifica, busca configs/config.yaml
    relativo a la raíz del proyecto (dos niveles arriba de este archivo).
    """
    if config_path is None:
        project_root = Path(__file__).parent.parent.parent
        config_path = project_root / "configs" / "config.yaml"

    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Config no encontrado en {config_path}. "
            "Asegúrate de ejecutar desde la raíz del proyecto."
        )

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config


def get_project_root() -> Path:
    """Retorna la raíz del proyecto como objeto Path."""
    return Path(__file__).parent.parent.parent


def get_data_path(subdir: str, filename: str | None = None) -> Path:
    """
    Construye rutas a subdirectorios de data de forma segura.
    
    Uso:
        get_data_path("raw", "application_train.csv")
        get_data_path("processed")
    """
    root = get_project_root()
    config = load_config()
    
    subdir_map = {
        "raw": config["data"]["raw_dir"],
        "processed": config["data"]["processed_dir"],
        "splits": config["data"]["splits_dir"],
    }
    
    if subdir not in subdir_map:
        raise ValueError(f"Subdirectorio desconocido: '{subdir}'. Usa: {list(subdir_map.keys())}")
    
    path = root / subdir_map[subdir]
    
    if filename:
        return path / filename
    return path