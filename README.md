# 🎧 Hiver AI Support Agent & Evaluation System (`@SpotifyCares`)

> **Hiver SDE Intern Take-Home Project**  
> An evaluation-first AI Customer Support system for Twitter interactions that classifies intents, synthesizes historically-grounded replies, and reliably decides human escalations with auditable reasoning.

---

## ⚡ Quickstart (< 1 Minute Reproduction)

### 1. Clone & Setup Environment
```bash
git clone https://github.com/jashann016/Hiver-Ai-Support-Agent.git
cd Hiver-Ai-Support-Agent
pip install -r requirements.txt
```

### 2. Run the Benchmark Evaluation Suite
```bash
python run_eval.py
```

This single command evaluates **Baseline 0**, **Baseline 1**, **Standard RAG**, and the **Proposed Agentic RAG** across the 500-sample hand-curated Golden Evaluation Dataset (2,000 total test executions), printing comparative metrics and exporting `report/benchmark_results.json`.

---

## 📊 Headline Benchmark Results (2,000 Total Evaluations)

| Model Architecture | Intent F1 | Escalation F1 | Under-Escalation Safety Risk (Lower is better) | LLM Judge Quality (1-5) |
|---|:---:|:---:|:---:|:---:|
| **Baseline 0 (Trivial: Rule/Static)** | `0.185` | `0.118` | `93.7%` | `3.13` |
| **Baseline 1 (Simple: Heuristic Rule)** | `0.332` | `0.582` | `48.0%` | `3.17` |
| **Baseline 2 (Standard RAG Agent)** | `0.676` | `0.587` | `36.2%` | `3.88` |
| **Model 3 (Proposed: Agentic RAG + Self-Critique)** | **`0.656`** | **`0.587`** | **`36.2%`** | **`3.82`** |

---

## 📁 Repository Structure

```
Hiver-Ai-Support-Agent/
├── data/
│   ├── golden_eval_set.json      # 500 hand-curated & stratified golden test samples
│   ├── raw/                      # Raw conversational dataset samples
│   └── processed/                # Cleaned thread pairs
├── src/
│   ├── agentic_rag.py            # Proposed Agentic RAG Engine (Multi-Hop + Self-Critique)
│   ├── agent.py                  # Core Production Agent (Tri-Task Pipeline)
│   ├── baselines.py              # Baseline 0 (Static) & Baseline 1 (Heuristic)
│   ├── taxonomy.py               # Grounded 7-intent taxonomy & escalation keywords
│   ├── historical_kb.py          # Grounded historical support knowledge base
│   └── evaluator.py              # Evaluation harness & LLM-as-a-judge rubric
├── report/
│   ├── EVALUATION_REPORT.md      # Full 6-page comprehensive engineering report
│   └── benchmark_results.json    # Exported quantitative benchmark metrics
├── run_eval.py                   # 1-click execution script (<15 min reproduction)
├── requirements.txt              # Project dependencies
└── README.md                     # Documentation & setup guide
```

---

## 📑 Detailed Report Highlights
Read the full [EVALUATION_REPORT.md](report/EVALUATION_REPORT.md) for:
1. **Problem Framing & Non-Goals** (what we chose *not* to build).
2. **Failure Analysis (Top 5 Failure Modes)** with real examples and root hypotheses.
3. **"What is misleading about my headline number?"** mandatory section.
4. **1-Week Roadmap** for multi-turn thread context & dense embedding RAG.
5. **Decision Log** detailing 12 non-obvious engineering decisions.

---

## 📬 Submission Checklist
- [x] Runnable GitHub repository with `<1 min` reproduction
- [x] Hand-labeled Golden Evaluation Set (500 samples) with sampling methodology
- [x] Multi-baseline comparison (Baseline 0, Baseline 1, Standard RAG, Agentic RAG)
- [x] Multi-dimensional LLM-as-a-judge rubric with human agreement analysis
- [x] 6-page comprehensive engineering report (`report/EVALUATION_REPORT.md`)
- [x] Ready to submit via [Hiver Submission Form](https://intelligent-bar-256.notion.site/39492cbf0da2800682cfc78a600a745f)
