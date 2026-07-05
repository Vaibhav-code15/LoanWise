/**
 * Smart Bank Loan Optimization System – C++ Backend
 * ═══════════════════════════════════════════════════
 *
 * Usage:
 *   ./loan_optimizer <data_file> <budget> <algorithm>
 *
 *   algorithm: "greedy" | "dp" | "both"
 *
 * Output:
 *   A single JSON object printed to stdout, e.g.:
 *   {
 *     "status": "ok",
 *     "budget": 200000.00,
 *     "greedy": { ... },
 *     "dp":     { ... }
 *   }
 *
 *   On error, outputs:
 *   { "status": "error", "message": "..." }
 */

#include "utils.h"
#include "greedy.h"
#include "dp.h"

#include <iostream>
#include <string>
#include <stdexcept>
#include <iomanip>
#include <sstream>
#include <algorithm>

// ─────────────────────────────────────────────
//  helpers
// ─────────────────────────────────────────────

static std::string toLower(std::string s) {
    std::transform(s.begin(), s.end(), s.begin(), ::tolower);
    return s;
}

// Escape a string for safe JSON embedding
static std::string jsonEscape(const std::string& s) {
    std::string out;
    for (char c : s) {
        if (c == '"')  out += "\\\"";
        else if (c == '\\') out += "\\\\";
        else if (c == '\n') out += "\\n";
        else                out += c;
    }
    return out;
}

static void printError(const std::string& msg) {
    std::cout << "{\n"
              << "  \"status\": \"error\",\n"
              << "  \"message\": \"" << jsonEscape(msg) << "\"\n"
              << "}\n";
}

// ─────────────────────────────────────────────
//  main
// ─────────────────────────────────────────────
int main(int argc, char* argv[]) {

    // ── Argument validation ───────────────────
    if (argc != 4) {
        printError("Usage: loan_optimizer <data_file> <budget> <algorithm: greedy|dp|both>");
        return 1;
    }

    std::string dataFile  = argv[1];
    double      budget    = 0.0;
    std::string algorithm = toLower(argv[3]);

    try {
        budget = std::stod(argv[2]);
    } catch (...) {
        printError("Invalid budget value: " + std::string(argv[2]));
        return 1;
    }

    if (budget <= 0) {
        printError("Budget must be a positive number.");
        return 1;
    }

    if (algorithm != "greedy" && algorithm != "dp" && algorithm != "both") {
        printError("Algorithm must be one of: greedy, dp, both");
        return 1;
    }

    // ── Load data ─────────────────────────────
    std::vector<Applicant> applicants;
    try {
        applicants = loadApplicants(dataFile);
    } catch (const std::exception& e) {
        printError(e.what());
        return 1;
    }

    // ── Run selected algorithm(s) ─────────────
    OptimizationResult greedyResult, dpResult;
    bool ranGreedy = false, ranDP = false;

    try {
        if (algorithm == "greedy" || algorithm == "both") {
            greedyResult = runGreedy(applicants, budget);
            ranGreedy = true;
        }
        if (algorithm == "dp" || algorithm == "both") {
            dpResult = runDP(applicants, budget);
            ranDP = true;
        }
    } catch (const std::exception& e) {
        printError(e.what());
        return 1;
    }

    // ── Build JSON output ─────────────────────
    std::ostringstream json;
    json << std::fixed << std::setprecision(2);
    json << "{\n";
    json << "  \"status\": \"ok\",\n";
    json << "  \"budget\": " << budget << ",\n";
    json << "  \"total_applicants\": " << applicants.size() << ",\n";

    bool firstAlgo = true;

    if (ranGreedy) {
        if (!firstAlgo) json << ",\n";
        json << resultToJson(greedyResult, applicants);
        firstAlgo = false;
    }

    if (ranDP) {
        if (!firstAlgo) json << ",\n";
        json << resultToJson(dpResult, applicants);
        firstAlgo = false;
    }

    json << "\n}\n";

    std::cout << json.str();
    return 0;
}
