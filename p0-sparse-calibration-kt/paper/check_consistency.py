import os

folder = r"c:\TRINH\P0\p0-sparse-calibration-kt\springer_upload_folder\tables"

tests = {
    "Table 3 ASSISTments DKT": r"0.6980 \pm 0.0013",
    "Table 3 ASSISTments SimpleKT": r"0.6840 \pm 0.0025",
    "Table 3 Junyi DKT": r"0.7317 \pm 0.0012",
    "Table 3 XES3G5M DKT": r"0.8170 \pm 0.0028",
    "Table 5 XES3G5M dense DKT": r"0.8168",
    "Table 5 XES3G5M dense SimpleKT": r"0.7547",
    "Table 5 XES3G5M sparse DKT": r"0.8590",
    "Table 5 XES3G5M sparse SimpleKT": r"0.8509",
    "Table 5 XES3G5M very sparse DKT": r"0.8413",
    "Table 5 XES3G5M very sparse SimpleKT": r"0.8379",
    "Table 6 ASSISTments warm DKT": r"0.6606",
    "Table 6 ASSISTments warm SimpleKT": r"0.6734", # actually 0.6734? Let's check Table 6 SimpleKT ASSISTments warm.
    "Table 6 Junyi warm DKT": r"0.6949",
    "Table 6 Junyi warm SimpleKT": r"0.7167",
    "Table 6 XES3G5M warm DKT": r"0.6626",
    "Table 6 XES3G5M warm SimpleKT": r"0.6615",
    "Figure 3/Table C5 Junyi SimpleKT dense ECE": r"0.0889",
    "Figure 3/Table C5 Junyi SimpleKT dense N": r"3,072,767",
    "Figure 3/Table C5 Junyi SimpleKT very sparse ECE": r"0.0841",
    "Figure 3/Table C5 Junyi SimpleKT very sparse N": r"2,545"
}

for root, dirs, files in os.walk(folder):
    for file in files:
        if file.endswith('.tex'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                for test_name, query in list(tests.items()):
                    if query in content:
                        print(f"PASS: {test_name} ({query}) found in {file}")
                        del tests[test_name]

for test_name, query in tests.items():
    print(f"FAIL: {test_name} ({query}) NOT FOUND")

