import os

def delete_ds_store(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower() == ".ds_store":
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

if __name__ == "__main__":
    folder_path = "DSA"  # Change this to the absolute path if needed
    if os.path.exists(folder_path):
        delete_ds_store(folder_path)
    else:
        print(f"Folder '{folder_path}' not found.")
