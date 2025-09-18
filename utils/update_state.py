import csv
import socket

import pandas as pd
import os
import datetime
import requests

# root for the script

root_dir = "miner_github/analyzer"

def get_ip_from_sshosts(sshosts_path):
    try:
        # Get the current node's hostname
        #hostname = socket.gethostname()
        with open(sshosts_path, 'r') as file:
            for line in file:
                line_hostname, ip_address = line.strip().split()
                if line_hostname == hostname:
                    return ip_address
    except Exception as e:
        return None

def update_first_false_to_true(file_path):
    rows = []
    updated = False

    # Read the CSV file
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader)  # If your CSV has a header row, uncomment this line
        for row in csvreader:
            if not updated and row[-1] == 'False':
                row[-1] = 'True'
                updated = True
            rows.append(row)

    # Write the updated rows back to the CSV file
    with open(file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)  # If your CSV has a header row, uncomment this line
        csvwriter.writerows(rows)


def get_public_ip(sshhosts_path='/users/akazad/miner_github/sshhosts_hostname'):
    ip_address = get_ip_from_sshosts(sshhosts_path)
    if ip_address:
        return ip_address
    
    # If that fails, fall back to the API method
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
    except requests.RequestException as e:
        return "ErrorFetchingIP"
# Example usage
def main():

    host_ip = get_public_ip()
    date = datetime.date.today().strftime("%m%d%Y")
    
    # here we read the .csv file containg this node's split of the repo list to be mined
    input_csv_file = os.path.join(root_dir, f"github_repositories_{host_ip}.csv")   
    update_first_false_to_true(input_csv_file)



if __name__ == "__main__":
    main()