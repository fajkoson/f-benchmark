# 🛠️ Benchmarking CLI — Usage Guide

This document explains how to use the `benchmark.py` tool for benchmarking, plotting, and (eventually) templating results from Factorio simulations.

---

## ⚙️ Defaults

- If `--mode` is omitted, it defaults to `bench`
- If `--config` is omitted, it defaults to `default.cfg` from the `config/` folder
- The first positional argument is always the `<folder>` inside the `benchmarks/` directory
- Only one mode (`bench`, `plot`, or `template`) is allowed per run

---

## 🅰️ Benchmark Mode

### 🔧 Usage

python benchmark.py --mode bench <folder> [--config=<cfgname>]

### 📝 Description

- Runs Factorio benchmarks on maps inside `benchmarks/<folder>/`
- Loads benchmark config from `config/<cfgname>` (default: `default.cfg`)
- Outputs `results.csv` into the same folder

### 🧪 Example

python benchmark.py --mode bench 0001-iron-smelter

---

## 🅱️ Plot Mode

### 🔧 Usage

python benchmark.py --mode plot <folder> [--config=<cfgname>] [--csv=<filename>]

### 📝 Description

- Reads a CSV file from `benchmarks/<folder>/`
- Generates performance plots in `benchmarks/<folder>/plots/`
- Uses plotting options from `config/<cfgname>`

### 🧪 Examples

python benchmark.py --mode plot 0001-iron-smelter  
python benchmark.py --mode plot 0030-copper --csv=custom.csv

---

## 🅲️ Template Mode (planned)

- Not implemented yet — `run_template()` is a placeholder.

---

## ✅ Summary

- Use `--mode` to select operation: `bench`, `plot`, or `template`
- Use `<folder>` to select which benchmark folder to process
- Configs are always loaded from `config/<name>.cfg`
- Output is placed back into the selected `benchmarks/<folder>/`

You're now ready to benchmark like a pro. 🚀

---

## 📁 Project Structure

```text
proj_root/
├── benchmarks/
│   └── 0001-iron-smelter/
│       ├── iron_smelter_enable_clocked.zip
│       ├── ...
│       └── results.csv             # Generated output file
│
├── config/
│   └── default.cfg                 # Default config
│ 
├── docs
│   ├── commands.md                 # Factorio commands
│   └── usage.md                    # how to use this script
│ 
├── mods
│   └── mod-list.json               # not implemented yet
│    
├── src/                            # Relevant import modules for benchmark.py
│
├── template/                       # Templates for generating .md into benchmark folders
│
├── tool/                           
│   └── requirements.txt            # Modules installed via pip install into .env
│
├── benchmark.py                    # Main benchmarking logic (Python)
├── benchmark.bat                   # Windows-friendly launcher
├── install_env.bat                 # Installation of virtual environment
└── README.md                       # Project overview
```
