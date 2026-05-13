import subprocess
import sys

processes = []
xxx = 49

for batch_nb in range(xxx):  # 0 to 49
    p = subprocess.Popen([
        sys.executable,
        "wikiscroping.py",
        str(batch_nb)
    ])
    processes.append(p)

for p in processes:
    p.wait()
