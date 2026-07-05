#pragma once

#include "utils.h"
#include <vector>

/**
 * Greedy Loan Selection Algorithm
 * ─────────────────────────────────
 * Strategy: Sort applicants by profit-to-loan ratio (== interest rate / 100)
 * in descending order, then greedily pick each applicant whose loan amount
 * fits within the remaining budget.
 *
 * Time Complexity : O(n log n)  – dominated by sorting
 * Space Complexity: O(n)
 *
 * NOTE: This is a heuristic and may not always yield the globally optimal
 *       profit.  The DP algorithm provides the true optimum.
 */
OptimizationResult runGreedy(const std::vector<Applicant>& applicants,
                             double budget);
