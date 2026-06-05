# AVAL — Scoring Crediticio Alternativo

**El problema:** En LATAM, ~70% de adultos tiene acceso limitado o nulo al sistema financiero formal. No porque sean riesgosos, sino porque nunca tuvieron crédito y el buró no tiene historial que reportar. La consecuencia: los sistemas de scoring tradicionales los rechazan por definición, no por riesgo real.

**Lo que AVAL hace:** Evalúa a esos clientes usando señales alternativas —comportamiento de pago, regularidad de actividad, patrones digitales— construyendo un score que no depende del historial bancario. El resultado no es "un modelo con buen AUC". Es una **curva de ganancia esperada** que le dice a la fintech: *"con tu apetito de riesgo, puedes aprobar 12% más de solicitudes manteniendo la mora bajo el umbral que ya tienes"*.

---

## Diferencial frente al scoring genérico

| Componente | Scoring genérico | AVAL |
|---|---|---|
| Señales | Historial buró | Variables alternativas (behavioral, digital, telco) |
| Entregable | Score numérico | Curva aprobación/mora con punto óptimo |
| Explicabilidad | Ninguna o básica | SHAP por decisión + explicación en lenguaje natural |
| Sesgo | No atendido | Reject inference + análisis de fairness documentado |
| Auditabilidad | Nula | Registro inmutable por decisión, apto revisión SBS |

---

## Arquitectura del sistema

```
Señales alternativas
(comportamiento, digital, telco)
         │
         ▼
Feature Pipeline ──── [feature-pipeline-alternative-signals.py]
         │
         ▼
XGBoost + Calibración ─── Comparado contra LightGBM/CatBoost
         │
         ├── SHAP (explicación por decisión)
         │
         ▼
Agente LangChain ──── Traduce SHAP a lenguaje natural
         │
         ▼
FastAPI /predict ──── score + decisión + explicación + reporte
         │
         ▼
Dashboard Streamlit ── Factor wow: thin-file aprobado vs. rechazo tradicional
```

---

## Stack técnico

- **Modelado:** XGBoost · LightGBM · CatBoost · scikit-learn · Optuna
- **Explainability:** SHAP · Scorecard WoE/IV
- **Capa agéntica:** LangChain · GPT 5.4 mini (intercambiable)
- **API:** FastAPI · Pydantic
- **Despliegue:** Docker · docker-compose
- **Dashboard:** Streamlit
- **Tracking:** MLflow
- **Datos:** Home Credit Default Risk (Kaggle)

---

## Lo que el sistema atiende explícitamente

1. **Reject inference** — El modelo no aprende solo de aprobados. Técnica de reweighting con supuesto MAR declarado.
2. **Costo asimétrico** — El umbral se deriva de la curva de ganancia esperada, no de F1 o Youden.
3. **Fairness** — Análisis de disparidad de aprobación por grupos. Cada variable top justificada como legítima ante la SBS.
4. **Auditabilidad** — Cada decisión genera un registro JSONL con score, factores SHAP, explicación y timestamp.

---

## Instalación y ejecución local

```bash
# Clonar y configurar
git clone https://github.com/blackjaguar-ai/aval-credit-scoring.git
cd aval-credit-scoring

# Entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencias (versiones fijas)
pip install -r requirements.txt

# Variables de entorno
cp .env.example .env
# Editar .env con tus claves

# Verificar que el entorno está operativo (benchmark del Día 1)
python scripts/verify-day1-setup.py

# Despliegue con Docker
docker-compose up -d
```

---

## Frontera simulación/realidad

AVAL corre sobre Home Credit (Kaggle). Eso es una credencial de capacidad, no un producto vendible. El valor real nace cuando se conecta la data interna del cliente —transaccional, telco, digital— que es exactamente la data que el sistema está diseñado para consumir. La arquitectura no cambia; cambia el origen de las señales.

---

## Estado del proyecto

| Semana | Foco | Estado |
|---|---|---|
| S1 | Datos, features y baseline | 🔄 En progreso |
| S2 | Modelado, comparación y calibración | ⏳ Pendiente |
| S3 | Explainability, agente y curva | ⏳ Pendiente |
| S3.5 | Despliegue y cierre | ⏳ Pendiente |

---

*Sistema construido en solitario. Toda decisión técnica es defendible por sus números, no por su nombre.*