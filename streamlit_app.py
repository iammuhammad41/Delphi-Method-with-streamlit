# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fuzzy_aggregator import run_aggregation, MIN_CONSENSUS
from convergence_check import compare_consensus
from group_bias_anova import test_group_bias

st.set_page_config(page_title="Fuzzy Delphi Dashboard", layout="wide")
st.title("🔮 Fuzzy Delphi Expert Survey Explorer")

st.sidebar.header("Upload your files")
resp_file = st.sidebar.file_uploader("1. Round‑2 Responses (CSV)", type="csv")
prev_file = st.sidebar.file_uploader("2. Round‑1 Results (CSV)", type="csv")
info_file = st.sidebar.file_uploader("3. Expert Info (CSV)", type="csv")

if resp_file:
    # Save and read
    df_resp = pd.read_csv(resp_file)
    st.subheader("✅ Survey Round 2 Data")
    st.dataframe(df_resp.head())

    # Run fuzzy aggregation
    agg = run_aggregation(resp_file.name)
    st.subheader("📊 Aggregation Results")
    st.dataframe(agg)

    # Plot scores
    fig1, ax1 = plt.subplots()
    agg.plot.bar(x='Item', y='Score', ax=ax1, legend=False, figsize=(8,3))
    st.pyplot(fig1)

    # Plot consensus
    fig2, ax2 = plt.subplots()
    agg.plot.bar(x='Item', y='Consensus', ax=ax2, legend=False, figsize=(8,3))
    ax2.axhline(MIN_CONSENSUS, color='red', linestyle='--')
    st.pyplot(fig2)

    # Convergence tests
    if prev_file:
        st.subheader("🔄 Consensus Convergence")
        compare_consensus(prev_file.name, resp_file.name)

    # ANOVA bias tests
    if info_file:
        st.subheader("👥 Role/Dept Bias (MANOVA)")
        bias_df = test_group_bias(info_file.name, resp_file.name)
        st.dataframe(bias_df)

st.sidebar.markdown(
    """
    **Usage**  
    1. Upload your CSVs in order.  
    2. View aggregated scores & consensus rates.  
    3. Optionally check stability & bias tests.
    """
)
