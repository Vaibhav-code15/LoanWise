<div align="center">

# 🏦 LoanWise

<p>A bank loan portfolio optimizer that compares Greedy and Dynamic Programming side by side.</p>

![C++](https://img.shields.io/badge/C%2B%2B-17-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557C?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</div>

---

## What is this?

Banks get more loan requests than they can fund. LoanWise finds the best combination of loans to approve — maximizing profit without exceeding the budget.

It solves the **0/1 Knapsack problem** two ways and lets you compare the results:

| Algorithm | Time Complexity | Always Optimal? |
|-----------|----------------|-----------------|
| Greedy | O(n log n) | ❌ |
| Dynamic Programming | O(n × W) | ✅ |

---

## Screenshots

### Home
![Home](images/01_home.png)

### Upload CSV
![CSV Upload](images/02_csv_upload.png)

### File Preview
![File Preview](images/03_file_preview.png)

### Portfolio Summary
![Portfolio Summary](images/04_portfolio_summary.png)

### Loan Distribution
![Loan Distribution](images/05_loan_distribution.png)

### Alternative Plan
![Alternative Plan](images/06_alternative_plan.png)

### Technical Analysis — Greedy vs DP
![Technical Analysis](images/07_technical_analysis.png)

### Expected Return Comparison
![Comparison Chart](images/08_comparison_chart.png)

---

## How it works

```
You upload a CSV  →  Python calls C++ binary  →  C++ runs both algorithms
→  returns JSON  →  Streamlit renders the dashboard
```

The C++ engine handles all the computation and outputs a clean JSON response. Python doesn't touch the algorithm logic — it just sends data in and displays what comes back.

---

## Project structure

```
LoanWise/
├── backend/
│   ├── main.cpp          ← entry point, reads CSV, outputs JSON
│   ├── greedy.cpp/h      ← greedy algorithm
│   ├── dp.cpp/h          ← 0/1 knapsack DP
│   ├── utils.cpp/h       ← CSV parser, data structs, JSON helpers
│   └── Makefile
├── frontend/
│   ├── streamlit_app.py  ← the entire dashboard
│   └── requirements.txt
├── data/                 ← sample CSV files to test with
├── images/               ← screenshots
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```

---

## Getting Started

**1. Compile the C++ backend**

```bash
cd backend
g++ -std=c++17 -O2 -o loan_optimizer main.cpp greedy.cpp dp.cpp utils.cpp
```

> Windows: use `loan_optimizer.exe` as the output name

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run**

```bash
cd frontend
streamlit run streamlit_app.py
```

Opens at `http://localhost:8501`

---

## CSV Format

```csv
id,loan_amount,interest_rate,credit_score
1,50000,7.5,720
2,30000,9.0,680
```

Sample files are in the `data/` folder. Start with `data5.csv`.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Engine Not Found" | Compile the C++ backend first |
| `g++ not found` | Windows: install [MinGW](https://www.mingw-w64.org/) · Linux: `sudo apt install g++` |
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| Blank page | Wait 5–10 seconds on first load |

---

## License

MIT — free to use and modify. See [LICENSE](LICENSE).

---

<div align="center">

**Vaibhav Khandelwal**  
B.Tech CSE · Jaypee Institute of Information Technology, Noida

[![GitHub](https://img.shields.io/badge/GitHub-Vaibhav--code15-181717?style=for-the-badge&logo=github)](https://github.com/Vaibhav-code15)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Vaibhav%20Khandelwal-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/vaibhav-khandelwal-5a532b28a/)

*If this helped you, a star would mean a lot ⭐*

</div>
