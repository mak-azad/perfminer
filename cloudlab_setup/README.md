# ☁️ CloudLab Cluster Setup Guide for PerfMiner

This guide documents the **end-to-end process** for preparing a CloudLab cluster with one **server node** and multiple **client nodes** to run the **PerfMiner** framework.

---

## 🚀 Step 1. Login to the Server Node

1. SSH into your **server node**:
   ```bash
   ssh <server-node-address>
   ```

2. Generate an SSH key pair on the **server node**:
   ```bash
   ssh-keygen -t rsa -b 4096 -C "n43@gmail.com"
   cat ~/.ssh/id_rsa.pub
   ```

3. Copy the **public key** and **add it to your CloudLab portal** (under “SSH Keys”).

4. Once added, verify **server-client communication** later using `parallel-ssh`.

---

## 🧰 Step 2. Clone Repository and Run Server Setup

1. Clone the PerfMiner repository:
   ```bash
   git clone https://github.com/mak-azad/perfminer.git
   cd perfminer
   ```

2. Run the **server setup script**:
   ```bash
   bash setup_master.sh
   ```

---

## 🗂️ Step 3. Generate Node IP List

1. Run the helper script to extract IPs from your CloudLab Manifest file:
   ```bash
   python extract_ip_cloudlab.py
   ```

   > ⚙️ Tip: Comment/uncomment the relevant `{ip_address}` or `{hostname}` lines in the script depending on your manifest format.

2. Update the following files (excluding the server IP):
   - `sshhosts` → list of **client IPs**
   - `sshhosts_hostname` → list of **client hostnames**

---

## 🔗 Step 4. Verify Server–Client Communication

Run a quick check:
```bash
bash check_node_status.sh
```

If all hostnames return successfully, proceed. If it fails with permission denied, restart all nodes on the portal.
Next, next follow nfs setup section below to make sure storage available before proceeding.

---

## 🧬 Step 5. Clone Repo to All Clients

Distribute PerfMiner to all client nodes:
```bash
parallel-ssh -i -h sshhosts 'git clone https://github.com/mak-azad/perfminer.git'
```

Verify:
```bash
parallel-ssh -i -h sshhosts 'ls'
```

---

## ⚙️ Step 6. Install Python on Clients (Batch 20)

Install Python 3.10 and dependencies in parallel (batch of 20 clients):
```bash
parallel-ssh -i -h sshhosts -p 20 -t 0   'sleep $((RANDOM % 30));    sudo apt-get update &&    sudo apt-get install -y software-properties-common lsb-release ca-certificates apt-transport-https curl &&    sudo add-apt-repository -y ppa:deadsnakes/ppa &&    sudo apt-get update &&    sudo apt-get install -y python3.10'
```

Sanity check:
```bash
parallel-ssh -i -h sshhosts 'python3.10 --version'
```

---

## 📦 Step 7. Prepare Offline Packages

On the **server node**, download all required Python wheels:
```bash
mkdir -p ~/wheelhouse
pip download -r ~/perfminer/requirements.txt --dest ~/wheelhouse --only-binary=:all:
```

Create directories and copy wheels to all clients:
```bash
parallel-ssh -h ~/perfminer/sshhosts -p 20 -t 0 -x "-o StrictHostKeyChecking=no" -i 'mkdir -p /users/akazad/wheelhouse'
parallel-scp -h ~/perfminer/sshhosts -p 20 -x "-o StrictHostKeyChecking=no" ~/wheelhouse/* /users/akazad/wheelhouse/
```

Sanity check:
```bash
parallel-ssh -h ~/perfminer/sshhosts -p 10 -x "-o StrictHostKeyChecking=no" -i 'ls -1 /users/akazad/wheelhouse | wc -l'
```

---

## 🧪 Step 8. Install Virtual Environment on Clients

Create and prepare the virtual environment:
```bash
parallel-ssh -h ~/perfminer/sshhosts -p 10 -t 0 -x "-o StrictHostKeyChecking=no" -i   'export PATH="$HOME/.local/bin:$PATH" PIP_DEFAULT_TIMEOUT=180;    chmod +x ~/perfminer/install_venv.sh && ~/perfminer/install_venv.sh'
```

---

## 📚 Step 9. Install Python Requirements Inside venv

Install all dependencies inside the created virtual environment:
```bash
parallel-ssh -h ~/perfminer/sshhosts -p 20 -t 0 -x "-o StrictHostKeyChecking=no" -i   'export PATH="$HOME/.local/bin:$PATH";    if [ ! -x "$HOME/venvs/mytoolenv/bin/python" ]; then ~/perfminer/install_venv.sh; fi;    "$HOME/venvs/mytoolenv/bin/pip" install --no-index --find-links "$HOME/wheelhouse" -r "$HOME/perfminer/requirements.txt"'
```

---

## 🧠 Step 10. Test Model Inference

Finally, verify model inference works on all clients:
```bash
parallel-ssh -h ~/perfminer/sshhosts -p 20 -t 0 -x "-o StrictHostKeyChecking=no" -i   'if [ ! -x "$HOME/venvs/mytoolenv/bin/python" ]; then ~/perfminer/install_venv.sh; fi;    "$HOME/venvs/mytoolenv/bin/python" -u "$HOME/perfminer/test/test_model.py"'
```

---

## ✅ Summary

After completing all steps, your CloudLab cluster should have:

- ✅ SSH connectivity between server ↔ clients  
- ✅ Python 3.10 installed  
- ✅ Isolated virtual environments  
- ✅ All dependencies preloaded (offline)  
- ✅ Working model inference  


# Cluster setup guide (NFS Server + Client Setup Guide) 

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
