# Factorio Benchmark Runner

A configurable benchmarking system for Factorio maps.

Shout out to [abucnasty](https://github.com/abucnasty), I highly recommend to check his channel on [youtube](https://www.youtube.com/@abucnasty), who introduced benchmarking of Factorio to me.

---

## How It Works

1. ✅ Install Python 3.12.6+ and run `install_env.bat` to set up the virtual environment  
2. 📦 Place `.zip` benchmark maps inside a subfolder in `benchmarks/`  
3. ⚙️ Create or modify `.cfg` files in the `config/` folder to adjust benchmark settings  
4. ▶️ Run the script with your desired folder and optional config [HOW TO USE HERE](https://github.com/fajkoson/bp-factorio/blob/main/docs/usage.md)  
5. 📈 Results will be stored as `.csv` files in the same benchmark folder

6. 🔧 `ticks` controls benchmark duration (e.g. `3600` ticks ≈ 1 in-game minute)  
7. 📁 Factorio mods can be managed at: `%APPDATA%\\Factorio\\mods\\`

## Mod-list

- [Base mod] (game)
- [Elevated Rails] (game)
- [Quality] (game)
- [Space Age] (game)
- [Editor Extensions/Testing](https://mods.factorio.com/mod/EditorExtensions) (c)raiguard
- [Factorio Library](https://mods.factorio.com/mod/flib) (c)raiguard
- [Rate Calculator](https://mods.factorio.com/mod/RateCalculator) (c)raiguard
- [Region Cloner](https://mods.factorio.com/mod/region-cloner) (c)mulark
- [Testbenchcontrols](https://mods.factorio.com/mod/Testbenchcontrols) (c)HansJoachim

---

## Links

- [Commands](https://github.com/fajkoson/bp-factorio/blob/main/docs/commands.md)
- [Factorio Wiki - Main page](https://wiki.factorio.com/Main_Page)
- [Factorio Wiki - Command line](https://wiki.factorio.com/Command_line_parameters)
- [Factorio Wiki - Console](https://wiki.factorio.com/Console)
- [Factorio Mods](https://mods.factorio.com/)
- [Matplotlib colors](https://matplotlib.org/stable/gallery/color/named_colors.html)
- [Matplotlib boxplot](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.boxplot.html)

## TODO

- simple GUI
- mod-list.json handling and enabling mods with this
- verbose
  