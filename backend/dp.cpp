#include "dp.h"
#include <vector>
#include <algorithm>
#include <cmath>
#include <stdexcept>

// ─────────────────────────────────────────────
//  Constants
// ─────────────────────────────────────────────

// Loan amounts are divided by SCALE_UNIT to convert them to integer weights.
// E.g. a $25,000 loan becomes weight 25 (in thousands).
// This keeps the DP table width = budget / SCALE_UNIT, a manageable number.
static const double SCALE_UNIT = 1000.0;

// Profit values are stored as integer cents to avoid float comparison issues.
// $2,750.50 profit → 275050 cents.
static const double CENTS = 100.0;

// ─────────────────────────────────────────────
//  runDP
// ─────────────────────────────────────────────
OptimizationResult runDP(const std::vector<Applicant>& applicants,
                         double budget) {

    int n = static_cast<int>(applicants.size());

    // Convert budget to integer capacity (in SCALE_UNIT units)
    int W = static_cast<int>(std::floor(budget / SCALE_UNIT));

    if (W <= 0) {
        throw std::runtime_error(
            "ERROR: Budget is too small relative to the scale unit ($1,000). "
            "Please use a budget >= $1,000.");
    }

    // Guard against unreasonably large tables (> 200 MB roughly)
    if (static_cast<long long>(n) * W > 200'000'000LL) {
        throw std::runtime_error(
            "ERROR: Budget / scale combination produces a DP table that is too "
            "large.  Consider increasing SCALE_UNIT or reducing budget.");
    }

    // Build integer weight and profit arrays
    std::vector<int> weight(n); // in SCALE_UNIT units
    std::vector<long long> profit(n); // in cents

    for (int i = 0; i < n; ++i) {
        // Round down loan amount to nearest SCALE_UNIT
        weight[i] = static_cast<int>(std::floor(applicants[i].loanAmount / SCALE_UNIT));
        // Store profit in cents
        profit[i] = static_cast<long long>(
            std::round(applicants[i].profit() * CENTS));

        if (weight[i] <= 0) {
            // Loan amount smaller than SCALE_UNIT: treat as weight 1
            weight[i] = 1;
        }
    }

    // ─── 2-D DP table for backtracking ───────────────────────────────────
    // dp[i][w] = maximum profit (cents) using first i applicants with
    //            capacity w (in SCALE_UNIT units).
    // We keep the full table so we can backtrack to find selected items.
    //
    // Memory: n * (W+1) * sizeof(long long)
    // For n=50, W=500 → 50*501*8 ≈ 200 KB   (fine)
    // ─────────────────────────────────────────────────────────────────────
    std::vector<std::vector<long long>> dp(
        n + 1, std::vector<long long>(W + 1, 0LL));

    for (int i = 1; i <= n; ++i) {
        int    wi = weight[i - 1];
        long long pi = profit[i - 1];

        for (int w = 0; w <= W; ++w) {
            // Option A: skip applicant i
            dp[i][w] = dp[i - 1][w];

            // Option B: include applicant i (if it fits)
            if (w >= wi) {
                long long withItem = dp[i - 1][w - wi] + pi;
                if (withItem > dp[i][w]) {
                    dp[i][w] = withItem;
                }
            }
        }
    }

    // ─── Backtrack to find selected applicants ────────────────────────────
    std::vector<bool> selected(n, false);
    int w = W;
    for (int i = n; i >= 1; --i) {
        if (dp[i][w] != dp[i - 1][w]) {
            // Applicant i was included
            selected[i - 1] = true;
            w -= weight[i - 1];
        }
    }

    // ─── Build result ─────────────────────────────────────────────────────
    OptimizationResult result;
    result.algorithm     = "DP";
    result.totalProfit   = 0.0;
    result.totalLoanUsed = 0.0;

    for (int i = 0; i < n; ++i) {
        if (selected[i]) {
            result.selectedIds.push_back(applicants[i].id);
            result.totalProfit   += applicants[i].profit();
            result.totalLoanUsed += applicants[i].loanAmount;
        }
    }

    return result;
}
