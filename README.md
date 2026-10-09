# AI Data Analyst

An AI-powered data analysis web application built with Python and Streamlit that allows users to upload CSV/Excel datasets and automatically generate data analysis, KPIs, visualizations, time-based analysis, outlier detection, and AI-powered business insights.

## Live Demo

https://ai-data-analyst-piyush.streamlit.app/

## GitHub Repository

https://github.com/Piyushsingh68/AI-Data-Analyst

---

## Project Overview

The AI Data Analyst simplifies the data analysis workflow by combining traditional Python-based data analysis with AI-generated business insights.

Users can upload a CSV or Excel file, and the application automatically analyzes the dataset and presents useful information through an interactive Streamlit dashboard.

The application can:

- Analyze dataset structure
- Detect numerical, categorical, and date columns
- Calculate KPIs
- Detect missing values
- Detect duplicate records
- Detect statistical outliers
- Generate automatic visualizations
- Perform time-based analysis
- Identify verified business findings
- Generate AI-powered business insights

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- SQLite
- Requests
- Ollama
- Groq API
- Git
- GitHub

---

## Key Features

### Dataset Upload

Supports:

- CSV files
- Excel (`.xlsx`) files

### Dataset Analysis

Automatically identifies:

- Number of rows
- Number of columns
- Column names
- Numerical columns
- Categorical columns
- Date/time columns
- Missing values
- Duplicate rows
- Unique values

### KPI Generation

For numerical columns, the application calculates:

- Total
- Average
- Minimum
- Maximum
- Count

### Outlier Detection

The application uses the Interquartile Range (IQR) method to identify potential outliers in numerical columns.

### Automatic Data Visualization

The application can automatically generate:

- Bar charts
- Line charts
- Trend-line charts
- Scatter plots
- Histograms

### Time Analysis

When a date column is detected, the application can analyze:

- Monthly trends
- Yearly trends
- Best-performing periods
- Worst-performing periods

### Verified Business Findings

Before sending information to the AI model, the application generates verified findings directly from the dataset.

This helps ensure that AI-generated insights are based on actual calculated results rather than unsupported assumptions.

### AI-Powered Insights

The application supports:

**Local AI**
- Ollama
- Qwen 2.5 3B

**Cloud AI fallback**
- Groq API
- GPT-OSS 20B

If the local AI service is unavailable or times out, the application can use Groq as a fallback.

---

## AI Insight Workflow

```text
Upload Dataset
      ↓
Dataset Analysis
      ↓
KPI Generation
      ↓
Statistical Analysis
      ↓
Verified Findings
      ↓
Local Ollama AI
      ↓
If unavailable
      ↓
Groq API
      ↓
Business Insights
```

The AI receives verified analytical findings rather than directly performing calculations on the raw dataset.

---

## Example

For a sales dataset containing:

- Date
- Region
- Product
- Sales
- Profit
- Quantity

The application can identify findings such as:

```text
Overall average Sales = 66466.67

Highest individual Sales value = 110000.00

Lowest individual Sales value = 30000.00

Highest Region Sales total = West with 300000.00

Lowest Region Sales total = East with 192000.00
```

The AI then converts these verified findings into readable business insights.

---

## Project Structure

```text
AI_Data_Analyst/
│
├── app.py
├── ai_insights.py
├── analyzer.py
├── charts.py
├── database.py
├── insight_engine.py
├── kpi_generator.py
├── outlier_detector.py
├── report_generator.py
├── time_analysis.py
├── ask_data.py
├── requirements.txt
├── README.md
│
├── data/
│   └── sales_data.csv
│
└── reports/
```

---

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/Piyushsingh68/AI-Data-Analyst.git
```

### 2. Open the project

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

The application will open at:

```text
http://localhost:8501
```

---

## Local AI Setup

The project can use Ollama for local AI processing.

```bash
ollama pull qwen2.5:3b
```

Then run:

```bash
ollama run qwen2.5:3b
```

---

## Cloud Deployment

The application is deployed using Streamlit Community Cloud.

The deployed application uses the Groq API for cloud-based AI processing.

The API key should be stored securely using Streamlit Secrets or an environment variable.

Never commit API keys to GitHub.

---

## Security

API credentials are not stored directly in the source code.

The application retrieves the Groq API key through environment variables or Streamlit Secrets.

```text
GROQ_API_KEY
```

API keys should never be uploaded to GitHub.

---

## Skills Demonstrated

- Python programming
- Pandas data analysis
- NumPy
- Data cleaning
- Exploratory Data Analysis
- Statistical analysis
- KPI development
- Data visualization
- Time-series analysis
- Outlier detection
- Streamlit application development
- REST API integration
- Local LLM integration
- Cloud AI integration
- Git/GitHub
- Application deployment

---

## Author

**Piyush Singh**

B.Sc. Physical Science with Computer Science  
Motilal Nehru College, University of Delhi

### Project Links

Live Application:  
https://ai-data-analyst-piyush.streamlit.app/

GitHub:  
https://github.com/Piyushsingh68/AI-Data-Analyst
