#include "utils.h"

#include <fstream>
#include <sstream>
#include <stdexcept>
#include <iomanip>
#include <algorithm>
#include <cctype>

// ─────────────────────────────────────────────
//  loadApplicants
// ─────────────────────────────────────────────
std::vector<Applicant> loadApplicants(const std::string& filename) {
    std::vector<Applicant> applicants;

    auto trim = [](std::string s) -> std::string {
        auto notSpace = [](unsigned char ch) { return !std::isspace(ch); };
        s.erase(s.begin(), std::find_if(s.begin(), s.end(), notSpace));
        s.erase(std::find_if(s.rbegin(), s.rend(), notSpace).base(), s.end());
        return s;
    };

    std::ifstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("ERROR: Cannot open input file: " + filename);
    }

    std::string line;

    // Skip header row
    if (!std::getline(file, line)) {
        throw std::runtime_error("ERROR: Input file is empty.");
    }

    int lineNo = 1;
    while (std::getline(file, line)) {
        ++lineNo;
        if (line.empty()) continue;

        // Strip Windows-style \r
        if (!line.empty() && line.back() == '\r') line.pop_back();

        std::istringstream ss(line);
        std::string token;
        Applicant a;

        try {
            std::getline(ss, token, ','); a.id           = std::stoi(trim(token));
            std::getline(ss, token, ','); a.loanAmount   = std::stod(trim(token));
            std::getline(ss, token, ','); a.interestRate = std::stod(trim(token));
            std::getline(ss, token, ','); a.creditScore  = std::stoi(trim(token));
        } catch (const std::exception& e) {
            throw std::runtime_error("ERROR: Malformed CSV at line "
                                     + std::to_string(lineNo) + ": " + e.what());
        }

        // Basic validation
        if (a.id <= 0)
            throw std::runtime_error("ERROR: id must be > 0 at line "
                                     + std::to_string(lineNo));
        if (a.loanAmount <= 0)
            throw std::runtime_error("ERROR: loanAmount must be > 0 at line "
                                     + std::to_string(lineNo));
        if (a.interestRate <= 0)
            throw std::runtime_error("ERROR: interestRate must be > 0 at line "
                                     + std::to_string(lineNo));
        if (a.creditScore < 300 || a.creditScore > 850)
            throw std::runtime_error("ERROR: creditScore must be 300–850 at line "
                                     + std::to_string(lineNo));

        applicants.push_back(a);
    }

    if (applicants.empty()) {
        throw std::runtime_error("ERROR: No applicant records found in file.");
    }

    // Enforce unique IDs (improves determinism and prevents confusing results)
    std::vector<int> ids;
    ids.reserve(applicants.size());
    for (const auto& a : applicants) ids.push_back(a.id);
    std::sort(ids.begin(), ids.end());
    auto dupIt = std::adjacent_find(ids.begin(), ids.end());
    if (dupIt != ids.end()) {
        throw std::runtime_error("ERROR: Duplicate applicant id found: " + std::to_string(*dupIt));
    }

    return applicants;
}

// ─────────────────────────────────────────────
//  resultToJson  – produces one JSON object block
// ─────────────────────────────────────────────
std::string resultToJson(const OptimizationResult& res,
                         const std::vector<Applicant>& applicants) {
    // Build a quick lookup: id -> Applicant
    // (IDs are assumed unique)
    std::ostringstream json;
    json << std::fixed << std::setprecision(2);

    json << "    \"" << res.algorithm << "\": {\n";
    json << "      \"total_profit\": " << res.totalProfit << ",\n";
    json << "      \"total_loan_used\": " << res.totalLoanUsed << ",\n";
    json << "      \"selected_count\": " << res.selectedIds.size() << ",\n";
    json << "      \"selected_applicants\": [\n";

    for (std::size_t i = 0; i < res.selectedIds.size(); ++i) {
        int sid = res.selectedIds[i];
        // Find applicant by ID
        const Applicant* ap = nullptr;
        for (const auto& a : applicants) {
            if (a.id == sid) { ap = &a; break; }
        }
        if (!ap) continue;

        json << "        {\n";
        json << "          \"id\": "            << ap->id           << ",\n";
        json << "          \"loan_amount\": "   << ap->loanAmount   << ",\n";
        json << "          \"interest_rate\": " << ap->interestRate << ",\n";
        json << "          \"credit_score\": "  << ap->creditScore  << ",\n";
        json << "          \"profit\": "        << ap->profit()     << "\n";
        json << "        }";
        if (i + 1 < res.selectedIds.size()) json << ",";
        json << "\n";
    }

    json << "      ]\n";
    json << "    }";
    return json.str();
}

// ─────────────────────────────────────────────
//  printResult  – human-readable debug output
// ─────────────────────────────────────────────
void printResult(const OptimizationResult& res,
                 const std::vector<Applicant>& applicants) {
    std::cout << "\n=== " << res.algorithm << " ===\n";
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Total Profit   : $" << res.totalProfit  << "\n";
    std::cout << "Total Loan Used: $" << res.totalLoanUsed << "\n";
    std::cout << "Selected (" << res.selectedIds.size() << " applicants):\n";

    for (int sid : res.selectedIds) {
        for (const auto& a : applicants) {
            if (a.id == sid) {
                std::cout << "  ID=" << a.id
                          << "  Loan=$" << a.loanAmount
                          << "  Rate=" << a.interestRate << "%"
                          << "  Credit=" << a.creditScore
                          << "  Profit=$" << a.profit() << "\n";
            }
        }
    }
}
