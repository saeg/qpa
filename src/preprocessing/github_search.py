import os
import sys
from datetime import datetime, timezone
from github import Github, GithubException
from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta
from src.conf import config
import json

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_PAT")

TARGET_RESULT_COUNT = 60
SORT_BY = "stars"
SORT_ORDER = "desc"


search_queries = [
    'topic:quantum-computing language:Python',
    'topic:quantum-machine-learning language:Python',
    'topic:quantum-algorithms language:Python',
]

# Important frameworks are never missed by topic searches.
known_repos = [
    # Qiskit repos
    "Qiskit/qiskit",
    "qiskit-community/qiskit-algorithms",
    "qiskit-community/qiskit-machine-learning",
    "qiskit-community/qiskit-nature",
    "qiskit-community/qiskit-finance",
    "qiskit-community/qiskit-optimization",
    "qiskit-community/qiskit-dynamics",
    "qiskit-community/qiskit-experiments",
    # Cirq
    "quantumlib/Cirq",
    "quantumlib/ReCirq",
    "quantumlib/Qualtran",
    "quantumlib/OpenFermion",
    # PennyLane
    "PennyLaneAI/pennylane",
    # Rigetti Ecosystem
    "rigetti/pyquil",
    # Other Major Frameworks & Libraries
    "qutip/qutip",
    "qiboteam/qibo",
    "ProjectQ-Framework/ProjectQ",
    "XanaduAI/strawberryfields",
    "eclipse-qrisp/Qrisp",
    "jcmgray/quimb",
    "tencent-quantum-lab/tensorcircuit",
    "Classiq/classiq-library",
    "tensorflow/quantum",
    "mit-han-lab/torchquantum",
    # Amazon Braket Libraries
    "amazon-braket/amazon-braket-sdk-python",
    "amazon-braket/amazon-braket-examples",
    "amazon-braket/amazon-braket-algorithm-library",
]

MIN_STARS = 50
MIN_CONTRIBUTORS = 10
MAX_INACTIVITY_MONTHS = 12

EXCLUSION_KEYWORDS = [
    "provider", "qpu", "hardware", "device", "backend", "client", "cloud",
    "pulse", "control", "calibration", "benchmarking", "chip", "metal",
    "workshop", "game", "qiskit-advocate", "tutorial", "awesome-list",
    "plugin", "connector", "interface", "adapter", "books", "paper",
    "cryptography", "qkd", "post-quantum"
]

OUTPUT_FOLDER = config.PROJECT_ROOT / "data"

def check_for_exclusion(repo):
    """Checks if a repository should be excluded based on keywords."""
    repo_name = repo.full_name.lower()
    description = repo.description.lower() if repo.description else ""
    topics = [topic.lower() for topic in repo.topics]
    text_to_check = f"{repo_name} {description}"

    for keyword in EXCLUSION_KEYWORDS:
        if keyword in text_to_check:
            return True, f"Keyword '{keyword}' in name/description"
        if keyword in topics:
            return True, f"Topic '{keyword}'"
    return False, None


def is_repo_relevant(repo):
    """Applies all filters to a single repository. Returns (is_relevant, contributor_count)."""
    if repo.archived:
        print(f"[SKIPPING] {repo.full_name}: Archived repository.")
        return False, None
    if repo.fork:
        return False, None # Skip forks silently
    if repo.stargazers_count < MIN_STARS:
        print(f"[SKIPPING] {repo.full_name}: Not enough stars ({repo.stargazers_count} < {MIN_STARS}).")
        return False, None

    now = datetime.now(timezone.utc)
    inactivity_threshold = now - relativedelta(months=MAX_INACTIVITY_MONTHS)
    if repo.pushed_at < inactivity_threshold:
        print(f"[SKIPPING] {repo.full_name}: Inactive since {repo.pushed_at.date()}.")
        return False, None

    is_excluded, reason = check_for_exclusion(repo)
    if is_excluded:
        print(f"[SKIPPING] {repo.full_name}: Excluded by {reason}.")
        return False, None

    try:
        contributors_count = repo.get_contributors().totalCount
        if contributors_count < MIN_CONTRIBUTORS:
            print(f"[SKIPPING] {repo.full_name}: Not enough contributors ({contributors_count} < {MIN_CONTRIBUTORS}).")
            return False, None
    except GithubException as e:
        if e.status == 403:
            print(f"Warning: Could not fetch contributors for {repo.full_name} due to API limitations ({e.status}). Skipping.", file=sys.stderr)
            return False, None
        contributors_count = "N/A" # For other errors, we can proceed but mark as N/A

    return True, contributors_count


