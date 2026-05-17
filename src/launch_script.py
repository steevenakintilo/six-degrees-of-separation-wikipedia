import subprocess
import sys

processes = []
xxx = 100
for batch_nb in range(xxx):  # 0 to xxx
    p = subprocess.Popen([
        sys.executable,
        "wikisraping.py",
        str(batch_nb)
    ])
    processes.append(p)

for p in processes:
    p.wait()
