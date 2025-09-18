# imports
import socket
from pydriller import Repository
import pandas as pd
from tqdm import tqdm
import nltk
import csv
import json
import os
import datetime
import requests
import logging
import torch
import time
import re
import gc
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig #mistral
import hashlib


# Download the necessary NLTK models (run once)
nltk.download('punkt')
hostname = socket.gethostname()


data_threshold = 500
commit_data = [] # running commit buffer
commit_data_url = []

# Initialize a global batch_id
batch_id = 0
batch_id_url = 0
seen_hashes = set()
total_found = 0
total_found_url = 0
repo_counter_success = 0
repo_counter_fail = 0
total_commit = 0
# Disable tokenizers parallelism
os.environ["TOKENIZERS_PARALLELISM"] = "false"
cpu_count = os.cpu_count()




def clear_crontab():
    os.system('crontab -r')
    print("All crontab entries have been removed.")

 # Check if GPU (CUDA) is available, else use CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
##### Roberta ########
# Load the tokenizer and model only once

tokenizer = AutoTokenizer.from_pretrained("ManojAlexender/second_Base_version_of_codebert_with_commit_and_diff")

# #### Roberta Ends #####



# root for the script
storage_dir = "/nfs"
root_dir = "miner_github/analyzer" #for test
#root_dir = "miner_github/analyzer"
# Logging configuration
logs_dir = os.path.join(root_dir, "logs") #log directory
os.makedirs(logs_dir, exist_ok=True)  # Ensure the logs directory exists
log_file_path = os.path.join(logs_dir, f"log_{hostname}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info(f"Using device {device}")





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
        logging.error(f"Error reading from sshosts: {e}")
        return None


def get_info(repo_url):
    # Extract the repository's owner and name from the URL
    parts = repo_url.split('/')
    if len(parts) < 2:
        return None
    owner, repo_name = parts[-2], parts[-1]

    # GitHub API endpoint for getting repo details
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}"

    # Make a request to the GitHub API
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        repo_data = response.json()
        # return repo_data.get('fork', False)
        fork = repo_data.get('fork', False)
        size = repo_data.get('size', 0)
        return { "fork": fork, "size": size}
    else:
        logging.info(f"Failed to fetch repository data: Status code {response.status_code}")
        return None

def get_public_ip(sshhosts_path='/users/akazad/miner_github/sshhosts_hostname'):
    ip_address = get_ip_from_sshosts(sshhosts_path)
    if ip_address:
        logging.info(f"fetched IP locally!")
        return ip_address
    
    # If that fails, fall back to the API method
    try:
        response = requests.get('https://api.ipify.org')
        if response.status_code == 200:
            return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching public IP: {e}")
        return "ErrorFetchingIP"




# Create a 'results' directory if it doesn't exist
results_dir = f'{storage_dir}/results_java'
if not os.path.exists(results_dir):
    os.makedirs(results_dir)    


# Set up the filename using only the hostname
out_filename = f"java_{hostname}.jsonl"
out_file_path = os.path.join(results_dir, out_filename)

# Function to write commit_info to file immediately
def write_commit_info(commit_info, file_path):
    with open(file_path, 'a') as file:  # Open in append mode
        file.write(json.dumps(commit_info) + '\n')

def read_repository_urls_from_csv(input_csv_file):
    logging.info(f"Processing input filename: {input_csv_file}")
    with open(input_csv_file, 'r') as input_file:
        reader = csv.reader(input_file)
        next(reader, None)  # Skip the header row
        repo_urls = {row[6] for row in reader}
    return list(repo_urls)

