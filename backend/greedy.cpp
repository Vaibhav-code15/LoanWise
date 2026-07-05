#include "greedy.h"
#include <algorithm>
#include <vector>

// ─────────────────────────────────────────────
//  runGreedy
// ─────────────────────────────────────────────
OptimizationResult runGreedy(const std::vector<Applicant>& applicants,
                             double budget) {

    // Step 1: Create an index array sorted by profit ratio (high → low).
    //         Using indices avoids copying Applicant structs.
    std::vector<int> indices(applicants.size());
    for (int i = 0; i < static_cast<int>(applicants.size()); ++i) {
        indices[i] = i;
    }

    std::sort(indices.begin(), indices.end(),
              [&](int a, int b) {
                  // Sort by interest rate descending (profitRatio = rate/100)
                  return applicants[a].profitRatio() > applicants[b].profitRatio();
              });

    // Step 2: Greedily pick applicants while budget allows.
    OptimizationResult result;
    result.algorithm    = "Greedy";
    result.totalProfit  = 0.0;
    result.totalLoanUsed = 0.0;

    double remaining = budget;

    for (int idx : indices) {
        const Applicant& a = applicants[idx];
        if (a.loanAmount <= remaining) {
            result.selectedIds.push_back(a.id);
            result.totalProfit   += a.profit();
            result.totalLoanUsed += a.loanAmount;
            remaining            -= a.loanAmount;
        }
        // If applicant doesn't fit, skip (pure 0-1 greedy)
    }

    return result;
}
