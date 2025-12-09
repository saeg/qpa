import json
import csv
import os
import glob
from datetime import datetime

# Configuration
INPUT_FOLDER = "data"
OUTPUT_FOLDER = "results"

def get_latest_json_file(folder):
    """Finds the most recently created JSON file in the data folder."""
    list_of_files = glob.glob(os.path.join(folder, "quantum_language_dist_*.json"))
    if not list_of_files:
        return None
    return max(list_of_files, key=os.path.getctime)

def generate_exports():
    # 1. Find and Load Data
    json_file = get_latest_json_file(INPUT_FOLDER)

    if not json_file:
        print(f"No JSON data files found in '{INPUT_FOLDER}/'. Run the search script first.")
        return

    print(f"Processing file: {json_file}")

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    distribution = data.get("distribution", {})
    total_repos = data.get("meta", {}).get("total_repos", 0)
    timestamp = data.get("meta", {}).get("timestamp", "unknown")

    # Prepare output folder
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    base_filename = f"quantum_stats_{timestamp}"
    csv_path = os.path.join(OUTPUT_FOLDER, f"{base_filename}.csv")
    md_path = os.path.join(OUTPUT_FOLDER, f"{base_filename}.md")

    # 2. Prepare Data Structure (Calculate Percentages)
    # Convert dict to list of tuples: (Rank, Language, Count, Percentage)
    stats_list = []
    rank = 1

    # Variables for "The Python Argument" aggregation
    python_ecosystem_count = 0

    for lang, count in distribution.items():
        percentage = (count / total_repos) * 100 if total_repos > 0 else 0
        stats_list.append({
            "rank": rank,
            "language": lang,
            "count": count,
            "percentage": percentage
        })

        # Aggregate Python + Jupyter for your specific research argument
        if lang in ["Python", "Jupyter Notebook"]:
            python_ecosystem_count += count

        rank += 1

    # 3. Write CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Rank", "Language", "Count", "Percentage"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in stats_list:
            writer.writerow({
                "Rank": row["rank"],
                "Language": row["language"],
                "Count": row["count"],
                "Percentage": f"{row['percentage']:.2f}%"
            })

    print(f"-> CSV saved to: {csv_path}")

    # 4. Write Markdown
    with open(md_path, "w", encoding="utf-8") as md:
        # Header
        md.write(f"# Quantum Computing Open Source Language Distribution\n\n")
        md.write(f"**Total Repositories Analyzed:** {total_repos}\n\n")
        md.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n")

        # The Argument Section (Python Dominance)
        python_share = (python_ecosystem_count / total_repos) * 100 if total_repos > 0 else 0
        md.write("## 🐍 Python Dominance Analysis\n")
        md.write("In the context of scientific computing, **Python** and **Jupyter Notebooks** represent the same ecosystem. ")
        md.write("Aggregating these reveals the true market share:\n\n")
        md.write(f"- **Python Ecosystem Share:** {python_share:.2f}%\n")
        md.write(f"- **Other Languages:** {100 - python_share:.2f}%\n\n")

        # The Full Table
        md.write("## Detailed Language Breakdown\n\n")
        md.write("| Rank | Language | Count | Percentage |\n")
        md.write("| :--- | :--- | :--- | :--- |\n")

        for row in stats_list:
            # Bolding top 3 for emphasis
            prefix = "**" if row["rank"] <= 3 else ""
            suffix = "**" if row["rank"] <= 3 else ""

            md.write(f"| {row['rank']} | {prefix}{row['language']}{suffix} | {row['count']} | {row['percentage']:.2f}% |\n")

    print(f"-> Markdown saved to: {md_path}")

    # Print Markdown to console for quick copy-paste
    print("\n" + "="*30 + " PREVIEW " + "="*30)
    with open(md_path, 'r') as f:
        print(f.read())
    print("="*69)

if __name__ == "__main__":
    generate_exports()