def write_commit_data_to_file_and_upload(results_dir):
    """
    Writes commit data to a .jsonl file, uploads it to OCI Object Storage, and removes the file locally.
    """
    global commit_data
    global batch_id
    #hostname = socket.gethostname()
    # Get the current date and time
    now = datetime.datetime.now()

    # Format the date and time to include year, month, day, hour, minute, and second
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"java_{hostname}_batch_{batch_id}_{timestamp}.jsonl"
    file_path = os.path.join(results_dir, filename)
    
    try:
        with open(file_path, 'w') as file:
            for commit_info in commit_data:
                file.write(json.dumps(commit_info) + '\n')
    except IOError as e:
        logging.info(f"An error occurred while writing or uploading the file: {e}")
    finally:
        commit_data.clear()
        logging.info(f"PERF{batch_id}: uploading complete!")
        # garbage collect and emtpy cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()



# regex to clean commit message
#fixes_re = re.compile("fix(es)?\\s+#\\d+", re.I)
merge_re0 = re.compile("merge pull request[^\\n]+", re.I)
merge_re1 = re.compile("Merge (remote-tracking )?branch[^\\n]+", re.I)
sign_re0 = re.compile("(Signed-off-by|Reviewed-By|Change-Id):[^\\n]+", re.I)
git_svn_re0 = re.compile("git-svn-id:[^\\n]+", re.I)
bot_re0 = re.compile("(.|\n)*dependabot(.|\n)*", re.I)
ticket_re0 = re.compile("Ticket: [^\\n]+", re.I)

# python ['.py']
# c/c++ ['.cu', '.cuh', '.c', '.h', '.cpp', '.hpp', '.cc', '.c++', '.cxx']

