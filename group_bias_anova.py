import pandas as pd
from sklearn.preprocessing import LabelEncoder
from statsmodels.multivariate.manova import MANOVA

def test_group_bias(expert_info_csv: str, responses_csv: str):
    """
    expert_info_csv must have columns [ExpertID, Role, Department]
    responses_csv must have [ExpertID, Question1, Question2, …]
    """
    info = pd.read_csv(expert_info_csv)
    resp = pd.read_csv(responses_csv)
    merged = pd.merge(info, resp, on='ExpertID')
    questions = [c for c in resp.columns if c != 'ExpertID']
    results = []
    for q in questions:
        le = LabelEncoder()
        merged['RespEnc']  = le.fit_transform(merged[q])
        merged['RoleEnc']  = le.fit_transform(merged['Role'])
        merged['DeptEnc']  = le.fit_transform(merged['Department'])
        df = merged[['RoleEnc','DeptEnc','RespEnc']]
        maov = MANOVA.from_formula('RespEnc ~ RoleEnc + DeptEnc', data=df)
        pval = maov.mv_test().results['RespEnc']['stat']['Pr > F'][0]
        results.append({'Question':q, 'p_value': pval})
    return pd.DataFrame(results)
    
if __name__ == '__main__':
    print(test_group_bias('expert_info.csv','survey_round2.csv'))
