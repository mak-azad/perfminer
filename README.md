## Running the tool 
- Use `extract_ip_cloudlab.py` script to get the ip list of nodes from `Manifest.xml` file for the cluster at cloudlab, paste them in `sshhosts` and `sshhosts_hostname` files 
- `bash check.sh` (checking if nodes setup correctly)
- `parallel-ssh -i -h sshhosts 'curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"'` (setting up conda)
- `parallel-ssh -i -h sshhosts  -t 0  'bash Miniforge3-Linux-x86_64.sh -b '` (setting up conda)
- `bash freeze_ubuntu.sh` (for oracle cloud nodes)
- `bash master.sh` (setup master node)
- `parallel-ssh -i -h sshhosts -x "-oStrictHostKeyChecking=no" -P -t 0 'nohup bash /users/akazad/miner_github/install_n_run.sh'`  (setup all nodes for mining tool)
- `python3 task_parallelizer.py repository_lists/filtered_repositories_c.csv ubuntu`  (split task to all node)
- `parallel-ssh -i -h sshhosts 'chmod +x miner_github/cronjob/add_cron_job.sh'`   
- `parallel-ssh -i -h sshhosts 'bash miner_github/cronjob/add_cron_job.sh'` (start mining)
- Run `monitor_logs.py` to restart a node in case the script hangs 
- `parallel-ssh -i -h sshhosts 'ps aux | grep 'miner_github/analyzer/test_repo_analyzer.py' | grep -v grep'`  (check mining process, start in 5 min)

### Setup language config
```bash
# Set language once for all nodes
./set_mining_language.sh python

# Verify configuration
./check_mining_language.sh

# Set environment variable on all nodes
parallel-ssh -h sshhosts -i 'echo "export PERFMINER_LANGUAGE=python" >> ~/.bashrc'
```




## Cluster setup guide (NFS Server + Client Setup Guide) 

This guide documents how to configure an NFS server and mount it on multiple clients in a cluster.  
It is based on a working setup tested on CloudLab nodes (Ubuntu/Debian style).

---

## 1. Server Setup

### 1.1 Install required packages
```bash
sudo apt-get update
sudo apt-get install -y nfs-kernel-server
```

### 1.2 Prepare the export directory
Identify your data disk (example: `/dev/sdd`):
```bash
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT
```

If not mounted, mount it at `/nfs`:
```bash
sudo mkdir -p /nfs
sudo mount /dev/sdd /nfs
ls -lh /nfs    # confirm files are visible
```

Make the disk mount persistent across reboots:
```bash
echo "/dev/sdd  /nfs  ext4  defaults  0  2" | sudo tee -a /etc/fstab
```

### 1.3 Configure exports
Edit `/etc/exports` and save:
```bash
echo "/nfs *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee /etc/exports
```

👉 Later, restrict it to your subnets, e.g.:
```
/nfs 155.98.36.0/24(rw,sync,no_subtree_check,no_root_squash) 155.98.38.0/24(rw,sync,no_subtree_check,no_root_squash)
```

### 1.4 Start services
# SERVER ONLY
```sudo systemctl restart rpcbind```

# Precheck to avoid exportfs hang due to self-mount:
```
mount | awk '$3=="/nfs"{print $5}' | grep -q '^nfs' \
  && { echo "ERROR: /nfs is NFS-mounted on server; fix with: sudo umount -lf /nfs && sudo mount /dev/sdX /nfs"; exit 1; }

sudo systemctl restart nfs-server
sudo exportfs -ravvv
showmount -e localhost   # should list /nfs instantly
```
You should see `/nfs` listed.

---
## Run these ONLY on the SERVER to ensure it won't self-mount.

