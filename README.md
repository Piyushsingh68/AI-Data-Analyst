# 🤖 AI Data Analyst

An AI-powered data analysis dashboard built with Python, Pandas, Streamlit, Matplotlib, and local AI.

The application allows users to upload CSV or Excel datasets and automatically perform data analysis, generate charts, calculate KPIs, detect data-quality issues and outliers, analyze time-based trends, and ask questions about their data.

## 🚀 Live Demo

**Streamlit Dashboard:**  
https://ai-data-analyst-piyush.streamlit.app/

**GitHub Repository:**  
https://github.com/Piyushsingh68/AI-Data-Analyst

## 📌 Project Overview

AI Data Analyst is a web-based analytics application designed to simplify the process of exploring and understanding datasets.

The application automatically examines an uploaded dataset and provides:

- Dataset overview
- Column and data-type analysis
- Missing-value detection
- Duplicate-row detection
- Numerical statistics
- Categorical analysis
- KPI calculations
- Business insights
- Automatic charts
- Time-series analysis
- Trend analysis
- Outlier detection
- Correlation analysis
- AI-generated insights
- Natural-language questions about the dataset

The project is designed to work with different CSV and Excel datasets rather than being limited to a single dataset.

## ✨ Features

### 📊 Dataset Analysis

Automatically identifies:

- Number of rows
- Number of columns
- Column names
- Numerical columns
- Categorical columns
- Date/time columns
- Unique values
- Missing values
- Duplicate rows

### 📈 Statistical Analysis

For numerical columns, the application calculates:

- Count
- Sum
- Average
- Minimum
- Maximum
- Statistical summaries

### 💰 KPI Generator

The KPI module automatically calculates important metrics for numerical columns.

Examples:

- Total Sales
- Average Sales
- Minimum Sales
- Maximum Sales
- Total Profit
- Average Profit
- Total Quantity

### 📉 Automatic Charts

The application automatically generates visualizations based on the available dataset columns.

Supported charts include:

- Bar charts
- Line charts
- Trend-line charts
- Scatter plots
- Histograms

### 🕒 Time Analysis

If a dataset contains a date column, the application can perform:

- Monthly analysis
- Yearly analysis
- Best-performing period analysis
- Worst-performing period analysis
- Time-based sales analysis
- Time-based profit analysis
- Trend analysis

### 🚨 Outlier Detection

The application detects potential outliers in numerical columns using the IQR (Interquartile Range) method.

The analysis identifies:

- Lower bound
- Upper bound
- Number of outliers
- Outlier values

### 🔍 Correlation Analysis

When multiple numerical columns are available, the application calculates correlations between numerical variables.

This can help identify relationships between metrics such as:

- Sales and Profit
- Sales and Quantity
- Profit and Quantity

### 🧠 Automatic Business Analysis

The application analyzes the dataset and identifies important business findings such as:

- Highest-performing category
- Lowest-performing category
- Total values
- Average values
- Data-quality issues
- Important numerical patterns

The analysis uses actual dataset values.

### 🤖 AI Data Analyst

The project includes a local AI-powered analysis feature using Ollama and the Qwen 2.5 3B model.

The AI receives verified findings from the Python analysis modules and generates business-oriented insights.

This helps keep AI-generated responses grounded in the actual dataset.

### 💬 Ask Your Data

Users can ask questions about their dataset using natural language.

Example questions:

- What is the total sales?
- Which region has the highest sales?
- Which region has the lowest sales?
- Show sales by region.
- Compare Laptop and Mobile sales.
- What is the average sales?
- What is the highest sales?

The application interprets the question and attempts to return an answer based on the uploaded dataset.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- OpenPyXL
- Ollama
- Qwen 2.5 3B
- Git
- GitHub

## 📂 Project Structure

