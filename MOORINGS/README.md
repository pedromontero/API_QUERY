# Mooring_query: Time Series Visualization and Export Tool

Developed for INTECMAR by Pedro Montero.

## 🌊 Overview
This module handles **Mooring data** (fixed stations with sensors at specific depths). It retrieves historical observations from the INTECMAR API, generates high-quality time series plots, and exports data to structured Excel files.

## 🏗️ Project Structure
- `src/api/`: API clients (Base and Mooring specific).
- `src/data/`: Data processing and Excel export (`mooring_processor.py`, `mooring_exporter.py`).
- `src/visualization/`: Time series plotting with multiple depth support.
- `src/models/`: Domain models for Measurements and Batches.
- `run_moorings.py`: Main launcher script that executes both plotting and export.
- `plots_standalone.py`: Tool for generating plots only.
- `export_standalone.py`: Tool for generating Excel files only.

## ⚙️ Configuration
The configuration is split into three files to maintain modularity:

### 1. `input.json` (Common)
```json
{
    "begin_date": "2023-01-01",
    "end_date": "2023-01-15",
    "stations": ["15001", "15005"],
    "variables": ["TAU", "SAL", "Velocidade do Vento"],
    "frequency": "hourly",
    "function": "AVG"
}
```

### 2. `input_plots.json` (Plotting specific)
```json
{
    "plots_dir": "plots"
}
```

### 3. `input_export.json` (Export specific)
```json
{
    "output_dir": "output"
}
```

- **Variables**: Can be the ParameterCode (e.g., "20003"), the Short Name (e.g., "TAU"), or the Description.
- **Filtering**: Data with **QualityCode 9** is automatically excluded from both plots and Excel files.

## 📈 Features
- **Multi-Depth Plotting**: Automatic comparison of sensors at different depths in a single graph.
- **Excel Export**: Structured files with timestamp and value/flag columns for each variable and depth.
- **Premium Aesthetics**: Professional-grade plots using Seaborn.
- **Dynamic Variable Matching**: Automatically resolves parameter IDs for each station.

## 🚀 Usage
```powershell
# Activate venv
..\CTD\venv\Scripts\Activate.ps1

# Run everything (Plots + Excel)
python run_moorings.py

# Or run parts separately
python plots_standalone.py
python export_standalone.py
```

## 🛠️ Requirements
- `pandas`, `matplotlib`, `seaborn`, `requests`, `python-dotenv`, `openpyxl`.