def mine_repo_commits(repo_url, file_types=['.java']):
    global seen_hashes
    global total_commit
    global batch_id
    global batch_id_url
    global total_found
    global total_found_url
    global commit_data
    global commit_data_url
    global data_threshold
    global repo_counter_fail
    global repo_counter_success
    local_commit_counter = 0
    local_commit_counter_url = 0
    start_time = time.time()  # Record the start time for the current repository

    try:
        for commit in Repository(repo_url, only_no_merge=True, only_modifications_with_file_types=file_types).traverse_commits():
            total_commit += 1
            try: 
                commit_message = commit.msg
                # clean data please
                #commit_message = fixes_re.sub("", commit_message)
                commit_message = merge_re0.sub("", commit_message)
                commit_message = merge_re1.sub("", commit_message)
                commit_message = sign_re0.sub("", commit_message)
                commit_message = git_svn_re0.sub("", commit_message)
                commit_message = bot_re0.sub("", commit_message)
                commit_message = bot_re0.sub("", commit_message)
                commit_message = ticket_re0.sub("", commit_message)
                commit_message = commit_message.replace('\n', ' ').strip()
                
                l = len(commit_message.split())
                if l >= 1000:
                    logging.info(f"Too big commit message!")
                    continue
                if l <= 3:
                    continue
                no_changed_files = commit.files
                if  no_changed_files == 1: # and get_prediction_mistral(commit_message): #get_prediction(commit_message) == 'LABEL_1':
                    modified_file = commit.modified_files[0]
                    code_diff = modified_file.diff
                    if len(tokenizer.tokenize(commit_message)) + len(tokenizer.tokenize(code_diff)) > 515:
                        logging.info(f"Context Exceded! Skipping")
                        continue
                    input_text = commit_message + ' ' + code_diff

                    if modified_file.change_type not in ["ADD", "DELETE"]:
                        no_modified_method = len(modified_file.changed_methods)
                        if  no_modified_method == 1:
                            pred = True
                            if pred == True:
                                if 'merge' in commit_message or 'revert' in commit_message:
                                    logging.info(f"Skipping merge commit: {commit.hash}")
                                    continue
                                # get commit hash

                                # original source code
                                
                                src_original = modified_file.source_code_before or "na"
                                lsrc = len(src_original.split())
                                if lsrc >= 150000: #skip large file
                                    logging.info(f"Avoid large file 1Mb")
                                    continue
                                src_modified = modified_file.source_code or "na"
                                key = src_original + src_modified # the idea is comes from disticnt traning data sicne we pass this code, so focus on it
                                #deduplicate based on this

                                key_hash = hashlib.md5(key.encode('utf-8')).hexdigest()
                                if key_hash in seen_hashes:
                                    logging.info(f"Skipping duplicate commit: {commit.hash}")
                                    continue
                                #now proceed, extract info for this commit which met all our critera
                                # mark it seen to avoid duplicate
                                seen_hashes.add(key_hash)
                                # get changed method name
                                changed_method_name = modified_file.changed_methods[0].name
                                
                                # get the commmit url
                                commit_url = repo_url
                                # get hash 
                                sha = commit.hash
                                # get filename
                                filename = modified_file.filename
                                # get changed method's location
                                changed_method_loc_start = modified_file.changed_methods[0].start_line
                                changed_method_loc_end = modified_file.changed_methods[0].end_line
                                loc_changed_method = f'[{changed_method_loc_start}:{changed_method_loc_end}]'
                                # get the list of methods in this file
                                methods = modified_file.methods_before
                                # now iterate through these methods to extract original version
                                # of the changed_method
                                for func in methods:
                                    if func.name == changed_method_name:
                                        orig_method_loc_start = func.start_line
                                        orig_method_loc_end = func.end_line
                                        func_token = func.token_count
                                        break
                                loc_orig_method = f'[{orig_method_loc_start}:{orig_method_loc_end}]'
                                
                                #get tokens in file
                                #file_tokens = modified_file.token_count
                                n_loc = modified_file.nloc
                                n_added_lines = modified_file.added_lines
                                n_deleted_lines = modified_file.deleted_lines
                                
                                author = commit.author
                                # its time to concat all these info
                                commit_info = {
                                    'project_name': commit.project_name,
                                    'commit_url': commit_url + '/commit/' + commit.hash,
                                    'commit_message': commit_message,
                                    'filename': filename,
                                    'commit_date': str(commit.committer_date),
                                    'author_email': author.email,
                                    'author_name': author.name,
                                    'nloc': n_loc,
                                    'n_added_lines': n_added_lines,
                                    'n_deleted_lines': n_deleted_lines,
                                    'modified_method': changed_method_name,
                                    'loc_before': loc_orig_method,
                                    'loc_after': loc_changed_method,
                                    'src_before': src_original,
                                    'src_after': src_modified,
                                    'diff': code_diff,
                                    'func_no_tokens': func_token
                                }
                                # add this commit info to running list
                                commit_data.append(commit_info)
                                #write_commit_info(commit_info,out_file_path)

                                total_found += 1
                                local_commit_counter += 1
                                logging.info(f"Total perf found: {total_found}")

                                if len(commit_data) == data_threshold:
                                    batch_id += 1
                                    #write_commit_data_to_file()
                                    write_commit_data_to_file_and_upload(namespace, bucket_name, results_dir)
                            # else:
                            #     if 'merge' in commit_message or 'revert' in commit_message:
                            #         logging.info(f"Skipping merge commit: {commit.hash}")
                            #         continue
                            #     # get commit hash

                            #     # original source code
                            #     code_diff = modified_file.diff
                            #     src_original = modified_file.source_code_before or "na"
                            #     src_modified = modified_file.source_code or "na"
                            #     key = src_original + src_modified # the idea is comes from disticnt traning data sicne we pass this code, so focus on it
                            #     #deduplicate based on this

                            #     key_hash = hashlib.md5(key.encode('utf-8')).hexdigest()
                            #     if key_hash in seen_hashes:
                            #         logging.info(f"Skipping duplicate commit: {commit.hash}")
                            #         continue
                            #     #now proceed, extract info for this commit which met all our critera
                            #     # get changed method name
                            #     changed_method_name = modified_file.changed_methods[0].name
                                
                            #     # get the commmit url
                            #     commit_url = repo_url
                            #     # get hash 
                            #     sha = commit.hash
                            #     # get filename
                            #     filename = modified_file.filename
                            #     # get changed method's location
                            #     changed_method_loc_start = modified_file.changed_methods[0].start_line
                            #     changed_method_loc_end = modified_file.changed_methods[0].end_line
                            #     loc_changed_method = f'[{changed_method_loc_start}:{changed_method_loc_end}]'
                            #     # get the list of methods in this file
                            #     methods = modified_file.methods_before
                            #     # now iterate through these methods to extract original version
                            #     # of the changed_method
                            #     for func in methods:
                            #         if func.name == changed_method_name:
                            #             orig_method_loc_start = func.start_line
                            #             orig_method_loc_end = func.end_line
                            #             func_token = func.token_count
                            #             break
                            #     loc_orig_method = f'[{orig_method_loc_start}:{orig_method_loc_end}]'
                                
                            #     #get tokens in file
                            #     #file_tokens = modified_file.token_count
                            #     n_loc = modified_file.nloc
                            #     n_added_lines = modified_file.added_lines
                            #     n_deleted_lines = modified_file.deleted_lines
                                
                            #     # its time to concat all these info
                            #     commit_info = {
                            #         'commit_url': commit_url + '/commit/' + commit.hash,
                            #         'commit_message': commit_message,
                            #         'filename': filename,
                            #         'commit_date': str(commit.committer_date),
                            #         #'no_tokens': file_tokens,
                            #         'nloc': n_loc,
                            #         'n_added_lines': n_added_lines,
                            #         'n_deleted_lines': n_deleted_lines,
                            #         'modified_method': changed_method_name,
                            #         'loc_before': loc_orig_method,
                            #         'loc_after': loc_changed_method,
                            #         'src_before': src_original,
                            #         'src_after': src_modified,
                            #         'diff': code_diff,
                            #         'func_no_tokens': func_token
                            #     }
                            #     # add this commit info to running list
                            #     commit_data_nperf.append(commit_info)
                            #     # mark it seen to avoid duplicate
                            #     seen_hashes.add(key_hash)
                            #     total_found_nperf += 1
                            #     local_commit_counter_nperf += 1
                            #     logging.info(f"Total nperf found: {total_found_nperf}")

                            #     if len(commit_data_nperf) == data_threshold:
                            #         batch_id_nperf += 1
                            #         #write_commit_data_to_file()
                            #         write_commit_data_to_file_and_upload_nperf(namespace, bucket_name, results_dir)
                elif no_changed_files > 1: #and no_changed_files <= 20 and get_prediction(commit_message):
                    continue
                    # commit_info = {
                    #     'url': repo_url + '/commit/' + commit.hash
                    # }
                    # # add this commit info to running list
                    # commit_data_url.append(commit_info)
                    # if len(commit_data_url) == data_threshold:
                    #     batch_id_url += 1
                    #     #write_commit_data_to_file()
                    #     write_commit_data_to_file_and_upload_url(namespace, bucket_name, results_dir)
        
                    
                
            except Exception as commit_error:
                logging.error(f"Error processing commit '{commit.hash}' in repository '{repo_url}': {commit_error}")
                # Continue to the next commit despite the error
                continue
        repo_counter_success += 1
        return True
    except Exception as repo_error:
        repo_counter_fail += 1
        logging.error(f"Error while accessing repository '{repo_url}': {repo_error}")
        return True
        
        # Continue to the next repository despite the error

    finally:
        end_time = time.time()  # End time for the current repository
        time_taken = end_time - start_time
        logging.info(f"Time taken for processing {repo_url}: {time_taken} seconds")
        logging.info(f"local_commit_found (perf/nperf):{local_commit_counter}/{local_commit_counter_url}: {repo_url}")



