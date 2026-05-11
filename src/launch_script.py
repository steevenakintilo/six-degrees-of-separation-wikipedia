import subprocess
import sys

processes = []

for batch_nb in range(51):  # 0 to 49
    p = subprocess.Popen([
        sys.executable,
        "wikisraping.py",
        str(batch_nb)
    ])
    processes.append(p)

for p in processes:
    p.wait()