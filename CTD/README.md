# CTD_query: Profile Recovery & Visualization Tool

Developed for INTECMAR by Pedro Montero.

## 🌊 Overview
This is **CTD_query**, a professional, object-oriented Python application designed to retrieve oceanographic CTD profile data from the INTECMAR API. It processes the raw data, exports structured Excel reports, and generates high-quality profile visualizations.

## 🏗️ Project Structure
- `src/api/`: API clients (Base and CTD specific).
- `src/data/`: Data processing (`processor.py`) and Excel exporting (`exporter.py`) logic.
- `src/visualization/`: Advanced profile plotting using Matplotlib and Seaborn.
- `src/models/`: Domain models for Profiles and Measurements.
- `run_ctd.py`: Integrated main launcher.
- `export_standalone.py`: Standalone script for Excel export only.
- `plots_standalone.py`: Standalone script for Profile plotting only.
- `heatmap_standalone.py`: Standalone script for Depth vs. Time heatmaps.

## ⚙️ Configuration Files

The tool uses a modular configuration system:

1.  **`input.json` (Common)**: 
    *   `begin_date` & `end_date`: Query time range.
    *   `stations`: Array of station codes (e.g., ["V3", "P3"]).
    *   `variables`: List of variables to retrieve.

2.  **`input_plots.json` (Profile Plotting Specifics)**:
    *   `plots_dir`: Output folder for images.
    *   ... (rest of settings)

3.  **`input_heatmap.json` (Heatmap Specifics)**:
    *   `top`: Starting depth for the Y-axis (meters).
    *   `bottom`: Meters to subtract from the station depth for the end range.
    *   `color_map`: Colormap to use (matplotlib names).

4.  **`input_export.json` (Export Specifics)**:
    *   `output_dir`: Output folder for Excel files.

## 📈 Plotting Features
- **Premium Aesthetics**: Professional look using Seaborn themes.
- **Multiple Subplots**: Each variable is plotted in its own subplot with a unique color.
- **Quality Indicators**:
    - **● Filled Circle**: Good Data (Flag 1).
    - **○ Hollow Circle**: No Control (Flag 0).
    - **❌ Black X**: Bad Data (Flag 4).
- **Inverted Y-Axis**: Depth is correctly shown with 0 at the top.
- **UTC Time**: Plots include the exact sampling time in UTC.

## 🚀 Usage

### 1. Setup
```powershell
# Create and activate venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment (NEVER commit the .env file)
cp .env.template .env
# Edit .env and add your INTECMAR credentials
```

### 2. Execution
- **Full Run**: `python run_ctd.py`
- **Only Excel**: `python export_standalone.py`
- **Only Plots**: `python plots_standalone.py`

## 🛠️ Requirements
- `pandas`: Data manipulation.
- `openpyxl`: Excel generation.
- `matplotlib` & `seaborn`: Visualization.
- `requests`: API interaction.
- `python-dotenv`: Environment variable management.
- `jsonpickle`: Object serialization (internal).

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
