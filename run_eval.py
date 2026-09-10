"""
1-Click Reproducible Benchmark Script for Hiver SDE Intern Submission.
Executes Baseline 0, Baseline 1, and Production Agent across Golden Evaluation Set.
Generates rich comparison tables and exports evaluation JSON.
"""

import os
import json
from src.agent import SpotifySupportAgent
from src.baselines import Baseline0TrivialAgent, Baseline1SimpleAgent
from src.evaluator import SupportAgentEvaluator

def main():
    print("=" * 80)
    print("🚀 HIVER SDE INTERN: AI CUSTOMER SUPPORT AGENT EVALUATION BENCHMARK")
    print("Brand: @SpotifyCares | Dataset: Customer Support on Twitter Golden Set (N=200)")
    print("=" * 80)

    golden_path = os.path.join(os.path.dirname(__file__), "data", "golden_eval_set.json")
    evaluator = SupportAgentEvaluator(golden_path)

    models = {
        "Baseline 0 (Trivial: Rule/Static)": Baseline0TrivialAgent(),
        "Baseline 1 (Simple: Heuristic Rule)": Baseline1SimpleAgent(),
        "Production Agent (RAG + Calibrated Routing)": SpotifySupportAgent()
    }

    results = {}

    for name, model in models.items():
        print(f"\nEvaluating: {name}...")
        metrics = evaluator.evaluate_model(model)
        results[name] = metrics

    print("\n" + "=" * 80)
    print("📊 HEADLINE EVALUATION RESULTS")
    print("=" * 80)

    header = f"{'Model':<45} | {'Intent F1':<10} | {'Escalation F1':<14} | {'Safety Risk (Under-Esc)':<22} | {'Judge Score (1-5)':<18}"
    print(header)
    print("-" * 115)

    for name, m in results.items():
        row = f"{name:<45} | {m['intent_macro_f1']:<10.3f} | {m['escalation_f1']:<14.3f} | {m['under_escalation_safety_risk']*100:<21.1f}% | {m['avg_reply_judge_quality']:<18.2f}"
        print(row)

    print("-" * 115)
    print(f"🎯 Judge-Human Cohen's Kappa Agreement: {results['Production Agent (RAG + Calibrated Routing)']['judge_human_cohen_kappa']}")
    print(f"🎯 Judge-Human Exact Agreement Rate: {results['Production Agent (RAG + Calibrated Routing)']['judge_human_agreement_pct']}%")

    # Save benchmark results
    out_path = os.path.join(os.path.dirname(__file__), "report", "benchmark_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n✅ Full benchmark metrics saved to: {out_path}")

if __name__ == "__main__":
    main()
