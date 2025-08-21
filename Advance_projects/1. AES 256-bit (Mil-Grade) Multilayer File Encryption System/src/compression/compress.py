import zipfile
import os

def compress_file_or_folder(path):
    zip_path = path + ".zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, path))
        else:
            zipf.write(path, os.path.basename(path))
    return zip_path