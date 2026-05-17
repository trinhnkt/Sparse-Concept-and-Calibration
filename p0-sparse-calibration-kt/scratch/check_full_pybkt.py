import pandas as pd
from pyBKT.models import Model as BKTModel
from pathlib import Path

def main():
    print("Loading datasets...")
    train_df = pd.read_csv("data/processed/assist2012/splits/learner_based/fold_0/train.csv")
    test_df = pd.read_csv("data/processed/assist2012/splits/learner_based/fold_0/test.csv")
    
    # Map correct to 0 and 1 explicitly
    train_df['correct'] = train_df['correct'].astype(int)
    test_df['correct'] = test_df['correct'].astype(int)
    
    bkt = BKTModel(seed=42)
    
    all_kcs = sorted(pd.concat([train_df['kc_id'], test_df['kc_id']]).unique())
    kc_map = {kc: i for i, kc in enumerate(all_kcs)}
    
    bkt_train = train_df[['user_id', 'kc_id', 'correct']].copy()
    bkt_train['skill_name'] = bkt_train['kc_id'].map(lambda x: f"skill_{kc_map[x]}")
    bkt_train = bkt_train[['user_id', 'skill_name', 'correct']]
    
    print("Fitting full BKT...")
    bkt.fit(data=bkt_train)
    
    print("Predicting on full test...")
    bkt_test = test_df[['user_id', 'kc_id', 'correct']].copy()
    bkt_test['skill_name'] = bkt_test['kc_id'].map(lambda x: f"skill_{kc_map[x]}")
    bkt_test = bkt_test[['user_id', 'skill_name', 'correct']]
    
    preds = bkt.predict(data=bkt_test)
    print("Predictions description:")
    print(preds['correct_predictions'].describe())
    print("Value counts:")
    print(preds['correct_predictions'].value_counts(dropna=False).head(20))

if __name__ == '__main__':
    main()
