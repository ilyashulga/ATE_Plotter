# ATE Export Data Comparison Tool

This program facilitates the uploading and comparison of two or more "ATE Export" files in the `.xlsx` format. Leveraging the power of Python, Dash, Plotly, and Pandas, it offers a user-friendly interface to visually compare distributions of measurement data across different "ATE export" files.

## Key Features:

- **Multi-file Upload**: Upload two or more `.xlsx` ATE Export files (THE FILES SHOULD HAVE THE SAME COLUMN NAMES)
- **Visual Comparison**: Seamlessly compare the data distributions from different files using interactive graphs.
- **Flexible Adjustments**: Customize your data visualizations with the following tools:
  - **Bin Size Selector**: Choose the appropriate granularity for your histograms.
  - **Value Exclusion Tools**: 
    - **Exclude Above**: Omit data values above a certain threshold.
    - **Exclude Below**: Exclude data values below a particular point.
  - **Column-specific Filter**: Isolate and view data based on specific column contents.

## Prerequisites:

To run this program, ensure you have the following libraries installed:

- `dash`
- `plotly`
- `pandas`
- `openpyxl`

## How to Run:

1. Ensure you have all the required libraries installed:
    ```bash
    pip install dash plotly pandas openpyxl
    ```

2. Run the Python script.
3. Open the provided link in a web browser.
4. Use the interface to upload the required `.xlsx` files and utilize the available adjustments to customize your visualization.

## Screenshot:
![Screenshot](https://github.com/ilyashulga/ATE_Plotter/assets/107320352/f3c9caac-1fa3-4857-a20b-8f8925b7e5db)