### A) Ensure the server has NO client-style /etc/fstab entry:
```
grep -nE '(:/nfs[[:space:]]+/nfs[[:space:]]+nfs)' /etc/fstab \
  && { echo "ERROR: Remove client NFS line for /nfs from /etc/fstab on the SERVER!"; exit 1; } \
  || echo "OK: no NFS /nfs line in server's /etc/fstab."
```
### B) Ensure /nfs on the SERVER is NOT NFS-mounted:
```
mount | awk '$3=="/nfs"{print $5}' | grep -q '^nfs' \
  && { echo "ERROR: /nfs is NFS-mounted on the SERVER (self-mount loop). Unmount with: sudo umount -lf /nfs"; exit 1; } \
  || echo "OK: /nfs on server is not NFS (good)."
```
### C) (If you use parallel-ssh) Make sure the SERVER is not in sshhosts:
```
SERVER_IP=155.98.38.80
grep -E "(^|[[:space:]])${SERVER_IP}([[:space:]]|$)" sshhosts \
  && { echo "ERROR: Remove ${SERVER_IP} (the server) from sshhosts!"; exit 1; } \
  || echo "OK: server not listed in sshhosts."
```
## 2. Client Setup

# CLIENTS ONLY
sudo mkdir -p /nfs
sudo mount -t nfs -o vers=3,nolock SERVER_IP:/nfs /nfs


### 2.1 Install NFS client packages
```bash
sudo apt-get update
sudo apt-get install -y nfs-common
```

### 2.2 Create mountpoint
```bash
sudo mkdir -p /nfs
```

### 2.3 Mount the export
Replace `SERVER_IP` with your server’s IP (example: `155.98.36.136`):
```bash
sudo mount -t nfs -o vers=3,nolock SERVER_IP:/nfs /nfs
```

Check:
```bash
ls -lh /nfs
```

You should see shared files (e.g., `perfannotator-mini.tgz`).

### 2.4 Make the mount persistent
Add to `/etc/fstab`:
```
SERVER_IP:/nfs /nfs nfs vers=3,nolock,_netdev,defaults 0 0
```

Then:
```bash
sudo mount -a
```

---



## 3. Multi-Node Setup (with `parallel-ssh`)

Create a file `sshhosts` containing all client hostnames/IPs (exclude the server).
### Which clients mounted it?
```
parallel-ssh -h sshhosts -i "mount | grep '${SERVER_IP}:/nfs' || echo 'NOT_MOUNTED'"
```

### 0) Make sure the server is NOT in the host list
```
grep -E '(^| )155\.98\.38\.80( |$)' sshhosts && echo "Remove server from sshhosts!" || echo "OK: server not in sshhosts"
```
### 1) Set server IP for local expansion
```
SERVER_IP=155.98.38.80
```
### 2) Fan-out mount to clients (longer timeout & gentle listing)
```parallel-ssh -t 600 -h sshhosts -i \
  "sudo mkdir -p /nfs && \
   (mountpoint -q /nfs || sudo mount -t nfs -o vers=3,nolock ${SERVER_IP}:/nfs /nfs) && \
   ls -lh /nfs | head || echo 'MOUNT_FAILED'"
```
---

## 4. Health Checks

### if suspect a loop on the server
```
# On the SERVER
mount | grep " /nfs "      # should show ONLY: /dev/sdX on /nfs type ext4
sudo exportfs -v           # should list /nfs and your client CIDRs
showmount -e localhost     # must return immediately with /nfs
```
### quick fix for loop
```
sudo umount -lf /nfs
sudo mount /dev/sdX /nfs
sudo systemctl restart rpcbind nfs-server
sudo exportfs -ravvv
```

### quick fix on clients where it failed to mount due to version
```
SERVER_IP=<PUT_SERVER_IP_HERE>
sudo mkdir -p /nfs
sudo mount -t nfs -o vers=4.1,proto=tcp ${SERVER_IP}:/nfs /nfs
ls -lh /nfs | head
```



### Can they see a known file (if present)?
parallel-ssh -h sshhosts -i "test -e /nfs/perfannotator-mini.tgz && echo OK || echo MISSING"
---
