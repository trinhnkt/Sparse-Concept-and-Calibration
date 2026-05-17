import pandas as pd
from pyBKT.models import Model as BKTModel

def main():
    print("Loading datasets...")
    train_df = pd.read_csv("data/processed/assist2012/splits/learner_based/fold_0/train.csv")
    test_df = pd.read_csv("data/processed/assist2012/splits/learner_based/fold_0/test.csv")
    
    print("Train unique correct:", train_df['correct'].unique())
    print("Test unique correct:", test_df['correct'].unique())
    
    # Map correct to 0 and 1 explicitly in case it is float or boolean
    train_df['correct'] = train_df['correct'].astype(int)
    test_df['correct'] = test_df['correct'].astype(int)
    
    # Take a sample of train_df to fit quickly
    train_sample = train_df.sample(n=10000, random_state=42)
    test_sample = test_df.sample(n=2000, random_state=42)
    
    bkt = BKTModel(seed=42)
    
    # Create clean skill name mapping to avoid regex issue in pyBKT
    all_kcs = sorted(pd.concat([train_df['kc_id'], test_df['kc_id']]).unique())
    kc_map = {kc: i for i, kc in enumerate(all_kcs)}
    
    bkt_train = train_sample[['user_id', 'kc_id', 'correct']].copy()
    bkt_train['skill_name'] = bkt_train['kc_id'].map(lambda x: f"skill_{kc_map[x]}")
    bkt_train = bkt_train[['user_id', 'skill_name', 'correct']]
    
    print("Fitting model on 10k sample...")
    bkt.fit(data=bkt_train)
    
    print("Predicting on 2k sample...")
    bkt_test = test_sample[['user_id', 'kc_id', 'correct']].copy()
    bkt_test['skill_name'] = bkt_test['kc_id'].map(lambda x: f"skill_{kc_map[x]}")
    bkt_test = bkt_test[['user_id', 'skill_name', 'correct']]
    
    preds = bkt.predict(data=bkt_test)
    print("Predictions columns:", preds.columns)
    print("Predictions stats:")
    print(preds['correct_predictions'].describe())
    print("Unique predictions:", preds['correct_predictions'].unique()[:20])

if __name__ == '__main__':
    main()
