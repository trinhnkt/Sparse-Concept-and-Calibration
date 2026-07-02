import re
import csv
from pathlib import Path

def get_reliability_flag(n_events_str):
    n_str = n_events_str.replace(',', '').strip()
    try:
        n = int(n_str)
        if n >= 1000:
            return 'R'
        elif n >= 100:
            return 'L'
        else:
            return 'I'
    except ValueError:
        return 'R'

def process_table(tex_path, out_tex_path, out_csv_path, is_table4):
    with open(tex_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    out_lines = []
    csv_rows = []
    
    in_tabular = False
    
    for line in lines:
        if line.strip().startswith('\\begin{tabular}'):
            # add one column specification
            # \begin{tabular}{lllcrcccc} -> \begin{tabular}{lllccrcccc}
            # Actually just insert a 'c' before or after Events
            parts = re.split(r'(\{.*?\})', line)
            if len(parts) > 1:
                col_spec = parts[1]
                parts[1] = col_spec[:-1] + 'c}'
                line = "".join(parts)
            out_lines.append(line)
            in_tabular = True
            continue
            
        if line.strip().startswith('\\end{tabular}'):
            in_tabular = False
            out_lines.append(line)
            continue
            
        if not in_tabular:
            if '\\multicolumn' in line and 'Note:' in line:
                # Add note about reliability
                note = "Reliability is assigned by the number of test events in each bucket: Reliable (R: N >= 1000), Limited (L: 100 <= N < 1000), and Insufficient (I: N < 100). Insufficient results are reported descriptively only."
                line = line.replace('Note:', f'Note: {note}')
            out_lines.append(line)
            continue
            
        # We are inside tabular
        if line.strip().startswith('\\toprule') or line.strip().startswith('\\midrule') or line.strip().startswith('\\bottomrule'):
            out_lines.append(line)
            continue
            
        # It's a row
        cols = [c.strip() for c in line.split('&')]
        
        # Check if it's the header
        if 'Dataset' in cols[0] and 'Bucket' in cols[2]:
            if is_table4:
                # Table 4: Dataset & Model & Bucket & \#KCs & \#Events & AUC & ACC & NLL & RMSE
                # Add Rel. after Bucket or before #KCs
                cols.insert(3, 'Rel.')
            else:
                # Table 5: Dataset & Model & Bucket & \#Events & ECE & Brier & UNC & REL & RES
                cols.insert(3, 'Rel.')
            
            # Reconstruct header line
            out_lines.append(" & ".join(cols).replace('\\\\', '').strip() + " \\\\\n")
            
            # CSV header
            csv_header = [c.replace('\\#', '').replace('\\', '').strip() for c in cols]
            csv_header[-1] = csv_header[-1].replace('\\\\', '').strip()
            csv_rows.append(csv_header)
            continue
            
        # It's a data row
        if len(cols) > 3:
            # Check for \textbf in the line and strip if Insufficient
            if is_table4:
                # Dataset, Model, Bucket, #KCs, #Events
                n_events_col = 4
            else:
                # Dataset, Model, Bucket, #Events
                n_events_col = 3
                
            n_events_str = cols[n_events_col].replace('\\\\', '').strip()
            flag = get_reliability_flag(n_events_str)
            
            if flag == 'I':
                # Remove \textbf{} from this row
                for i in range(len(cols)):
                    cols[i] = re.sub(r'\\textbf\{(.*?)\}', r'\1', cols[i])
                    
            cols.insert(3, flag)
            
            out_lines.append(" & ".join(cols).replace('\\\\', '').strip() + " \\\\\n")
            
            # CSV row
            csv_row = [re.sub(r'\$.*?\$', lambda m: m.group(0).replace('$', ''), c).replace('\\\\', '').strip() for c in cols]
            csv_rows.append(csv_row)
        else:
            out_lines.append(line)

    with open(out_tex_path, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)
        
    with open(out_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)
        
process_table(
    'paper/tables/table4_metric_per_bucket.tex', 
    'paper/tables/table_iv_bucket_performance_with_reliability.tex',
    'results/tables/table_iv_bucket_performance_with_reliability.csv',
    is_table4=True
)

process_table(
    'paper/tables/table5_calibration_per_bucket.tex', 
    'paper/tables/table_v_calibration_with_reliability.tex',
    'results/tables/table_v_calibration_with_reliability.csv',
    is_table4=False
)
