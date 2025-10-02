# PerfMiner AI Assistant Instructions

## Project Overview
PerfMiner is a distributed mining framework for analyzing performance-related commits in open-source repositories. It uses machine learning to classify commits and extract performance optimization patterns across multiple programming languages (Python, C++, Java, JavaScript, etc.).

## Architecture & Core Components

### Cluster-Based Design
- **Master node**: Coordinates work distribution, runs setup scripts (`setup_master.sh`, `master.sh`)
- **Worker nodes**: Execute mining tasks in parallel using `parallel-ssh` commands
- **NFS storage**: Shared `/nfs` directory for results aggregation
- **SSH hosts management**: `sshhosts` and `sshhosts_hostname` files define cluster topology

### Key Entry Points
- `analyzer/repo_analyzer.py` - Main mining engine that processes GitHub repositories
- `utils/task_parallelizer.py` - Splits CSV repository lists across worker nodes
- `cronjob/run_miner.sh` - Cron-based execution wrapper with PID management
- `monitor_logs.py` - Automatic node restart when mining processes stall

### ML Classification Pipeline
- Uses fine-tuned GraphCodeBERT model at `/users/akazad/fine_tuned_graphcodebert_best_170K`
- Tokenizer max length: 512 tokens, device auto-detection (CUDA/CPU)
- Performance commit classification with probability thresholds
- Results stored as JSONL files with commit metadata, code diffs, and ML predictions

## Development Workflows

### Cluster Setup (CloudLab)
```bash
# Extract IPs from CloudLab manifest
python cloudlab_setup/extract_ip_cloudlab.py

# Setup master node
bash setup_master.sh

# Verify connectivity
bash check_node_status.sh

# Install dependencies across cluster (batch processing with -p 20)
parallel-ssh -h sshhosts -p 20 -t 0 'install commands...'
```

### Mining Execution
```bash
# Split work across nodes
python3 utils/task_parallelizer.py repository_lists/filtered_repositories_python.csv ubuntu

# Start mining with cron jobs
parallel-ssh -h sshhosts 'bash perfminer/cronjob/cron_install.sh'

# Monitor progress
python monitor_logs.py
```

## Project-Specific Patterns

### Data Flow
1. Repository lists in `repository_lists/` (filtered CSV format)
2. Work split by `task_parallelizer.py` → per-node CSV files  
3. Each node processes assigned repos via `repo_analyzer.py`
4. Results written to `/nfs/results_<language>/` as JSONL batches
5. State tracking in CSV files with "done"/"failed"/"pending" status

### Error Handling & Resilience
- **Timeout protection**: SIGALRM handlers for stuck commit processing
- **Duplicate detection**: SHA-based commit deduplication using `seen_hashes` set
- **State persistence**: CSV state files track per-repository progress
- **Auto-restart**: `monitor_logs.py` kills stalled processes based on log timestamps
- **Batch processing**: `-p 20` flag for parallel-ssh to avoid overwhelming nodes

### Virtual Environment Management
- **Standard path**: `~/venvs/mytoolenv` across all nodes
- **Offline installation**: Pre-download wheels to `~/wheelhouse` for air-gapped installs
- **Conda integration**: Miniforge3 setup with environment activation in cron jobs

### File Naming Conventions
- Repository CSVs: `github_repositories_<language>_<date>.csv`
- Split files: `github_repositories_<hostname>.csv`
- Log files: `log_<hostname>_<timestamp>.txt`
- Results: `<language>_<hostname>.jsonl`

## Critical Dependencies
- PyDriller for Git analysis
- Transformers for ML inference  
- parallel-ssh (pssh) for cluster operations
- NFS for shared storage

## Common Debugging Commands
```bash
# Check mining process status
parallel-ssh -h sshhosts 'ps aux | grep repo_analyzer.py'

# Monitor log timestamps
parallel-ssh -h sshhosts "cd ~/perfminer/analyzer/logs && ls -lt | head -5"

# Verify NFS mounts
parallel-ssh -h sshhosts "mountpoint -q /nfs && echo OK || echo FAILED"

# Check cron jobs
parallel-ssh -h sshhosts 'crontab -l'
```

## Integration Points
- **CloudLab**: Manifest XML parsing for node discovery
- **GitHub**: Repository URL processing and commit analysis
- **ML Models**: GraphCodeBERT tokenization and classification
- **Storage**: NFS for distributed result collection
- **Monitoring**: Log-based health checking with automatic recovery

When working with this codebase, prioritize understanding the distributed nature of operations and always consider the cluster-wide impact of changes.