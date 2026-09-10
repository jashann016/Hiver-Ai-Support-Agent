"""
Evaluation Harness:
- Intent Classification Metrics (Macro F1, Precision, Recall, Accuracy)
- Escalation Gating Metrics (Escalation Precision, Recall, F1, Under-escalation risk)
- Response Quality Evaluation & LLM-as-a-Judge simulation
- Human-Judge Alignment (Cohen's Kappa & Agreement %)
"""

import json
from typing import List, Dict, Any
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, cohen_kappa_score


class SupportAgentEvaluator:
    def __init__(self, golden_set_path: str):
        with open(golden_set_path, "r", encoding="utf-8") as f:
            self.golden_data = json.load(f)

    def evaluate_model(self, model_instance) -> Dict[str, Any]:
        """
        Runs evaluation across full golden evaluation dataset.
        """
        y_true_intent = []
        y_pred_intent = []

        y_true_esc = []
        y_pred_esc = []

        predictions = []

        for item in self.golden_data:
            text = item["tweet_text"]
            res = model_instance.process_message(text)

            y_true_intent.append(item["true_intent"])
            y_pred_intent.append(res["predicted_intent"])

            y_true_esc.append(item["true_escalation"])
            y_pred_esc.append(res["escalate_to_human"])

            predictions.append({
                "id": item["id"],
                "input": text,
                "gold_intent": item["true_intent"],
                "pred_intent": res["predicted_intent"],
                "gold_esc": item["true_escalation"],
                "pred_esc": res["escalate_to_human"],
                "gold_reply": item["ideal_reply"],
                "pred_reply": res["draft_reply"],
                "gold_quality_score": item.get("gold_quality_score", 5)
            })

        # Intent metrics
        acc_intent = accuracy_score(y_true_intent, y_pred_intent)
        prec_intent, rec_intent, f1_intent, _ = precision_recall_fscore_support(
            y_true_intent, y_pred_intent, average="macro", zero_division=0
        )

        # Escalation metrics
        acc_esc = accuracy_score(y_true_esc, y_pred_esc)
        prec_esc, rec_esc, f1_esc, _ = precision_recall_fscore_support(
            y_true_esc, y_pred_esc, average="binary", zero_division=0
        )

        # Under-escalation rate (Dangerous: Should have escalated to human but auto-replied)
        under_escalations = sum(1 for yt, yp in zip(y_true_esc, y_pred_esc) if yt is True and yp is False)
        under_escalation_rate = under_escalations / max(1, sum(1 for yt in y_true_esc if yt is True))

        # Over-escalation rate (Inefficient: Could have auto-resolved but sent to human queue)
        over_escalations = sum(1 for yt, yp in zip(y_true_esc, y_pred_esc) if yt is False and yp is True)
        over_escalation_rate = over_escalations / max(1, sum(1 for yt in y_true_esc if yt is False))

        # Response Quality Evaluation (LLM-as-a-Judge scoring rubric 1-5)
        judge_scores = []
        for p in predictions:
            # Multi-dimensional rubric: Intent alignment (40%), Groundedness (30%), Safety/Escalation correctness (30%)
            score = 1.0
            if p["gold_intent"] == p["pred_intent"]:
                score += 2.0
            if p["gold_esc"] == p["pred_esc"]:
                score += 1.5
            if "https://" in p["pred_reply"] or "DM" in p["pred_reply"]:
                score += 0.5
            judge_scores.append(min(5.0, round(score, 1)))

        avg_judge_score = sum(judge_scores) / len(judge_scores)

        # Human-Judge Agreement Analysis
        # Discretize scores into 1-5 categories
        human_scores = [p["gold_quality_score"] for p in predictions]
        discrete_judge = [int(round(s)) for s in judge_scores]
        kappa = cohen_kappa_score(human_scores, discrete_judge)
        exact_match_rate = sum(1 for h, j in zip(human_scores, discrete_judge) if h == j) / len(human_scores)

        return {
            "intent_accuracy": round(acc_intent, 4),
            "intent_macro_f1": round(f1_intent, 4),
            "intent_macro_precision": round(prec_intent, 4),
            "intent_macro_recall": round(rec_intent, 4),
            "escalation_accuracy": round(acc_esc, 4),
            "escalation_precision": round(prec_esc, 4),
            "escalation_recall": round(rec_esc, 4),
            "escalation_f1": round(f1_esc, 4),
            "under_escalation_safety_risk": round(under_escalation_rate, 4),
            "over_escalation_cost_rate": round(over_escalation_rate, 4),
            "avg_reply_judge_quality": round(avg_judge_score, 2),
            "judge_human_cohen_kappa": round(kappa, 3),
            "judge_human_agreement_pct": round(exact_match_rate * 100, 1),
            "sample_predictions": predictions[:5]
        }
