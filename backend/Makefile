# ─────────────────────────────────────────────
#  Smart Bank Loan Optimizer – C++ Backend Makefile
# ─────────────────────────────────────────────

CXX      := g++
CXXFLAGS := -std=c++17 -O2 -Wall -Wextra -pedantic
TARGET   := loan_optimizer
SRCS     := main.cpp greedy.cpp dp.cpp utils.cpp
OBJS     := $(SRCS:.cpp=.o)

# Default target: build the executable
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^
	@echo "Build successful → ./$(TARGET)"

# Compile each .cpp to a .o
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Remove build artefacts
clean:
	rm -f $(OBJS) $(TARGET)

# Quick smoke-test using the sample data file
test: $(TARGET)
	@echo "--- Running greedy ---"
	./$(TARGET) ../data/data.csv 200000 greedy
	@echo ""
	@echo "--- Running dp ---"
	./$(TARGET) ../data/data.csv 200000 dp
	@echo ""
	@echo "--- Running both ---"
	./$(TARGET) ../data/data.csv 200000 both

.PHONY: all clean test
