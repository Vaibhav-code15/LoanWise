@echo off
echo ============================================
echo   Smart Bank Loan Optimizer - Setup
echo   github.com/VaibhavKhandelwal/smart-bank-loan-optimizer
echo ============================================
echo.

:: ── Step 1: Check g++ ────────────────────────
echo [1/3] Checking for g++ compiler...
g++ --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: g++ not found!
    echo  Please install MinGW-w64 from https://www.mingw-w64.org/
    echo  and add it to your PATH, then run this script again.
    echo.
    pause
    exit /b 1
)
echo  g++ found!

:: ── Step 2: Compile C++ backend ──────────────
echo.
echo [2/3] Compiling C++ backend...
cd backend
g++ -std=c++17 -O2 -o loan_optimizer.exe main.cpp greedy.cpp dp.cpp utils.cpp
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: Compilation failed! Check the error messages above.
    cd ..
    pause
    exit /b 1
)
cd ..
echo  Compiled successfully! (backend/loan_optimizer.exe)

:: ── Step 3: Install Python deps ──────────────
echo.
echo [3/3] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo  ERROR: pip install failed. Make sure Python and pip are installed.
    pause
    exit /b 1
)
echo  Dependencies installed!

:: ── Done ─────────────────────────────────────
echo.
echo ============================================
echo   Setup complete!
echo ============================================
echo.
echo   To run the app:
echo     cd frontend
echo     streamlit run streamlit_app.py
echo.
echo   Then open http://localhost:8501 in your browser.
echo.
pause
