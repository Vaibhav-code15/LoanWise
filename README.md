
# 🏦 LoanWise

### Smart Bank Loan Portfolio Optimization System

**C++ Algorithm Engine · Python Streamlit Dashboard · Greedy Algorithm · Dynamic Programming (0/1 Knapsack)**

![C++](https://img.shields.io/badge/C%2B%2B-17-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

[![GitHub](https://img.shields.io/badge/GitHub-Vaibhav--code15-181717?style=flat-square&logo=github)](https://github.com/Vaibhav-code15)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Vaibhav%20Khandelwal-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/vaibhav-khandelwal-5a532b28a/)

---

## 📌 Overview

LoanWise is a bank loan portfolio optimization system that helps maximize expected annual interest income while staying within a fixed lending budget. It compares a **Greedy Algorithm** with **Dynamic Programming (0/1 Knapsack)** and presents the results through an interactive Streamlit dashboard.

---

## ✨ Features

- Loan portfolio optimization using Greedy and Dynamic Programming
- Interactive Streamlit dashboard
- CSV-based applicant upload
- Portfolio KPI dashboard
- Loan allocation insights
- Algorithm comparison
- Technical analysis section
- JSON communication between Python and C++
- Input validation and error handling

---

## 🖥️ Screenshots

### 1. Home – Upload CSV & Set Budget
![Home](images/01_home.png)

---

### 2. CSV Upload
![CSV Upload](images/02_csv_upload.png)

---

### 3. File Preview
![File Preview](images/03_file_preview.png)

---

### 4. Portfolio Summary
![Portfolio Summary](images/04_portfolio_summary.png)

---

### 5. Loan Distribution
![Loan Distribution](images/05_loan_distribution.png)

---

### 6. Alternative Plan
![Alternative Plan](images/06_alternative_plan.png)

---

### 7. Technical Analysis
![Technical Analysis](images/07_technical_analysis.png)

---

### 8. Expected Return Comparison
![Comparison Chart](images/08_comparison_chart.png)

---

## 🗂️ Project Structure

```text
LoanWise/
│
├── backend/
├── frontend/
│   └── streamlit_app.py
├── data/
├── images/
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## ⚙️ How It Works

1. Upload a CSV containing loan applicants.
2. Set the available bank budget.
3. Python invokes the C++ optimization engine.
4. Greedy and Dynamic Programming algorithms are executed.
5. Results are returned as JSON.
6. Streamlit visualizes KPIs, charts, selected applicants, and algorithm comparison.

---

## 🚀 Getting Started

### 1. Compile the C++ backend

```bash
cd backend
g++ -std=c++17 -O2 -o loan_optimizer main.cpp greedy.cpp dp.cpp utils.cpp
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the application

```bash
cd frontend
streamlit run streamlit_app.py
```

---

## 🧠 Algorithms Used

| Algorithm | Complexity | Optimal |
|-----------|------------|---------|
| Greedy | O(n log n) | No |
| Dynamic Programming (0/1 Knapsack) | O(n × W) | Yes |

---

## 🛠️ Tech Stack

- C++17
- Python
- Streamlit
- Pandas
- Matplotlib
- JSON
- Dynamic Programming
- Greedy Algorithm

---

## 📄 CSV Format

```csv
id,loan_amount,interest_rate,credit_score
1,50000,7.5,720
2,30000,8.0,690
```

---

## 📚 Concepts Demonstrated

- Design and Analysis of Algorithms
- Greedy Algorithms
- Dynamic Programming
- 0/1 Knapsack
- C++ and Python Integration
- JSON-based Communication
- Data Visualization
- Software Engineering

---

## 📃 License

This project is licensed under the MIT License.

---

## 👤 Author

**Vaibhav Khandelwal**

B.Tech Computer Science Engineering  
Jaypee Institute of Information Technology, Noida

**GitHub:** https://github.com/Vaibhav-code15

**LinkedIn:** https://www.linkedin.com/in/vaibhav-khandelwal-5a532b28a/

⭐ If you found this project useful, consider giving it a star.
