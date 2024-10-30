#!/bin/sh

# Grant permission
chmod +x run_program.sh

# Execute lexical anlyzer
echo "~~~ Running Lexical Analyzer... ~~~\n"
python3 main.py
echo "\n=====================================================================================================\n"

# Execute test cases
echo "~~~ Running Test Cases... ~~~\n"
python3 testcase2.py
