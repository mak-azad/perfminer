
#!/bin/bash
echo "Checking connection to all nodes using pssh!"
parallel-ssh -i -h sshhosts -O StrictHostKeyChecking=no hostname
