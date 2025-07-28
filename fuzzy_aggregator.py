# fuzzy_aggregator.py

import pandas as pd
import numpy as np
import skfuzzy
import matplotlib.pyplot as plt

# Minimum consensus (%) to keep an item
MIN_CONSENSUS = 65

def translate_response(resp):
    """Map Likert response to a triangular fuzzy number."""
    mapping = {
        'Strongly agree':      (0.6, 0.8, 1.0),
        'Agree':               (0.4, 0.6, 0.8),
        'Neutral':             (0.2, 0.4, 0.6),
        'Disagree':            (0.0, 0.2, 0.4),
        'Strongly disagree':   (0.0, 0.0, 0.2),
    }
    return mapping.get(resp, (0.0, 0.05, 0.1))

def fuzzy_distance(a, b):
    """Euclidean distance between two triangular fuzzy numbers."""
    return (((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)/3)**0.5

def average_triangular(fuzzy_list):
    """Compute component‐wise average of a list of fuzzy triples."""
    return [sum(vals)/len(vals) for vals in zip(*fuzzy_list)]

def defuzzify_simple(triple):
    """Weighted average defuzzification."""
    a,b,c = triple
    return (a + 2*b + c) / 4

def defuzzify_centroid(triple):
    """Center‐of‐area defuzzification."""
    universe = np.linspace(0,1,1000)
    memb = np.array([membership(x,triple) for x in universe])
    return skfuzzy.defuzz(universe, memb, 'centroid')

def membership(x, triple):
    a,b,c = triple
    if x < a or x > c:
        return 0.0
    if x <= b:
        return (x - a)/(b - a) if b != a else 1.0
    return (c - x)/(c - b) if c != b else 1.0

def compute_item_score(df, column, method='simple'):
    """Compute defuzzified score, consensus %, and decision for one column."""
    vals = df[column].dropna().tolist()
    fuzzy_list = [translate_response(v) for v in vals]
    avg_fuz = average_triangular(fuzzy_list)
    score = (defuzzify_centroid(avg_fuz) if method=='centroid' 
             else defuzzify_simple(avg_fuz))
    distances = [fuzzy_distance(f, avg_fuz) for f in fuzzy_list]
    consensus = sum(d < 0.2 for d in distances) / len(distances) * 100
    decision = 'Retain' if consensus >= MIN_CONSENSUS else 'Remove'
    return score, consensus, decision

def run_aggregation(responses_csv: str):
    """Load survey CSV and compute fuzzy‐Delphi for each column (except ExpertID)."""
    df = pd.read_csv(responses_csv)
    questions = [c for c in df.columns if c != 'ExpertID']
    results = []
    for q in questions:
        s,c,d = compute_item_score(df, q)
        results.append({'Item': q, 'Score': s, 'Consensus': c, 'Decision': d})
    out = pd.DataFrame(results).sort_values('Score', ascending=False)
    return out

if __name__ == '__main__':
    summary = run_aggregation('survey_round2.csv')
    print(summary.to_string(index=False))
    summary.to_csv('aggregated_results.csv', index=False)

    # quick plots
    summary.plot.bar(x='Item', y='Score', figsize=(8,4), title='Defuzzified Scores')
    plt.tight_layout(); plt.show()
    ax = summary.plot.bar(x='Item', y='Consensus', figsize=(8,4), title='Consensus Rates')
    ax.axhline(MIN_CONSENSUS, color='r', linestyle='--')
    plt.tight_layout(); plt.show()
