import ast
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
ALGO_DIR = ROOT / "experiments" / "nvtai"
DATA_DIR = ROOT / "dataset" / "artificial data"
OUTPUT_DIR = ALGO_DIR

sys.path.append(str(ROOT))
sys.path.append(str(ALGO_DIR))

from brute_force import BruteForceKMismatches


def load_dataset():
    path_files = sorted(
        DATA_DIR.glob("dna_*.txt"),
        key=lambda p: int(p.stem.split("_")[1]),
    )

    records = []
    for path in path_files:
        with path.open("r") as f:
            for sample_id, line in enumerate(f):
                text, pattern, k, expected = line.strip().split(" ", maxsplit=3)
                records.append(
                    {
                        "file": path.name,
                        "sample_id": sample_id,
                        "text": text,
                        "pattern": pattern,
                        "k": int(k),
                        "expected": ast.literal_eval(expected),
                    }
                )
    return records


def valid(pred, expected):
    return sorted(pred) == sorted(expected)


def test_algorithm(algo, records):
    rows = []
    for row in records:
        eval_result = algo.evaluate(row["text"], row["pattern"], row["k"])
        pred = eval_result["matches"]
        rows.append(
            {
                "file": row["file"],
                "sample_id": row["sample_id"],
                "algorithm": algo.name,
                "input_size": len(row["text"]),
                "text_len": len(row["text"]),
                "pattern_len": len(row["pattern"]),
                "k": row["k"],
                "runtime_sec": eval_result["runtime_sec"],
                "num_expected": len(row["expected"]),
                "num_pred": eval_result["num_matches"],
                "valid": valid(pred, row["expected"]),
                "expected": row["expected"],
                "pred": pred,
            }
        )
    return rows


def build_results():
    records = load_dataset()
    algorithms = [
        BruteForceKMismatches(),
    ]

    all_rows = []
    for algo in algorithms:
        all_rows.extend(test_algorithm(algo, records))

    df_all = pd.DataFrame(all_rows)
    summary = (
        df_all.groupby(["algorithm", "input_size"])
        .agg(
            num_samples=("valid", "count"),
            num_correct=("valid", "sum"),
            avg_runtime_sec=("runtime_sec", "mean"),
            median_runtime_sec=("runtime_sec", "median"),
            min_runtime_sec=("runtime_sec", "min"),
            max_runtime_sec=("runtime_sec", "max"),
            total_runtime_sec=("runtime_sec", "sum"),
            avg_pattern_len=("pattern_len", "mean"),
            avg_k=("k", "mean"),
        )
        .reset_index()
    )
    summary["num_wrong"] = summary["num_samples"] - summary["num_correct"]
    summary["accuracy"] = summary["num_correct"] / summary["num_samples"]
    return df_all, summary


def save_plot(path):
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def plot_summary(summary):
    plt.figure(figsize=(10, 5))
    for algo_name, group in summary.groupby("algorithm"):
        plt.plot(group["input_size"], group["avg_runtime_sec"], marker="o", label=algo_name)
    plt.xlabel("Input size")
    plt.ylabel("Average runtime (seconds)")
    plt.title("Average Runtime by Input Size")
    save_plot(OUTPUT_DIR / "average_runtime_by_input_size.png")

    plt.figure(figsize=(10, 5))
    for algo_name, group in summary.groupby("algorithm"):
        plt.plot(group["input_size"], group["total_runtime_sec"], marker="o", label=algo_name)
    plt.xlabel("Input size")
    plt.ylabel("Total runtime (seconds)")
    plt.title("Total Runtime by Input Size")
    save_plot(OUTPUT_DIR / "total_runtime_by_input_size.png")

    plt.figure(figsize=(10, 5))
    for algo_name, group in summary.groupby("algorithm"):
        plt.plot(group["input_size"], group["accuracy"], marker="o", label=algo_name)
    plt.xlabel("Input size")
    plt.ylabel("Accuracy")
    plt.title("Accuracy by Input Size")
    plt.ylim(0, 1.05)
    save_plot(OUTPUT_DIR / "accuracy_by_input_size.png")

    plt.figure(figsize=(10, 5))
    for algo_name, group in summary.groupby("algorithm"):
        plt.plot(
            group["input_size"],
            group["avg_runtime_sec"],
            marker="o",
            label=f"{algo_name} average",
        )
        plt.fill_between(
            group["input_size"],
            group["min_runtime_sec"],
            group["max_runtime_sec"],
            alpha=0.15,
        )
    plt.xlabel("Input size")
    plt.ylabel("Runtime (seconds)")
    plt.title("Average Runtime with Min-Max Range")
    save_plot(OUTPUT_DIR / "average_runtime_min_max_range.png")


def main():
    df_all, summary = build_results()
    df_all.to_csv(OUTPUT_DIR / "experiment_results.csv", index=False)
    summary.to_csv(OUTPUT_DIR / "experiment_summary.csv", index=False)
    plot_summary(summary)

    print("Saved:")
    for path in [
        OUTPUT_DIR / "experiment_results.csv",
        OUTPUT_DIR / "experiment_summary.csv",
        OUTPUT_DIR / "average_runtime_by_input_size.png",
        OUTPUT_DIR / "total_runtime_by_input_size.png",
        OUTPUT_DIR / "accuracy_by_input_size.png",
        OUTPUT_DIR / "average_runtime_min_max_range.png",
    ]:
        print(path)


if __name__ == "__main__":
    main()
