import os
import shutil

def main():
    root = r"c:\TRINH\P0\p0-sparse-calibration-kt"
    source_dir = os.path.join(root, "jedm_upload_folder")
    output_zip = os.path.join(root, "jedm_upload_folder")
    
    shutil.make_archive(output_zip, 'zip', source_dir)
    print(f"Created zip archive: {output_zip}.zip")

if __name__ == "__main__":
    main()
