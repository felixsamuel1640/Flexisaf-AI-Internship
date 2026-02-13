# Data Ingestion & Cleaning Pipeline

## Project Overview
This project demonstrates a robust data ingestion pipeline using Python and Pandas. 
The goal was to load data from multiple formats (CSV, JSON, and TXT), perform data 
cleaning, and conduct basic Exploratory Data Analysis (EDA).

## Features
- **Multi-format Ingestion:** Supports loading `.csv`, `.json`, and `.txt` 
(tab-separated) files.
- **Data Normalization:** Standardizes column headers by stripping whitespace and 
converting to lowercase.
- **Handling Missing Values:** Identifies null values using `.info()` and imputes 
missing categorical data with "Unknown".
- **Exploratory Data Analysis (EDA):** Provides statistical summaries and frequency 
distributions for key columns.
- **Export:** Saves the final processed data to a standardized CSV format.

## File Structure
- `data/`: Contains raw source files.
- `notebook.ipynb`: The main data processing workspace.
- `cleaned_addiction_data.csv`: The final output of the pipeline.
