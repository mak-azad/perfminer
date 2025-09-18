#!/bin/bash
echo "Now going to setup OCI client..."
pip3 install oci
# Create the .oci directory in the home directory if it doesn't already exist
mkdir -p ~/.oci
sleep 5
echo "Copying OCI credentials...."
cp /home/akazad/miner_github/file.pem .oci/
# OCI configuration details
oci_user_ocid="ocid1.user.oc1..aaaaaaaantmgpywouidjiiw33kdpnlcadmdgsqotqwvwwtzfbna76hmwzwdq"
oci_fingerprint="26:2d:ef:f3:9c:ff:93:42:97:36:05:70:06:a1:72:48"
oci_tenancy_ocid="ocid1.tenancy.oc1..aaaaaaaar6oqqngegbs2tthc4vjzm3ruzvrddsof45yknta2oo6jmkvcgk5q"
oci_region="us-ashburn-1"
oci_key_file="/home/akazad/miner_github/file.pem" # Ensure this path is correct and accessible

# Write the config file. Adjust the path to the key file as necessary.
cat > ~/.oci/config << EOF
[DEFAULT]
user=${oci_user_ocid}
fingerprint=${oci_fingerprint}
tenancy=${oci_tenancy_ocid}
region=${oci_region}
key_file=${oci_key_file}
EOF

# Set file permissions to be read-only by the file's owner
#chmod 600 ~/.oci/config
echo "OCI configuration written to ~/.oci/config"


echo "Testing cloud storage.."
python3 miner_github/test_oci_store2.py 
# echo "Running the miner...."
# sleep 5
# python3 miner_github/analyzer/repo_analyzer.py

# echo "Script execution completed at slave"