def main():
    global total_commit
    global batch_id
    global batch_id_url
    global total_found
    global total_found_url
    global commit_data
    global commit_data_url
    global repo_counter_fail
    global repo_counter_success
    logging.info("Starting mining..")

    host_ip = get_public_ip()
    date = datetime.date.today().strftime("%m%d%Y")
    
    # here we read the .csv file containg this node's split of the repo list to be mined
    input_csv_file = os.path.join(root_dir, f"github_repositories_{host_ip}.csv")
    #input_csv_file = "filteredpython.csv"
    # create df frame
    df = pd.read_csv(input_csv_file)
    logging.info(f"CSV loaded into df!")
    #repo_urls = read_repository_urls_from_csv(input_csv_file)
    #unique_repo_urls = list(set(repo_urls))
    #repo_urls = ['https://github.com/opencv/opencv']  # List of repository URLs to process

    # process all the repositories in the list
    repo_counter = 0

    total_repo = len(df)
    
    if 'processed' not in df.columns:
        df['processed'] = False
        logging.info(f"processed columnd added to csv")
    df.to_csv(input_csv_file, index=False)
    logging.info(f"CSV file updated!")


    time_start = time.time()
    #for repo_url in unique_repo_urls:
    for index, row in df.iterrows():
        repo_url = row['url']

        if row['processed']:
            logging.info(f"Skipping already processed repo: {repo_url}")
            #batch_id = batch_id_nperf = 1000000
            continue
        #get meta data size is_fork
        #get meta data size is_fork
        df.at[index, 'processed'] = True
        df.to_csv(input_csv_file,index=False)
        try:
            meta_data = get_info(repo_url)
            if meta_data is not None:
                logging.info(f"Successfully retrieved metadata:{meta_data}")
                # You can access the dictionary as expected
                fork_status = meta_data["fork"]
                repo_size = meta_data["size"]
                logging.info(f"Fork: {fork_status}, Size: {repo_size} kB")
                if fork_status == True:
                    logging.info(f"Forked skipping")
                    continue
                if int(repo_size) > 3e6:
                    logging.info(f"LargeRepo! Skipping")
                    continue
            else:
                # Handle the case where no data was returned
                logging.info(f"No metadata could be retrieved.")
        except Exception as e:
            logging.info(f"An error occurred while fetching the metadata: {e}")
        #meta_data = get_info(repo_url)
        repo_counter += 1
        logging.info(f"[{repo_counter}/{total_repo}]:Progress: reopository: {repo_url}")
        
        # call miner function
        result = mine_repo_commits(repo_url) 

        df.at[index, 'processed'] = result
        df.to_csv(input_csv_file,index=False)
        logging.info(f"Updated csv file with current repo status!")

        if not result:
            logging.info(f"Failed to process repo: {repo_url}")


        # if total_found > MAX_COMMIT:
        #     logging.info("Exiting analysis!")
        #     break
        

    logging.info(f"Writing remaining commit data if any")
    #remaining data if any
    if commit_data:
        logging.info(f"Found remaining {len(commit_data)} commit rows")
        batch_id += 1
        #write_commit_data_to_file()
        write_commit_data_to_file_and_upload(namespace, bucket_name,results_dir)
        #remaining data if any
    # if commit_data_url:
    #     logging.info(f"Found remaining {len(commit_data_url)} commit rows")
    #     batch_id_url += 1
    #     #write_commit_data_to_file()
    #     write_commit_data_to_file_and_upload_url(namespace, bucket_name, results_dir)
    time_finish = time.time()
    total_time = time_finish - time_start
    minutes, seconds = divmod(total_time, 60)
    logging.info(f"Analysis is complete!. Creating poll text file..")
    
    # record summary
    logging.info(f"Total repository: {total_repo}")
    logging.info(f"Total successfully processed: {repo_counter_success}")
    logging.info(f"Total failed to process: {repo_counter_fail}")
    logging.info(f"Total perf commit curated: {total_found}")
    logging.info(f"Total >20 changedFile commit curated: {total_found_url}")
    logging.info(f"Total time taken: {int(minutes)}")
    logging.info(f"Total commit: {total_commit}")
    
    
    # Command to execute
    command = 'touch script_complete.txt'

    # Execute the command
    result = os.system(command)

    if result == 0:
        logging.info(f"File 'script_complete.txt' created successfully.")
    else:
        logging.info(f"Failed to create file 'script_complete.txt'.")
    logging.info(f'Killing the script!')
    clear_crontab()
    logging.info(f"All crontab entries have been removed.")

if __name__ == "__main__":
    main()
