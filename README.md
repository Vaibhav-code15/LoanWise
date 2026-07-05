<div align="center">

# 🏦 Smart Bank Loan Optimizer

### Greedy Algorithm vs Dynamic Programming (0/1 Knapsack)
**C++ Algorithm Engine · Python Streamlit Dashboard · DAA Academic Project**

<br>

![C++](https://img.shields.io/badge/C%2B%2B-17-00599C?style=for-the-badge&logo=cplusplus&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7%2B-11557C?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

<br>

[![GitHub](https://img.shields.io/badge/GitHub-Vaibhav--code15-181717?style=flat-square&logo=github)](https://github.com/Vaibhav-code15)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Vaibhav%20Khandelwal-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/vaibhav-khandelwal)

</div>

---

## 📌 What This Project Does

Banks receive hundreds of loan requests but have **limited capital**. This system helps a bank decide **which loans to approve** to **maximize total profit** (annual interest income) without exceeding the available budget.

This is a real-world application of the **0/1 Knapsack Problem**, solved and compared using two classic algorithms:

| Algorithm | Strategy | Time Complexity | Space Complexity | Optimal? |
|-----------|----------|-----------------|------------------|----------|
| **Greedy** | Sort by profit/loan ratio, pick greedily | O(n log n) | O(n) | ❌ Not always |
| **Dynamic Programming** | Full 2D DP table + backtracking | O(n × W) | O(n × W) | ✅ Always |

---

## 🖥️ Screenshots

### 1. Home — Upload CSV & Set Budget
![Home Screen](images/01_home.png)

---

### 2. File Preview — Loaded Applicants
![File Preview](images/03_file_preview.png)

---

### 3. Portfolio Summary — KPI Dashboard
![Portfolio Summary](images/04_portfolio_summary.png)

---

### 4. Loan Distribution Insight
![Loan Distribution](images/05_loan_distribution.png)

---

### 5. Alternative Plan (Greedy Result)
![Alternative Plan](images/06_alternative_plan.png)

---

### 6. Technical Analysis — Greedy vs DP
![Technical Analysis](images/07_technical_analysis.png)

---

### 7. Expected Return Comparison Chart
![Comparison Chart](images/08_comparison_chart.png)

---

## 🗂️ Project Structure

```
smart-bank-loan-optimizer/
│
├── backend/                    ← C++ Algorithm Engine
│   ├── main.cpp                ← Entry point · args parsing · JSON output
│   ├── greedy.cpp / greedy.h   ← Greedy algorithm
│   ├── dp.cpp / dp.h           ← 0/1 Knapsack DP algorithm
│   ├── utils.cpp / utils.h     ← CSV loader · Applicant struct · JSON helpers
│   └── Makefile                ← Build system
│
├── frontend/                   ← Python Streamlit Dashboard
│   ├── streamlit_app.py        ← Web dashboard (~1300 lines)
│   └── requirements.txt        ← Python dependencies
│
├── data/                       ← Sample CSV datasets
│   ├── data2.csv               ← 7 applicants
│   ├── data3.csv               ← 5 applicants
│   ├── data4.csv               ← 4 applicants
│   └── data5.csv               ← 15 applicants (best for testing)
│
├── images/                     ← Screenshots for README
│
├── .gitignore
├── LICENSE
├── requirements.txt            ← Root-level Python deps
├── setup.bat                   ← One-click setup for Windows
├── setup.sh                    ← One-click setup for Linux/macOS
└── README.md
```

---

## ⚙️ How It Works

```
┌──────────────────────┐      CSV file + Budget      ┌─────────────────────┐
│  Streamlit Frontend  │  ─────────────────────────►  │  C++ Backend Engine │
│     (Python)         │                              │                     │
│  • Upload CSV        │  ◄─────────────────────────  │  • Greedy Algorithm │
│  • Set Budget        │       JSON Results           │  • DP Knapsack      │
│  • View KPI Cards    │                              │  • Outputs JSON     │
│  • Compare Algos     │                              └─────────────────────┘
│  • Download Report   │
└──────────────────────┘
```

1. Upload a CSV of loan applicants
2. Python calls the compiled C++ binary via `subprocess`
3. C++ runs both algorithms and prints JSON to stdout
4. Python parses the JSON and renders the full dashboard

---

## 🚀 Getting Started

### Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| g++ | C++17+ | `sudo apt install g++` · [MinGW for Windows](https://www.mingw-w64.org/) |
| Python | 3.8+ | [python.org](https://www.python.org/downloads/) |
| pip | Latest | Comes with Python |

---

### ⚡ Option 1 — One-Click Setup (Easiest)

**Windows:**
```bat
setup.bat
```

**Linux / macOS:**
```bash
chmod +x setup.sh && ./setup.sh
```

This automatically compiles the C++ backend and installs all Python dependencies.

---

### 🔧 Option 2 — Manual Setup

**Step 1 — Compile the C++ backend**

```bash
# Linux / macOS
cd backend
g++ -std=c++17 -O2 -o loan_optimizer main.cpp greedy.cpp dp.cpp utils.cpp

# Windows (Command Prompt)
cd backend
g++ -std=c++17 -O2 -o loan_optimizer.exe main.cpp greedy.cpp dp.cpp utils.cpp
```

**Step 2 — Install Python dependencies**

```bash
pip install -r requirements.txt
```

**Step 3 — Launch the dashboard**

```bash
cd frontend
streamlit run streamlit_app.py
```

**Step 4 — Open in browser**

The app opens automatically at:
```
http://localhost:8501
```

---

## 📊 Using the Dashboard

| Step | Action |
|------|--------|
| 1 | Upload a CSV from the `data/` folder (start with `data5.csv`) |
| 2 | Set your **Total Bank Budget** in the left sidebar |
| 3 | Click **▶ Run Optimization** |
| 4 | View Portfolio Summary, KPI Cards, and Algorithm Comparison |
| 5 | Scroll down for Loan Distribution charts and Technical Analysis |
| 6 | Click **Show / Hide Technical Details** to compare Greedy vs DP |

---

## 📄 CSV Input Format

```csv
id,loan_amount,interest_rate,credit_score
1,50000,7.50,720
2,30000,9.00,680
3,80000,6.25,750
```

| Column | Type | Description | Valid Range |
|--------|------|-------------|-------------|
| `id` | int | Unique applicant ID | > 0, no duplicates |
| `loan_amount` | float | Loan requested (₹) | > 0 |
| `interest_rate` | float | Annual rate e.g. 7.5 = 7.5% | > 0 |
| `credit_score` | int | CIBIL score | 300 – 850 |

---

## 🧠 Algorithm Deep Dive

### Greedy Algorithm — O(n log n)
```
Sort applicants by interest_rate (descending)
For each applicant:
    if loan_amount ≤ remaining_budget:
        Approve → deduct from budget
```
**Why it can fail:** Makes the best local choice at every step but may miss globally better combinations.

---

### Dynamic Programming — O(n × W)
```
dp[i][w] = max profit using first i applicants with capacity w

For each applicant i:
    For each capacity w:
        dp[i][w] = max(
            dp[i-1][w],                      ← skip applicant
            dp[i-1][w - loan_amount] + profit ← approve applicant
        )

Backtrack from dp[N][W] to find selected applicants
```
**Guarantee:** Always finds the mathematically optimal solution.

> Loan amounts are scaled ÷ 1000 internally to keep the DP table manageable.

---

## 📦 Sample C++ JSON Output

```json
{
  "status": "ok",
  "budget": 300000.00,
  "total_applicants": 7,
  "Greedy": {
    "total_profit": 32095.00,
    "total_loan_used": 271000.00,
    "selected_count": 6,
    "selected_applicants": [...]
  },
  "DP": {
    "total_profit": 33195.00,
    "total_loan_used": 281000.00,
    "selected_count": 5,
    "selected_applicants": [...]
  }
}
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---------|-----|
| 🔴 `Engine Not Found` in sidebar | Compile the backend first — see Step 1 above |
| `g++ not found` | Install [MinGW](https://www.mingw-w64.org/) (Windows) or `sudo apt install g++` (Linux) |
| `ModuleNotFoundError: streamlit` | Run `pip install -r requirements.txt` |
| `DP table too large` error | Reduce budget or increase `SCALE_UNIT` in `backend/dp.cpp` |
| CSV parse error | Check column names match exactly: `id, loan_amount, interest_rate, credit_score` |
| Blank page on launch | Wait 5–10 seconds — Streamlit loads slowly on first run |

---

## 📚 Concepts Covered

- ✅ Greedy Algorithm — design, analysis, and limitations
- ✅ Dynamic Programming — 0/1 Knapsack with full backtracking
- ✅ Time & space complexity comparison
- ✅ C++ ↔ Python integration via subprocess + JSON
- ✅ Real-world problem modelling (finance / resource allocation)
- ✅ Multi-language system architecture

---

## 🤝 Contributing

Contributions are welcome from fellow students!

- 🐛 Found a bug? Open an **Issue**
- 💡 Want to add Branch & Bound? Submit a **Pull Request**
- ⭐ Found this useful? Give it a **star** — it helps others find it!

---

## 📃 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.
Free to use, modify, and share with credit.

---

<div align="center">

## 👤 Author

**Vaibhav Khandelwal**

B.Tech Computer Science Engineering
Jaypee Institute of Information Technology, Noida

*Design and Analysis of Algorithms — Academic Project*

<br>

[![GitHub](https://img.shields.io/badge/GitHub-Vaibhav--code15-181717?style=for-the-badge&logo=github)](https://github.com/Vaibhav-code15)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Vaibhav%20Khandelwal-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/vaibhav-khandelwal)

<br>

⭐ **If this project helped you, please give it a star — it helps other CS students find it!** ⭐

</div>
