import pandas as pd
import scipy.stats as st

def compare_consensus(round1_csv: str, round2_csv: str):
    """Load two CSVs of aggregated_results and run convergence tests."""
    r1 = pd.read_csv(round1_csv)[['Item','Consensus']]
    r2 = pd.read_csv(round2_csv)[['Item','Consensus']]
    merged = pd.merge(r1, r2, on='Item', suffixes=('_1','_2'))
    print("\n=== Consensus Convergence Tests ===")
    mw = st.mannwhitneyu(merged.Consensus_1, merged.Consensus_2)
    print(f"Mann–Whitney U: stat={mw.statistic}, p={mw.pvalue:.4f}")
    md = st.median_test(merged.Consensus_1, merged.Consensus_2)
    print(f"Median test:   stat={md[0]:.4f}, p={md[1]:.4f}")
    kw = st.kruskal(merged.Consensus_1, merged.Consensus_2)
    print(f"Kruskal–Wallis: stat={kw.statistic:.4f}, p={kw.pvalue:.4f}")
