#!/bin/sh

# Grant permission
chmod +x run_program.sh

# Execute lexical anlyzer
#echo "~~~ Running Lexical Analyzer... ~~~\n"
#python3 main.py
#echo "\n=====================================================================================================\n"

# Execute syntax analyzer
#echo "~~~ Running Syntax Analyzer... ~~~\n"
#python3 semantic_analyzer.py
#echo "\n=====================================================================================================\n"

# Execute test cases
echo "~~~ Running Test Cases... ~~~\n"
python3 test.py
