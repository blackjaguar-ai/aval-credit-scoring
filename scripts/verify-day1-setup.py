"""
scripts/verify-day1-setup.py

Script de verificación del Día 1.
Benchmark del roadmap: xgboost, shap, optuna importan sin error en local Y en VPS.

Ejecutar:
    python scripts/verify-day1-setup.py

Salida esperada: ✅ en cada línea. Si hay ❌, revisar requirements.txt.
"""

import sys
import importlib
from pathlib import Path


def check_import(module_name: str, version_attr: str = "__version__") -> tuple[bool, str]:
    try:
        mod = importlib.import_module(module_name)
        version = getattr(mod, version_attr, "version desconocida")
        return True, str(version)
    except ImportError as e:
        return False, str(e)


def check_config() -> tuple[bool, str]:
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from src.utils.config import load_config
        config = load_config()
        return True, f"proyecto='{config['project']['name']}'"
    except Exception as e:
        return False, str(e)


def check_directory_structure() -> tuple[bool, str]:
    project_root = Path(__file__).parent.parent
    required_dirs = [
        "data/raw", "data/processed", "data/splits",
        "src/features", "src/models", "src/explainability",
        "src/agent", "src/utils",
        "api", "dashboard", "models", "notebooks", "tests", "configs"
    ]
    missing = [d for d in required_dirs if not (project_root / d).exists()]
    if missing:
        return False, f"Directorios faltantes: {missing}"
    return True, f"{len(required_dirs)} directorios presentes"


checks = [
    ("xgboost", lambda: check_import("xgboost")),
    ("shap", lambda: check_import("shap")),
    ("optuna", lambda: check_import("optuna")),
    ("lightgbm", lambda: check_import("lightgbm")),
    ("catboost", lambda: check_import("catboost")),
    ("scikit-learn", lambda: check_import("sklearn", "__version__")),
    ("pandas", lambda: check_import("pandas")),
    ("numpy", lambda: check_import("numpy")),
    ("fastapi", lambda: check_import("fastapi")),
    ("langchain", lambda: check_import("langchain")),
    ("mlflow", lambda: check_import("mlflow")),
    ("streamlit", lambda: check_import("streamlit")),
    ("Estructura de directorios", check_directory_structure),
    ("Config YAML", check_config),
]

print(f"\n{'='*60}")
print(f"  AVAL — Verificación Día 1")
print(f"  Python {sys.version}")
print(f"{'='*60}\n")

all_passed = True
for name, check_fn in checks:
    ok, detail = check_fn()
    status = "✅" if ok else "❌"
    print(f"  {status}  {name:<30} {detail}")
    if not ok:
        all_passed = False

print(f"\n{'='*60}")
if all_passed:
    print("  ✅ Día 1 completo. Entorno operativo.")
else:
    print("  ❌ Hay problemas. Resolver antes de avanzar al Día 2.")
print(f"{'='*60}\n")

sys.exit(0 if all_passed else 1)