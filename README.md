# PerfMiner - Instructions to setup the mining tool

## 🚀 Quick Start Guide

### Prerequisites
- CloudLab cluster with NFS setup
- SSH key authentication configured
- `sshhosts` file with client node IPs

### Step 1: Cluster Setup
Follow the detailed instructions from `/cloudlab_setup/README.md` to:
- Set up master/client node architecture
- Configure NFS shared storage
- Install dependencies across all nodes

### Step 2: Prepare Mining Environment

Once your cluster is tested and ready, follow these steps:

#### 2.1 Configure Target Language
Set the programming language for mining across all nodes:

```bash
# Set language for all nodes (python, cpp, java, etc.)
./set_mining_language.sh python

# Verify configuration
./check_mining_language.sh

# Alternative: Set via environment variable
parallel-ssh -h sshhosts -i 'echo "export PERFMINER_LANGUAGE=python" >> ~/.bashrc'
```

#### 2.2 Deploy ML Model
Extract PerfAnnotator-mini model to all worker nodes:

```bash
# Extract perfannotator model from NFS to all nodes
./extract_perfannotator_to_nodes.sh

# Verify model extraction (optional)
parallel-ssh -h sshhosts -i 'ls -la /users/akazad/fine_tuned_graphcodebert_best_170K/'
```

The script will:
- Extract `/nfs/perfannotator-mini.tgz` to `/users/akazad/fine_tuned_graphcodebert_best_170K/` on all nodes
- Verify NFS access and successful extraction
- Report progress for all 95+ nodes

#### 2.3 Distribute Repository Lists
Split the repository CSV file among all client nodes:

```bash
# Split repository list across nodes (update path to your target CSV)
python utils/task_parallelizer.py repository_lists/filtered_repositories_python.csv ubuntu
```

#### 2.4 Verify Task Distribution
Ensure CSV files are properly distributed:

```bash
# Check CSV files exist on all nodes
parallel-ssh -h sshhosts -i 'ls perfminer/analyzer/*.csv'

# Verify task counts
parallel-ssh -h sshhosts -i 'cat perfminer/analyzer/*.csv | wc -l'
```

### Step 3: Start Mining

#### 3.1 Schedule Mining Jobs
Deploy cron jobs to all nodes:

```bash
parallel-ssh -h ~/perfminer/sshhosts -p 20 -t 0 -x "-o StrictHostKeyChecking=no" -i \
  'chmod +x /users/akazad/perfminer/cronjob/run_miner.sh /users/akazad/perfminer/cronjob/cron_install.sh; \
   /users/akazad/perfminer/cronjob/cron_install.sh; \
   crontab -l | tail -n +1'
```

#### 3.2 Monitor Mining Progress
Keep mining processes healthy:

```bash
# Monitor and auto-restart stalled processes
python monitor_logs.py

# Check mining process status
parallel-ssh -h sshhosts 'ps aux | grep repo_analyzer.py'

# View recent log activity
parallel-ssh -h sshhosts -i 'cd perfminer/analyzer/logs/ && tail $(ls -t | head -1)'
```

### Step 4: Collect Results

Results are automatically stored in `/nfs/results_<language>/` as JSONL files. Each node writes:
- `<language>_<hostname>.jsonl` - Mining results
- State tracking CSV files with progress status

## 📁 Project Structure

- `analyzer/repo_analyzer.py` - Main mining engine
- `utils/task_parallelizer.py` - Work distribution
- `cronjob/` - Cron job management and execution
- `cloudlab_setup/` - Cluster setup scripts
- `repository_lists/` - Repository CSV files for mining
- `monitor_logs.py` - Process health monitoring

## 🛠 Troubleshooting

### Common Commands
```bash
# Check node connectivity
bash check_node_status.sh

# Verify NFS mounts
parallel-ssh -h sshhosts "mountpoint -q /nfs && echo OK || echo FAILED"

# Check cron jobs
parallel-ssh -h sshhosts 'crontab -l'

# Monitor log timestamps
parallel-ssh -h sshhosts "cd ~/perfminer/analyzer/logs && ls -lt | head -5"
```

### Process Management
```bash
# Stop mining on all nodes
parallel-ssh -h sshhosts 'pkill -f repo_analyzer.py'

# Remove cron jobs
parallel-ssh -h sshhosts 'bash perfminer/cronjob/remove_cron_job.sh'

# Clean up extracted models (if needed)
./cleanup_perfannotator_from_nodes.sh
```

## 📊 Architecture

PerfMiner uses a distributed cluster architecture:
- **Master Node**: Coordinates setup, splits work, monitors progress
- **Client Nodes**: Execute mining tasks in parallel via cron jobs
- **NFS Storage**: Shared storage for results aggregation
- **ML Pipeline**: GraphCodeBERT model for performance commit classification

For detailed architecture information, see `.github/copilot-instructions.md`. 




