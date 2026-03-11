# Mooring_query: Time Series Visualization Tool

Developed for INTECMAR by Pedro Montero.

## 🌊 Overview
This module handles **Mooring data** (fixed stations with sensors at specific depths). It retrieves historical observations from the INTECMAR API and generates high-quality time series plots.

## 🏗️ Project Structure
- `src/api/`: API clients (Base and Mooring specific).
- `src/data/`: Data processing (`mooring_processor.py`).
- `src/visualization/`: Time series plotting with multiple depth support.
- `src/models/`: Domain models for Measurements and Batches.
- `run_moorings.py`: Main launcher script.

## ⚙️ Configuration (`input_moorings.json`)
```json
{
    "begin_date": "YYYY-MM-DD",
    "end_date": "YYYY-MM-DD",
    "stations": ["15001", "15005"],
    "variables": ["TAU", "SAL", "Velocidade do Vento"],
    "frequency": "hourly",
    "function": "AVG",
    "output_dir": "plots"
}
```
- **Variables**: Can be the ParameterCode (e.g., "20003"), the Short Name (e.g., "TAU"), or the Description (e.g., "Temperatura da Auga").
- **Frequency**: `10minute`, `hourly`, `daily`, `monthly`.
- **Function**: Aggregation function (defaults to `AVG`).

## 📈 Visual Features
- **Multi-Depth Plotting**: If a station has sensors at different depths (e.g., 1m and 3m), the tool automatically plots them as separate lines in the same graph with clear labels.
- **Premium Aesthetics**: Professional-grade plots using Seaborn.
- **Dynamic Variable Matching**: Automatically resolves parameter IDs for each station.

## 🚀 Usage
```powershell
# Activate venv (reusing the one from CTD or creating new)
..\CTD\venv\Scripts\Activate.ps1

# Run the tool
python run_moorings.py
```

## 🛠️ Requirements
(Same as CTD module)
- `pandas`, `matplotlib`, `seaborn`, `requests`, `python-dotenv`.
