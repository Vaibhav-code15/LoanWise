#!/bin/bash

echo "============================================"
echo "  Smart Bank Loan Optimizer - Setup"
echo "  github.com/VaibhavKhandelwal/smart-bank-loan-optimizer"
echo "============================================"
echo ""

# ── Step 1: Check g++ ────────────────────────
echo "[1/3] Checking for g++ compiler..."
if ! command -v g++ &> /dev/null; then
    echo ""
    echo " ERROR: g++ not found!"
    echo " Install it with:"
    echo "   Ubuntu/Debian : sudo apt install g++"
    echo "   macOS         : xcode-select --install"
    echo ""
    exit 1
fi
echo " g++ found: $(g++ --version | head -1)"

# ── Step 2: Compile C++ backend ──────────────
echo ""
echo "[2/3] Compiling C++ backend..."
cd backend
g++ -std=c++17 -O2 -o loan_optimizer main.cpp greedy.cpp dp.cpp utils.cpp
if [ $? -ne 0 ]; then
    echo ""
    echo " ERROR: Compilation failed! Check the error messages above."
    cd ..
    exit 1
fi
cd ..
echo " Compiled successfully! (backend/loan_optimizer)"

# ── Step 3: Install Python deps ──────────────
echo ""
echo "[3/3] Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo ""
    echo " ERROR: pip install failed."
    echo " Try: pip3 install -r requirements.txt"
    exit 1
fi
echo " Dependencies installed!"

# ── Done ─────────────────────────────────────
echo ""
echo "============================================"
echo "  Setup complete!"
echo "============================================"
echo ""
echo "  To run the app:"
echo "    cd frontend"
echo "    streamlit run streamlit_app.py"
echo ""
echo "  Then open http://localhost:8501 in your browser."
echo ""
