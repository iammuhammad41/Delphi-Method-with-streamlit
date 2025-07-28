# Fuzzy Delphi Expert Survey Dashboard

This repository provides a full pipeline for aggregating expert survey responses using a fuzzy Delphi approach, checking convergence of consensus, testing for group bias, and exploring results interactively via a Streamlit app.

## Repository Structure

- **fuzzy_aggregator.py**  
  Implements a triangular‐fuzzy aggregation of Likert‐scale responses, defuzzification (simple or centroid), computes consensus rates and “Retain/Remove” decisions per item, and produces summary CSV and plots.

- **convergence_check.py**  
  Loads two rounds of aggregated consensus results and runs Mann–Whitney U, median, and Kruskal–Wallis tests to assess stability of consensus between rounds.

- **group_bias_anova.py**  
  Performs a MANOVA to test whether expert role or department has significant effect on survey responses (detects potential group bias).

- **streamlit_app.py**  
  A self‐contained Streamlit dashboard that allows you to upload your survey and expert‐info CSVs, view aggregation results and plots, run convergence and bias tests—all via a web UI.

## Installation

```bash
git clone https://github.com/yourusername/fuzzy-delphi-dashboard.git
cd fuzzy-delphi-dashboard
pip install pandas numpy scikit-fuzzy scipy statsmodels streamlit matplotlib
````

## Usage

1. **Prepare your CSV files**

   * `survey_round2.csv`: Expert responses for Round 2 (columns: `ExpertID`, then one column per question with values *Strongly agree*, *Agree*, etc.)
   * *Optional* `survey_round1_results.csv`: Prior consensus results from Round 1 (must include columns `Item`, `Consensus`)
   * *Optional* `expert_info.csv`: Expert metadata (columns: `ExpertID`, `Role`, `Department`)

2. **Run from command line**

   ```bash
   python fuzzy_aggregator.py         # Aggregates and plots fuzzy-Delphi results
   python convergence_check.py       # Tests convergence between two rounds
   python group_bias_anova.py        # Tests for role/department bias via MANOVA
   ```

3. **Start the Streamlit dashboard**

   ```bash
   streamlit run streamlit_app.py
   ```

   Then open the URL shown in your browser to interactively upload files and view results.

## File Formats

* **Survey CSV** must have at least:

  * `ExpertID` (unique identifier per respondent)
  * One column per question, with responses in:

    * `Strongly agree`
    * `Agree`
    * `Neutral`
    * `Disagree`
    * `Strongly disagree`

* **Expert Info CSV** (for bias testing):

  * `ExpertID`, `Role`, `Department`

* **Round 1 Results CSV** (for convergence testing):

  * `Item`, `Consensus`

## Acknowledgments

This implementation was inspired by and adapted from the **Traditional Fuzzy Delphi Method** by Ihor Markevych.
Original script:
[https://github.com/IhorMarkevych/Traditional-Delphi-Method/blob/master/traditional\_delphi.py](https://github.com/IhorMarkevych/Traditional-Delphi-Method/blob/master/traditional_delphi.py), (https://github.com/IhorMarkevych/Consistency-Aggregation-Method) and (https://github.com/IhorMarkevych/DelphiMethod)

