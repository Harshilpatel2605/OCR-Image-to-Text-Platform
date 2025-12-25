import os

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def export_txt(text, job_id):
    path = f"{OUTPUT_DIR}/{job_id}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path
