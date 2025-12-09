import json
import os
import sys
from collections import Counter
from datetime import datetime
from dotenv import load_dotenv
from github import Github, GithubException

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_PAT")

# Configuration
# We want a broader search to get statistical significance
MAX_RESULTS_PER_QUERY = 500
MIN_STARS = 10  # Low filter to exclude empty/test "hello world" repos
OUTPUT_FOLDER = "data"

search_queries = [
    "topic:quantum-computing",
    "topic:quantum-machine-learning",
    "topic:quantum-algorithms",
    # You can also search by text matches in description/readme if topics aren't enough:
    # "quantum computing",
]

def search_and_analyze_languages():
    if not GITHUB_TOKEN:
        print("Error: GitHub PAT/TOKEN not found in .env", file=sys.stderr)
        return

    g = Github(GITHUB_TOKEN)

    # Use a dictionary keyed by ID to ensure we don't count the same repo twice
    # if it appears in multiple search queries.
    unique_repos = {}

    print(f"--- Starting Search (Targeting ~{MAX_RESULTS_PER_QUERY} per query) ---")

    for query in search_queries:
        print(f"Querying: '{query}'...")
        try:
            # We explicitly do NOT filter by language in the query
            repositories = g.search_repositories(query=query, sort="stars", order="desc")

            count = 0
            for repo in repositories:
                if count >= MAX_RESULTS_PER_QUERY:
                    break

                # Basic filtering
                if repo.fork:
                    continue # Skip forks to avoid double counting the same codebase
                if repo.stargazers_count < MIN_STARS:
                    continue # Stop if we hit low quality repos (since we sort by stars)

                unique_repos[repo.id] = repo
                count += 1

            print(f"  -> Fetched top {count} results for '{query}'")

        except GithubException as e:
            print(f"  Error querying '{query}': {e.status} {e.data}", file=sys.stderr)
            if e.status == 403:
                print("  Rate limit exceeded. Try again later.")
                break

    print("-" * 50)
    print(f"Total unique repositories analyze: {len(unique_repos)}")
    print("-" * 50)

    # --- Analyze Languages ---
    languages = []

    for repo in unique_repos.values():
        # repo.language returns the primary language of the repo
        # Some repos might be None (rare, usually markdown only)
        lang = repo.language if repo.language else "Unknown/Docs"
        languages.append(lang)

    # Count distribution
    lang_counts = Counter(languages)
    total = len(languages)

    # --- Display Statistics ---
    print(f"{'Language':<20} | {'Count':<6} | {'Percentage':<10}")
    print("-" * 42)

    sorted_stats = lang_counts.most_common()

    for lang, count in sorted_stats:
        percentage = (count / total) * 100
        print(f"{lang:<20} | {count:<6} | {percentage:.2f}%")

    # --- Save Data for your Report ---
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_FOLDER, f"quantum_language_dist_{timestamp}.json")

    output_data = {
        "meta": {
            "total_repos": total,
            "queries": search_queries,
            "timestamp": timestamp
        },
        "distribution": {lang: count for lang, count in sorted_stats}
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"\nData saved to {output_file}")

if __name__ == "__main__":
    search_and_analyze_languages()