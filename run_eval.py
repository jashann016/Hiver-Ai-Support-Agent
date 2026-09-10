"""
Benchmark Evaluation Suite:
Executes 4 Distinct Model Architectures across 500 Golden Samples (2,000 Total Individual Pipeline Runs):
1. Baseline 0 (Trivial: Rule/Static)
2. Baseline 1 (Simple: Heuristic Rule)
3. Baseline 2 (Production Standard Agent: Fixed Routing)
4. Model 3 (Proposed Agentic RAG: Dynamic Multi-Hop Retrieval + Self-Critique Guardrails)
"""

import os
import json
from src.agent import SpotifySupportAgent
from src.agentic_rag import AgenticRAGSupportAgent
from src.baselines import Baseline0TrivialAgent, Baseline1SimpleAgent
from src.evaluator import SupportAgentEvaluator

def main():
    print("=" * 90)
    print("🚀 HIVER SDE INTERN: LARGE-SCALE AI CUSTOMER SUPPORT AGENT BENCHMARK")
    print("Brand: @SpotifyCares | Evaluation Suite: 500 Golden Samples x 4 Models = 2,000 Total Tests")
    print("=" * 90)

    golden_path = os.path.join(os.path.dirname(__file__), "data", "golden_eval_set.json")
    evaluator = SupportAgentEvaluator(golden_path)

    models = {
        "Baseline 0 (Trivial: Rule/Static)": Baseline0TrivialAgent(),
        "Baseline 1 (Simple: Heuristic Rule)": Baseline1SimpleAgent(),
        "Baseline 2 (Standard RAG Agent)": SpotifySupportAgent(),
        "Model 3 (Proposed: Agentic RAG + Self-Critique)": AgenticRAGSupportAgent()
    }

    results = {}
    total_evals = 0

    for name, model in models.items():
        print(f"🔄 Executing 500 evaluations on: {name}...")
        metrics = evaluator.evaluate_model(model)
        results[name] = metrics
        total_evals += len(evaluator.golden_data)

    print("\n" + "=" * 90)
    print(f"📊 HEADLINE BENCHMARK COMPARISON ({total_evals} TOTAL COMPLETED EVALUATIONS)")
    print("=" * 90)

    header = f"{'Model Architecture':<47} | {'Intent F1':<10} | {'Escalation F1':<14} | {'Safety Risk (Under-Esc)':<22} | {'Judge Score (1-5)':<18}"
    print(header)
    print("-" * 122)

    for name, m in results.items():
        row = f"{name:<47} | {m['intent_macro_f1']:<10.3f} | {m['escalation_f1']:<14.3f} | {m['under_escalation_safety_risk']*100:<21.1f}% | {m['avg_reply_judge_quality']:<18.2f}"
        print(row)

    print("-" * 122)
    top_model = "Model 3 (Proposed: Agentic RAG + Self-Critique)"
    print(f"🎯 Agentic RAG Human-Judge Agreement (Cohen's Kappa): {results[top_model]['judge_human_cohen_kappa']}")
    print(f"🎯 Agentic RAG Human-Judge Exact Agreement Rate: {results[top_model]['judge_human_agreement_pct']}%")

    # Save benchmark results
    out_path = os.path.join(os.path.dirname(__file__), "report", "benchmark_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ All 2,000 test results successfully exported to: {out_path}")

if __name__ == "__main__":
    main()
