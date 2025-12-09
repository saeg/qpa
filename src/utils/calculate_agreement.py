import pandas as pd
from statsmodels.stats.inter_rater import fleiss_kappa, aggregate_raters
from sklearn.metrics import cohen_kappa_score
from src.conf import config


PATTERN_CLASSES_DATASET = config.RESULTS_DIR / "classes_dataset.csv"

def calculate_kappas(filename):
    try:
        df = pd.read_csv(filename)
        print(f"Successfully loaded '{filename}' with {len(df)} rows.")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found in this folder.")
        return

    raters_df = df[['pattern', 'higor_pattern', 'erico_pattern']].copy()

    #  Data Cleaning
    # Fleiss' Kappa requires that every subject be rated by the same number of raters.
    # We must drop rows where any author left a blank (NaN) answer.
    initial_count = len(raters_df)
    raters_df.dropna(inplace=True)
    final_count = len(raters_df)

    if final_count < initial_count:
        print(f"Removed {initial_count - final_count} rows containing missing values (empty cells).")
        print(f"Proceeding with {final_count} fully classified rows.\n")

    # all data are strings and strip whitespace to avoid mismatches like "Oracle" vs "Oracle "
    for col in raters_df.columns:
        raters_df[col] = raters_df[col].astype(str).str.strip()

    # ==========================================
    # PART A: FLEISS' KAPPA (Overall Agreement)
    # ==========================================
    print("--- 3-AUTHOR AGREEMENT (FLEISS' KAPPA) ---")

    # statsmodels requires a matrix of counts (Subject x Categories).
    # aggregate_raters converts the raw [Subject x Rater] dataframe into that format.
    agg_data, categories = aggregate_raters(raters_df.to_numpy())

    f_kappa = fleiss_kappa(agg_data)
    print(f"Fleiss' Kappa: {f_kappa:.4f}")
    interpret_score(f_kappa)
    print("")

    # ==========================================
    # PART B: COHEN'S KAPPA (Pairwise Agreement)
    # ==========================================
    print("--- PAIRWISE AGREEMENT (COHEN'S KAPPA) ---")

    # Pair 1: Original vs Higor
    k1 = cohen_kappa_score(raters_df['pattern'], raters_df['higor_pattern'])
    print(f"1. Original vs Higor: {k1:.4f}")

    # Pair 2: Original vs Erico
    k2 = cohen_kappa_score(raters_df['pattern'], raters_df['erico_pattern'])
    print(f"2. Original vs Erico: {k2:.4f}")

    # Pair 3: Higor vs Erico
    k3 = cohen_kappa_score(raters_df['higor_pattern'], raters_df['erico_pattern'])
    print(f"3. Higor    vs Erico: {k3:.4f}")

    # Calculate Light's Kappa (Average of Cohen's)
    lights_kappa = (k1 + k2 + k3) / 3
    print(f"\nLight's Kappa (Average): {lights_kappa:.4f}")
    interpret_score(lights_kappa)

def interpret_score(score):
    """Helper function to print interpretation based on Landis & Koch (1977)"""
    if score < 0:
        msg = "Poor agreement"
    elif score <= 0.20:
        msg = "Slight agreement"
    elif score <= 0.40:
        msg = "Fair agreement"
    elif score <= 0.60:
        msg = "Moderate agreement"
    elif score <= 0.80:
        msg = "Substantial agreement"
    else:
        msg = "Almost perfect agreement"
    print(f"Interpretation: {msg}")

if __name__ == "__main__":
    calculate_kappas(PATTERN_CLASSES_DATASET)