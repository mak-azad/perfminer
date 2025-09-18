#!/bin/bash
echo "Spliting task to all nodes..."
python3 task_parallelizer.py repository_lists/github_repositories_Python_04222024.csv ubuntu
echo "Now running the analyzer script.."
parallel-ssh -i -h sshhosts -t 0 'source miniforge3/bin/activate mytoolenv && nohup python3 miner_github/analyzer/repo_analyzer.py'
parallel-ssh -i -h sshhosts 'source miniforge3/bin/activate mytoolenv && nohup python3 miner_github/analyzer/repo_analyzer.py'
