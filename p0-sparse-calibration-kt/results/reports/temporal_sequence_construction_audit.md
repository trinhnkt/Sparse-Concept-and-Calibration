# Temporal Sequence Construction Audit

## Findings

| Check | Result | Detail |
|-------|--------|--------|
| timestamp_sort_in_data_loader | PRESENT | The data loader/test loop sorts by timestamp before building sequences |
| cold_start_first_step_0.5 | PRESENT | First step prediction is 0.5 (cold start placeholder) |
| causal_order_predict_then_update | MISSING | pred_val appended to output list before state_feats updated |
| groupby_user_id_in_test_loop | PRESENT | Test loop groups by user_id for sequential prediction |
| test_df_sorted_before_groupby | PRESENT | test_df is sorted by timestamp before groupby — BUT note: temporal split ensures global order, individual users may have |
| prediction_convention | INFO | Convention in baseline_runner.py: features[:-1] → labels[1:] in KTDataset (DKT training). In sequential test loop: at st |
| KTDataset_user_sequence_sort | PRESENT | KTDataset does NOT explicitly sort user interactions by timestamp. It relies on groupby preserving order of the input da |

## Convention

- Convention in baseline_runner.py: features[:-1] → labels[1:] in KTDataset (DKT training). In sequential test loop: at step i, model uses state_feats (history 0..i-1) to predict label at step i. This is CORRECT for KT (predict current from past). Prediction at i=0 is always 0.5 (cold start).

## Conclusion

The causal prediction convention is correct (predict step i from history 0..i-1). The critical risk is that **within-user interaction sequences are not explicitly sorted by timestamp** inside KTDataset or the test loop. This is fragile: correct only if the input CSV was pre-sorted. The temporal split saves data in sorted order, so this is likely OK, but should be made explicit by adding explicit sort.