#pragma once

#include "utils.h"
#include <vector>

/**
 * Dynamic Programming – 0/1 Knapsack Loan Selection
 * ────────────────────────────────────────────────────
 * Finds the OPTIMAL subset of applicants maximising total profit
 * subject to the budget constraint.
 *
 * Implementation details
 * ──────────────────────
 * • Loan amounts are scaled to integer "units" (divided by SCALE_UNIT = 1000)
 *   to keep the DP table a manageable size.
 * • Profit values are stored as integers (cents) to avoid floating-point
 *   comparison issues inside the table.
 * • A 1-D rolling array is used to reduce space from O(n·W) to O(W).
 *
 * Time Complexity : O(n · W)  where W = budget / SCALE_UNIT
 * Space Complexity: O(W)
 *
 * @param applicants  Full list of applicants read from file
 * @param budget      Maximum total loan the bank can issue (dollars)
 * @return            OptimizationResult with globally optimal selection
 */
OptimizationResult runDP(const std::vector<Applicant>& applicants,
                         double budget);
