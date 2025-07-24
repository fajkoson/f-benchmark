import re
from tqdm import tqdm
from typing import Callable


def progress_bar(read_func: Callable[[], str], total_ticks: int) -> list[str]:
    progress = tqdm(
        total=total_ticks,
        desc="Ticks",
        unit="tick",
        leave=False,
        dynamic_ncols=True,
    )

    buffer = ""
    output_lines = []
    last_tick = 0

    while True:
        out = read_func()
        if not out:
            break
        buffer += out

        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            line = line.strip()

            # Only keep specific lines
            if re.search(r"Running update\s+(\d+)", line):
                output_lines.append(line)

            match = re.search(r"Running update\s+(\d+)", line)
            if match:
                current = int(match.group(1))
                delta = current - last_tick
                if delta > 0:
                    progress.update(delta)
                last_tick = current

    progress.n = total_ticks
    progress.close()
    return output_lines