```text
AI_Data_Analyst/
├── app.py
├── ai_insights.py
├── analyzer.py
├── ask_data.py
├── charts.py
├── database.py
├── insight_engine.py
├── kpi_generator.py
├── outlier_detector.py
├── report_generator.py
├── time_analysis.py
├── data/
│   └── sales_data.csv
├── reports/
├── requirements.txt
├── README.md
└── .gitignore
```

## 🔎 Module Description

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application |
| `analyzer.py` | Dataset structure and statistical analysis |
| `charts.py` | Automatic chart generation |
| `kpi_generator.py` | KPI calculations |
| `outlier_detector.py` | IQR-based outlier detection |
| `time_analysis.py` | Date and time-based analysis |
| `insight_engine.py` | Business insight generation |
| `ai_insights.py` | Local AI-powered insights |
| `ask_data.py` | Natural-language dataset questions |
| `database.py` | Dataset/database handling |
| `report_generator.py` | Report-generation functionality |

## 📋 Sample Dataset

The project includes a sample sales dataset containing:

- Date
- Product
- Region
- Sales
- Profit
- Quantity

Example products:

- Laptop
- Mobile
- Tablet

Example regions:

- North
- South
- East
- West

## 📊 Sample Analysis

The included sample dataset contains 15 rows.

### Sales

- Total Sales: 997,000
- Average Sales: 66,466.67
- Minimum Sales: 30,000
- Maximum Sales: 110,000

### Profit

- Total Profit: 199,400
- Average Profit: 13,293.33
- Minimum Profit: 6,000
- Maximum Profit: 22,000

### Quantity

- Total Quantity: 84
- Average Quantity: 5.6

### Regional Sales

| Region | Sales |
|---|---:|
| West | 300,000 |
| North | 270,000 |
| South | 235,000 |
| East | 192,000 |

The West region has the highest total sales in the sample dataset.

### Product Sales

| Product | Sales |
|---|---:|
| Laptop | 555,000 |
| Mobile | 295,000 |
| Tablet | 147,000 |

Laptop has the highest total sales among the products in the sample dataset.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Piyushsingh68/AI-Data-Analyst.git
```

### 2. Open the project folder

```bash
cd AI-Data-Analyst
```

### 3. Create the Conda environment

```bash
conda create -n ai_data_analyst python=3.11
```

### 4. Activate the environment

```bash
conda activate ai_data_analyst
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## 🤖 Running Local AI

The AI features use Ollama locally.

Pull the Qwen model:

```bash
ollama pull qwen2.5:3b
```

Run the model:

```bash
ollama run qwen2.5:3b
```

The application communicates with the local Ollama API.

## ☁️ Streamlit Deployment

The Streamlit dashboard is deployed using Streamlit Community Cloud.

**Live Application:**

https://ai-data-analyst-piyush.streamlit.app/

The basic dashboard functionality can run in the cloud using the dependencies listed in `requirements.txt`.

The local Ollama-based AI functionality requires a locally running Ollama service and is separate from the basic cloud deployment.

## 🎯 Use Cases

This project can be used for:

- Sales analysis
- Business reporting
- Exploratory Data Analysis
- KPI monitoring
- Data-quality checking
- Time-series analysis
- Outlier detection
- Basic business intelligence
- Natural-language data exploration

## 📚 What I Learned

Through this project, I worked with:

- Python data analysis
- Pandas and NumPy
- Data cleaning and profiling
- Statistical analysis
- Data visualization
- Streamlit application development
- Modular Python development
- Natural-language data analysis
- Local AI integration
- Ollama API
- Git and GitHub
- Streamlit deployment

## 👨‍💻 Author

**Piyush Singh**

B.Sc. Physical Science with Computer Science  
Motilal Nehru College, University of Delhi

**GitHub:**  
https://github.com/Piyushsingh68

## ⭐ Future Improvements

Possible future enhancements include:

- More advanced natural-language querying
- More visualization types
- Automated PDF and Excel reports
- Improved AI-powered analysis
- Advanced forecasting
- Machine-learning based predictions
- User authentication
- Cloud-based AI integration
