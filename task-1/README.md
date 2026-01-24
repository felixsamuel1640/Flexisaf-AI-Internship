# AI Engineering Internship: Week 1 - Text Processing Pipeline

## 📌 Project Overview
This repository contains my first-week project for the AI Engineering Internship. 
The goal was to build a robust Python script capable of transforming "messy" raw 
text into structured data suitable for AI model training or analysis.

**Developed as part of the AI Engineering Internship at Flexisaf, focusing on data 
pipeline efficiency.**

## 🛠️ Key Features
* **Text Normalization:** Automatically converts text to lowercase and strips 
unnecessary punctuation (`!`, `.`, `,`).
* **Custom Tokenization:** Efficiently splits sentences into individual word units.
* **Stopword Filtering:** Implements a removal logic to filter out high-frequency, 
low-meaning words (e.g., "the", "is", "and").
* **Data Export:** Utilizes Python's `csv` module to generate a structured 
frequency report.

## 📂 Project Structure
* `main.py`: The core Python script containing the cleaning and counting logic.
* `cleaned_ai_report.csv`: The output file generated after running the script.
* `README.md`: Documentation for the project.

## 🚀 How To Run
1.  **Clone the repository** or download the `main.py` file.
2.  **Run the script** using your terminal or IDE:
    ```bash
    python main.py
    ```
3.  **Check the output:** A new file named `cleaned_ai_report.csv` will be created 
in your directory.

## 📈 Future Improvements
* Integrate **Pandas** for more advanced data manipulation and larger datasets.
* Utilize **Regex (Regular Expressions)** for more complex noise removal.
* Connect to an external API to fetch real-time data.

---
**Author:** Felix  
**Date:** January 2026
