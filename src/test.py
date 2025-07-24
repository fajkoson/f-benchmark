from tqdm import tqdm
import time

progress = tqdm(total=5000, desc="Ticks", unit="tick", leave=True, dynamic_ncols=True)
for i in range(0, 5001, 100):
    # progress.write(f"Running update {i}")
    progress.update(100)
    time.sleep(0.1)
progress.n = 5000
progress.close()
