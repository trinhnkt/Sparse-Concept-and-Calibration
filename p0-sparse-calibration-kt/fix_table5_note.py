import sys

def fix_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        old_text = "The sum of evaluated KCs across strata (e.g., 260/265 for ASSISTments 2012, 834/866 for XES3G5M) excludes strict cold-start concepts that never appeared in the test folds."
        new_text = "The evaluated-KC totals (e.g., 260/265 for ASSISTments 2012, 834/866 for XES3G5M) may be smaller than the dataset-level KC counts in Table 2 because only KCs appearing in the evaluated prediction exports after test-fold filtering and KC-strata matching are counted."
        
        if old_text in content:
            content = content.replace(old_text, new_text)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed {filepath}")
        else:
            print(f"Old text not found in {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

fix_file('jedm_upload_folder/tables/table_iv_bucket_performance_updated.tex')
fix_file('springer_upload_folder/tables/table_iv_bucket_performance_updated.tex')
