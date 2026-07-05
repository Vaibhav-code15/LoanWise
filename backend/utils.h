#pragma once

#include <string>
#include <vector>
#include <iostream>

// ─────────────────────────────────────────────
//  Applicant data model
// ─────────────────────────────────────────────
struct Applicant {
    int    id;
    double loanAmount;   // requested loan in dollars
    double interestRate; // annual rate, e.g. 5.50 means 5.50 %
    int    creditScore;  // FICO-style score 300–850

    // Profit = simple annual interest earned by the bank
    double profit() const {
        return loanAmount * interestRate / 100.0;
    }

    // Ratio used by the greedy algorithm
    double profitRatio() const {
        return profit() / loanAmount; // == interestRate / 100
    }
};

// ─────────────────────────────────────────────
//  Result returned by each algorithm
// ─────────────────────────────────────────────
struct OptimizationResult {
    std::string          algorithm;
    std::vector<int>     selectedIds;   // applicant IDs chosen
    double               totalProfit;
    double               totalLoanUsed;
};

// ─────────────────────────────────────────────
//  Utility function declarations
// ─────────────────────────────────────────────

/**
 * Load applicants from a CSV file.
 * Expected header: id,loan_amount,interest_rate,credit_score
 */
std::vector<Applicant> loadApplicants(const std::string& filename);

/**
 * Serialise a single result to a JSON-compatible string block.
 * Used by main.cpp to build the final JSON output.
 */
std::string resultToJson(const OptimizationResult& res,
                         const std::vector<Applicant>& applicants);

/**
 * Print a human-readable summary to stdout (debugging helper).
 */
void printResult(const OptimizationResult& res,
                 const std::vector<Applicant>& applicants);
