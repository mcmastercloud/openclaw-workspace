import os
import sys
import glob

def prepare_uploads(staging_dir):
    delta_files = glob.glob(os.path.join(staging_dir, "*-Delta.txt"))
    if not delta_files:
        print("No Delta files found.")
        return

    upload_dir = os.path.join(staging_dir, "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    
    total_prepared = 0
    for delta_path in delta_files:
        with open(delta_path, 'r') as f:
            lines = f.readlines()
        
        # Filter out HOLDING_IGNORE as per SOP
        upload_content = [line for line in lines if "HOLDING_IGNORE" not in line]
        
        if upload_content:
            account_id = os.path.basename(delta_path).replace("-Delta.txt", "")
            upload_path = os.path.join(upload_dir, f"{account_id}-Upload.txt")
            with open(upload_path, 'w') as f:
                f.writelines(upload_content)
            total_prepared += 1
            print(f"Prepared upload for {account_id}: {len(upload_content)} transactions.")

    print(f"Total upload files prepared: {total_prepared}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 prepare-upload-files.py <staging_dir>")
    else:
        prepare_uploads(sys.argv[1])
