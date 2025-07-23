import re
import csv
import subprocess
from sys import argv
from tqdm import tqdm
from pathlib import Path
from typing import Dict, Type, Tuple, List
from dataclasses import asdict
from src.echo import echo
from src.schemas import BenchmarkConfig, PlotConfig, RuntimeConfig
from src.plotting import plot_combined_boxplot, plot_avg_ups_horizontal
from src.check import Check
from src.argparser import parse_args
from src.confprint import print_selected_config
from src.config import load_config
from src.schemas import BenchmarkResult
from src.meme import gotcha


def update_tqdm_from_line(line: str, progress: tqdm) -> None:
    """
    Parses a line of output to extract performed ticks and updates the tqdm bar.

    Args:
        line (str): A line from Factorio output.
        progress (tqdm): The active tqdm progress bar to update.
    """
    match = re.search(r"Performed\s+(\d+)\s+updates", line)
    if match:
        performed_ticks = int(match.group(1))
        progress.n = performed_ticks
        progress.refresh()


def parse_benchmark_output(
    lines: list[str], ticks: int, map_name: str, run_index: int, platform: str
) -> BenchmarkResult:
    def safe_get(regex: str, source: str, group: int = 1) -> str:
        match = re.search(regex, source)
        return match.group(group) if match else ""

    avg_line = next((l for l in lines if "avg:" in l), "")
    perf_line = next((l for l in lines if "Performed" in l), "")
    load_line = next((l for l in lines if "Loading script.dat" in l), "")
    version_line = next((l for l in lines if "Version" in l), lines[0] if lines else "")

    avg_ms = safe_get(r"avg:\s*([\d.,]+)", avg_line).replace(",", ".")
    min_ms = safe_get(r"min:\s*([\d.,]+)", avg_line).replace(",", ".")
    max_ms = safe_get(r"max:\s*([\d.,]+)", avg_line).replace(",", ".")

    execution_time_str = safe_get(r"in\s+([\d.,]+)", perf_line)
    execution_time = (
        float(execution_time_str.replace(",", ".")) if execution_time_str else 0.0
    )

    actual_ticks = int(safe_get(r"Performed\s+(\d+)\s+updates", perf_line) or 0)

    startup_time = load_line.split()[0] if load_line else ""
    end_time = lines[-1].split()[0] if lines else ""
    factorio_version = lines[0].split()[4] if len(lines[0].split()) >= 5 else ""

    try:
        effective_ups = (
            round(1000 * ticks / execution_time, 2) if execution_time else 0.0
        )
    except ZeroDivisionError:
        effective_ups = 0.0

    return BenchmarkResult(
        map_name=map_name,
        run_index=run_index,
        startup_time=startup_time,
        end_time=end_time,
        avg_ms=avg_ms,
        min_ms=min_ms,
        max_ms=max_ms,
        ticks=ticks,
        actual_ticks=actual_ticks,
        execution_time=(
            execution_time_str.replace(",", ".") if execution_time_str else "0.0"
        ),
        effective_ups=effective_ups,
        factorio_version=factorio_version,
        platform=platform,
    )


def run_benchmark(
    runtime: RuntimeConfig, benchmark: BenchmarkConfig, folder: str
) -> None:
    folder_path = Path("benchmarks") / folder
    output_csv = folder_path / benchmark.output_file

    Check.dir_exists(folder_path)
    maps = list(folder_path.glob(f"*{benchmark.map_pattern}"))
    Check.condition(
        bool(maps),
        f"No maps found with pattern '{benchmark.map_pattern}' in {folder_path}",
    )

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [field.name for field in BenchmarkResult.__dataclass_fields__.values()]
    with output_csv.open("w", newline="") as f_csv:
        writer = csv.DictWriter(f_csv, fieldnames=fieldnames)
        writer.writeheader()

        for run_idx in range(1, benchmark.runs + 1):
            for map_path in maps:
                echo(
                    f"Running benchmark: {map_path.name} [Run {run_idx}/{benchmark.runs}]"
                )
                args = [
                    str(runtime.factorio_executable),
                    "--benchmark",
                    str(map_path),
                    "--benchmark-ticks",
                    str(benchmark.ticks),
                ]

                if runtime.disable_audio:
                    args.append("--disable-audio")

                process = subprocess.Popen(
                    args,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    bufsize=1,
                    universal_newlines=True,
                )

                output_lines = []
                progress = tqdm(
                    total=benchmark.ticks,
                    desc="Ticks",
                    unit="tick",
                    leave=False,
                    dynamic_ncols=True,
                )

                for line in process.stdout:
                    line = line.strip()
                    output_lines.append(line)

                    match = re.search(r"Performed\s+(\d+)\s+updates", line)
                    if match:
                        current = int(match.group(1))
                        progress.n = current
                        progress.refresh()

                process.wait()
                progress.n = benchmark.ticks
                progress.close()

                result: BenchmarkResult = parse_benchmark_output(
                    output_lines,
                    benchmark.ticks,
                    map_path.name,
                    run_idx,
                    benchmark.platform,
                )

                writer.writerow(asdict(result))

    echo(f"Benchmark results saved to: {output_csv}", level="S")


def run_template(template_section) -> None:
    pass


def run_plot(
    benchmark: BenchmarkConfig, plot_cfg: PlotConfig, folder: str, csv_file: str
) -> None:
    folder_path = Path("benchmarks") / folder
    csv_path = folder_path / csv_file
    plots_path = folder_path / "plots"

    Check.dir_exists(folder_path)
    Check.file_exists(csv_path)

    plots_path.mkdir(parents=True, exist_ok=True)

    if plot_cfg.combined_boxplot:
        plot_combined_boxplot(csv_path, plots_path, plot_cfg)

    if plot_cfg.average_barplot:
        plot_avg_ups_horizontal(csv_path, plots_path, plot_cfg)


def run_selected_mode(
    mode: list[str],
    args: dict,
    runtime_section: RuntimeConfig,
    benchmark_section: BenchmarkConfig,
    plot_section: PlotConfig,
) -> None:
    if mode == "bench":
        run_benchmark(runtime_section, benchmark_section, args["folder"])
        echo("Benchmark completed successfully.", level="S")
        gotcha()
    elif mode == "plot":
        run_plot(benchmark_section, plot_section, args["folder"], args["csv"])
        echo("Plots generated.", level="S")
    elif mode == "template":
        run_template(benchmark_section, args)
        echo("Template exported.", level="S")


def main():
    args = parse_args(argv[1:])
    runtime, benchmark, plot = load_config(args["config"])
    if runtime.showconfiguration:
        print_selected_config(args["mode"], runtime, benchmark, plot)
    run_selected_mode(args["mode"], args, runtime, benchmark, plot)


if __name__ == "__main__":
    main()
