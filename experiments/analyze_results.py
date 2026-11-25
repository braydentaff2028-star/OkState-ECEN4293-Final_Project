#Analyze Simulation Results

import csv
import os
import statistics
import matplotlib.pyplot as plt
from collections import defaultdict


RESULTS_FILE = "experiments/results/simulation_results.csv"
OUTPUT_FOLDER = "experiments/results"

METRICS = [
    "score",
    "lines_cleared",
    "maximum_height",
    "holes"
]


def load_results():
    results = defaultdict(lambda: defaultdict(list))

    with open(RESULTS_FILE, "r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            configuration = row["configuration"]

            for metric in METRICS:
                results[configuration][metric].append(
                    float(row[metric])
                )

    return results


def calculate_statistics(results):
    summary = []

    for configuration, metrics in results.items():
        row = {"configuration": configuration}

        for metric in METRICS:
            values = metrics[metric]

            row[f"average_{metric}"] = statistics.mean(values)
            row[f"std_dev_{metric}"] = (
                statistics.stdev(values) if len(values) > 1 else 0
            )

        summary.append(row)

    return summary


def save_summary(summary):
    output_file = os.path.join(
        OUTPUT_FOLDER,
        "summary_statistics.csv"
    )

    fieldnames = list(summary[0].keys())

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary)

    print(f"Summary saved to: {output_file}")


def create_graphs(summary):
    for metric in METRICS:
        configurations = [
            row["configuration"] for row in summary
        ]

        averages = [
            row[f"average_{metric}"] for row in summary
        ]

        standard_deviations = [
            row[f"std_dev_{metric}"] for row in summary
        ]

        plt.figure(figsize=(12, 6))

        plt.bar(
            configurations,
            averages,
            yerr=standard_deviations,
            capsize=5
        )

        plt.title(f"Average {metric.replace('_', ' ').title()}")
        plt.xlabel("AI Configuration")
        plt.ylabel(f"Average {metric.replace('_', ' ').title()}")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()

        output_file = os.path.join(
            OUTPUT_FOLDER,
            f"{metric}_comparison.png"
        )

        plt.savefig(output_file)
        plt.close()

        print(f"Graph saved to: {output_file}")


def display_summary(summary):
    print("\nSIMULATION RESULTS")
    print("=" * 100)

    for row in summary:
        print(f"\n{row['configuration']}")

        for metric in METRICS:
            average = row[f"average_{metric}"]
            std_dev = row[f"std_dev_{metric}"]

            print(
                f"  {metric}: "
                f"Average = {average:.2f}, "
                f"Standard Deviation = {std_dev:.2f}"
            )


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    results = load_results()
    summary = calculate_statistics(results)

    display_summary(summary)
    save_summary(summary)
    create_graphs(summary)

    print("\nAnalysis completed successfully!")


if __name__ == "__main__":
    main()
