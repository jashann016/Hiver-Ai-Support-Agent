# 🎧 Hiver AI Support Agent & Evaluation System (`@SpotifyCares`)

> **Hiver SDE Intern Take-Home Project**  
> An evaluation-first AI Customer Support system for Twitter interactions that classifies intents, synthesizes historically-grounded replies, and reliably decides human escalations with auditable reasoning.

---

## ⚡ Quickstart (< 2 Minutes Reproduction)

### 1. Clone & Setup Environment
```bash
cd /Users/jashanpreetsingh/.gemini/antigravity/scratch/hiver-ai-support-agent
pip install -r requirements.txt
```

### 2. Run the Benchmark Evaluation Suite
```bash
python run_eval.py
```

This single command evaluates **Baseline 0**, **Baseline 1**, and the **Production Agent** across the 200-sample hand-curated Golden Evaluation Dataset, printing comparative metrics and exporting `report/benchmark_results.json`.

---

## 📊 Headline Benchmark Results

| Model Architecture | Intent F1 | Escalation F1 | Under-Escalation Safety Risk (Lower is better) | LLM Judge Quality (1-5) |
|---|:---:|:---:|:---:|:---:|
| **Baseline 0 (Trivial: Rule/Static)** | `0.212` | `0.296` | `82.6%` | `3.25` |
| **Baseline 1 (Simple: Heuristic)** | `0.373` | `0.488` | `54.4%` | `3.22` |
| **Production Agent (RAG + Calibrated Routing)** | **`0.782`** | **`0.731`** | **`26.1%`** | **`4.32`** |

---

## 📁 Repository Structure

```
hiver-ai-support-agent/
├── data/
│   ├── golden_eval_set.json      # 200 hand-curated & stratified golden test samples
│   ├── raw/                      # Raw conversational dataset samples
│   └── processed/                # Cleaned thread pairs
├── src/
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
- [x] Runnable GitHub repository with `<15 min` reproduction
- [x] Hand-labeled Golden Evaluation Set (200 samples) with sampling methodology
- [x] Multi-baseline comparison (Baseline 0, Baseline 1, Production)
- [x] Multi-dimensional LLM-as-a-judge rubric with human agreement analysis
- [x] 6-page comprehensive engineering report (`report/EVALUATION_REPORT.md`)
- [x] Ready to submit via [Hiver Submission Form](https://intelligent-bar-256.notion.site/39492cbf0da2800682cfc78a600a745f)
