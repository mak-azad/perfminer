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
   bash master.sh
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

If all hostnames return successfully, proceed.

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