def search_github_for_qc_frameworks():
    """Searches GitHub using multiple queries and a known list, then filters."""
    if not GITHUB_TOKEN:
        print("Error: GitHub PAT/TOKEN not found.", file=sys.stderr); return

    try:
        g = Github(GITHUB_TOKEN)
        repo_candidates = {} # Use a dict for automatic de-duplication

        # Add known repositories first to ensure they are included
        print("--- Phase 1: Fetching known repositories ---")
        for repo_name in known_repos:
            try:
                repo = g.get_repo(repo_name)
                repo_candidates[repo.full_name] = repo
                print(f"  [OK] Fetched {repo.full_name}")
            except GithubException as e:
                print(f"Warning: Could not fetch known repo '{repo_name}': {e.status}", file=sys.stderr)

        # Discover new repositories using search queries
        print("\n--- Phase 2: Discovering new repositories via search ---")
        for query in search_queries:
            print(f"Searching with query: '{query}'...")
            try:
                # Limit search results per query to avoid excessive API usage
                repositories = g.search_repositories(query=query, sort=SORT_BY, order=SORT_ORDER)
                for repo in repositories[:200]: # Check top 200 from each query
                    if repo.full_name not in repo_candidates:
                        repo_candidates[repo.full_name] = repo
            except GithubException as e:
                print(f"Warning: Search query '{query}' failed: {e.status}", file=sys.stderr)

        print(f"\nGathered a total of {len(repo_candidates)} unique candidate repositories.")

        # filter an rank
        print("\n--- Phase 3: Applying quality filters ---")
        print(f" - Min Stars: {MIN_STARS}, Min Contributors: {MIN_CONTRIBUTORS}, Last push <= {MAX_INACTIVITY_MONTHS} months")
        print(f" - Excluding keywords: {', '.join(EXCLUSION_KEYWORDS[:4])}...")
        print("-" * 70)

        final_repos = []
        for repo in repo_candidates.values():
            is_relevant, contrib_count = is_repo_relevant(repo)
            if is_relevant:
                repo.contributors_count = contrib_count
                final_repos.append(repo)

        # Sort the final list by stars
        final_repos.sort(key=lambda r: r.stargazers_count, reverse=True)
        top_repos = final_repos[:TARGET_RESULT_COUNT]

        print("-" * 70)
        print(f"Found {len(top_repos)} matching repositories after filtering {len(repo_candidates)} candidates.\n")

        structured_results = []
        for i, repo in enumerate(top_repos):
            structured_results.append({
                "rank": i + 1,
                "full_name": repo.full_name,
                "stargazers_count": repo.stargazers_count,
                "contributors_count": repo.contributors_count,
                "forks_count": repo.forks_count,
                "pushed_at": repo.pushed_at.isoformat(),
                "description": repo.description,
                "html_url": repo.html_url
            })
            print(f"{i+1}. {repo.full_name}")
            print(f"   Stars: {repo.stargazers_count:<6} | Contributors: {str(repo.contributors_count):<6} | Forks: {repo.forks_count:<6} | Last Push: {repo.pushed_at.date()}")
            desc = (repo.description[:120] + '...') if repo.description and len(repo.description) > 120 else repo.description
            print(f"   Description: {desc}")
            print(f"   URL: {repo.html_url}\n")

        # Save structured results for easy processing
        OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        structured_output_file = OUTPUT_FOLDER / f"quantum_frameworks_structured_{timestamp}.json"
        with open(structured_output_file, 'w', encoding='utf-8') as f:
            json.dump(structured_results, f, indent=2, ensure_ascii=False)
        print(f"Structured results saved to: {structured_output_file}")
        print("-" * 70)

        # Save a simple list for the justfile
        repo_list_file = OUTPUT_FOLDER / "filtered_repo_list.txt"
        with open(repo_list_file, 'w', encoding='utf-8') as f:
            for repo in top_repos:
                f.write(f"{repo.full_name}\n")
        print(f"Simple repository list for automation saved to: {repo_list_file}")

        print("-" * 70)
        print("Search complete.")

    except GithubException as e:
        print(f"An error occurred with the GitHub API: {e.status} {e.data}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    search_github_for_qc_frameworks()