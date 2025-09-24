# imports
import socket
from pydriller import Repository
from pydriller import ModificationType as ModType
import pandas as pd
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
import signal

# Download the necessary NLTK models (run once)
nltk.download('punkt')
hostname = socket.gethostname()


data_threshold = 500 # threshold to write how many data in one file
commit_data = [] # running commit data buffer
#commit_data_url = []

# Initialize a global batch_id
batch_id = 0
batch_id_url = 0
seen_hashes = set()
total_found = 0
#total_found_url = 0
repo_counter_success = 0
repo_counter_fail = 0
total_commit = 0
# Disable tokenizers parallelism
os.environ["TOKENIZERS_PARALLELISM"] = "false"
cpu_count = os.cpu_count()
torch.set_num_threads(cpu_count)
torch.set_num_interop_threads(1)

class CommitTimeout(Exception):
    pass

def _commit_timeout_handler(signum, frame):
    raise CommitTimeout()

signal.signal(signal.SIGALRM, _commit_timeout_handler)


def clear_crontab():
    os.system('crontab -r')
    print("All crontab entries have been removed.")

 # Check if GPU (CUDA) is available, else use CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

##### loading the classifier model ########
# Load the tokenizer and model only once, use them for all predictions

tokenizer = AutoTokenizer.from_pretrained("/users/akazad/perfannotator-mini/fine_tuned_graphcodebert_best_170K")
model = AutoModelForSequenceClassification.from_pretrained("/users/akazad/perfannotator-mini/fine_tuned_graphcodebert_best_170K")
# Move model to the chosen device
model.to(device).eval()
# #### loading the classifier model Ends #####
MAX_LEN = min(512, getattr(tokenizer, "model_max_length", 512))

# root for the script
storage_dir = "/nfs"
root_dir = "/users/akazad/perfminer/analyzer" #for test

# Logging configuration
logs_dir = os.path.join(root_dir, "logs") #log directory
os.makedirs(logs_dir, exist_ok=True)  # Ensure the logs directory exists
log_file_path = os.path.join(logs_dir, f"log_{hostname}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.txt")
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info(f"Using device {device}")
logging.info(f"Using {cpu_count} CPU cores")


# # Create a 'results' directory if it doesn't exist
# results_dir = f'{storage_dir}/results_java'
# if not os.path.exists(results_dir):
#     os.makedirs(results_dir)
# # Set up the filename using only the hostname
# out_filename = f"java_{hostname}.jsonl"
# out_file_path = os.path.join(results_dir, out_filename)

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

# def get_info(repo_url):
#     # Extract the repository's owner and name from the URL
#     parts = repo_url.split('/')
#     if len(parts) < 2:
#         return None
#     owner, repo_name = parts[-2], parts[-1]

#     # GitHub API endpoint for getting repo details
#     api_url = f"https://api.github.com/repos/{owner}/{repo_name}"

#     # Make a request to the GitHub API
#     response = requests.get(api_url)

#     # Check if the request was successful
#     if response.status_code == 200:
#         repo_data = response.json()
#         # return repo_data.get('fork', False)
#         fork = repo_data.get('fork', False)
#         size = repo_data.get('size', 0)
#         return { "fork": fork, "size": size}
#     else:
#         logging.info(f"Failed to fetch repository data: Status code {response.status_code}")
#         return None

def get_public_ip(sshhosts_path='/users/akazad/perfminer/sshhosts_hostname'):
    ip_address = get_ip_from_sshosts(sshhosts_path)
    if ip_address:
        logging.info(f"fetched IP locally!")
        return ip_address
    
    # If that fails, fall back to the API method
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        if response.status_code == 200:
            return response.text
    except requests.RequestException as e:
        logging.error(f"Error fetching public IP: {e}")
        return "ErrorFetchingIP"



# get token length using tokenizer

def pack_inputs_once(msg: str, diff: str):
    # exact count (no truncation) so you can compute the flag
    enc_full = tokenizer(
        msg or "", diff or "",
        add_special_tokens=True,
        truncation=False,
        return_attention_mask=True,
        return_token_type_ids=False,
    )
    n_tokens = len(enc_full["input_ids"])
    fits_flag = 1 if n_tokens <= MAX_LEN else 0

    # build actual inputs, truncating ONLY the second sequence (diff) if needed
    enc_used = tokenizer(
        msg or "", diff or "",
        add_special_tokens=True,
        truncation="only_second",      # <-- key line
        max_length=MAX_LEN,
        return_attention_mask=True,
        return_token_type_ids=False,
    )

    inputs = {
        "input_ids": torch.tensor([enc_used["input_ids"]]),
        "attention_mask": torch.tensor([enc_used["attention_mask"]]),
    }
    return inputs, fits_flag, n_tokens #document these return values input, fits_flag, n_tokens


# set once, from your notebook sweep
DEFAULT_THRESHOLD = 0.5

@torch.inference_mode()
def classify_inputs(inputs, threshold: float = DEFAULT_THRESHOLD):
    """
    inputs: dict with 'input_ids' and 'attention_mask' (single example).
    Returns: (is_perf:int, prob_perf:float)
    """
    dev = next(model.parameters()).device  # model is already on CPU in your setup
    ii = inputs["input_ids"].to(dev, non_blocking=True)
    am = inputs["attention_mask"].to(dev, non_blocking=True)

    logits = model(input_ids=ii, attention_mask=am).logits      # shape [1, num_labels]
    probs  = torch.softmax(logits, dim=-1).squeeze(0)           # shape [num_labels]

    prob_perf = float(probs[1].item())                          # class 1 = Perf
    is_perf   = 1 if prob_perf >= threshold else 0
    return is_perf, prob_perf



# classification function
def get_prediction(input_text):
    """
    Accepts input_text and predicts 3 classes: LABEL_0, LABEL_1(Perf) or LABEL_2 
    """
    
    # Tokenize the input text
    inputs = tokenizer(input_text, return_tensors="pt",truncation=True, max_length=512)
    # Move the input tensors to the same device as the model
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        logits = model(**inputs).logits
    predicted_class_id = logits.argmax().item()
    predicted_label = model.config.id2label[predicted_class_id]
    return predicted_label

def read_repository_urls_from_csv(input_csv_file):
    logging.info(f"Processing input filename: {input_csv_file}")
    with open(input_csv_file, 'r') as input_file:
        reader = csv.reader(input_file)
        next(reader, None)  # Skip the header row
        repo_urls = {row[6] for row in reader}
    return list(repo_urls)

def write_commit_data_to_file_and_upload(results_dir, file_prefix):
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
    filename = f"{file_prefix}_{hostname}_batch_{batch_id}_{timestamp}.jsonl"
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
fixes_re = re.compile("fix(es)?\\s+#\\d+", re.I)
merge_re0   = re.compile(r"merge pull request[^\n]+", re.I)
merge_re1   = re.compile(r"merge (remote-tracking )?branch[^\n]+", re.I)
sign_re0    = re.compile(r"(Signed-off-by|Reviewed-By|Change-Id):[^\n]+", re.I)
git_svn_re0 = re.compile(r"git-svn-id:[^\n]+", re.I)
bot_re0     = re.compile(r"(dependabot|renovate)[\s\S]*", re.I)  # if you truly want to drop bot-y lines
ticket_re0  = re.compile(r"Ticket:\s*[^\n]+", re.I)
url_re      = re.compile(r"(?i)\b(?:https?://|www\.)\S+")
email_re    = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")


def clean_commit_message(msg: str) -> str:
    s = msg or ""
    s = fixes_re.sub("", s)
    s = merge_re0.sub("", s)
    s = merge_re1.sub("", s)
    s = sign_re0.sub("", s)
    s = git_svn_re0.sub("", s)
    s = bot_re0.sub("", s)
    s = ticket_re0.sub("", s)

    # normalize URLs and emails
    s = url_re.sub("<url>", s)
    s = email_re.sub("<email>", s)  

    s = s.replace("\n", " ")
    s = " ".join(s.split())  # normalize whitespace
    return s


# python ['.py']
# c/c++ ['.cu', '.cuh', '.c', '.h', '.cpp', '.hpp', '.cc', '.c++', '.cxx']

def mine_repo_commits(repo_url, file_types=None, results_dir=None, file_prefix="cpp"):
    assert file_types is not None, "file_types must be provided"
    global seen_hashes
    global total_commit
    global batch_id
    global batch_id_url
    global total_found
    #global total_found_url
    global commit_data
    #global commit_data_url
    global data_threshold
    global repo_counter_fail
    global repo_counter_success
    local_commit_counter = 0
    #local_commit_counter_url = 0
    start_time = time.time()  # Record the start time for the current repository

    try:
        for commit in Repository(repo_url, only_no_merge=True, only_modifications_with_file_types=file_types).traverse_commits():
            total_commit += 1
            
            try: 
                commit_message = commit.msg or ""
                l = len(commit_message.split())
                if l >= 1000:
                    logging.info(f"Too big commit message!")
                    signal.alarm(0)  # Cancel the alarm
                    continue
                if l <= 3:
                    signal.alarm(0)  # Cancel the alarm
                    continue
                
                # now clean the commit message and proceed
                commit_message = clean_commit_message(commit_message)
                
                if 'merge' in commit_message or 'revert' in commit_message:
                    logging.info(f"Skipping merge commit: {commit.hash}")   
                    signal.alarm(0)  # Cancel the alarm  
                    continue
                
                # we are only interested in commit with single changed file
                # and that file should have only one modified method
                # and the commit should be classified as perf by our model
                # also skip if the commit message or code diff is too long
                # (token length > 512)
                # also skip if the commit is a merge or revert commit
                # also skip if the original source code is too large (>150k words)
                # also skip if the commit is duplicate based on original+modified code
                # also skip if the commit is changing a file that is added or deleted
                
                no_changed_files = commit.files # use this because it's lightweight way to know number of changed files
                if  no_changed_files == 1:
                    modified_file = commit.modified_files[0]
                    
                    # some guardrails
                    if getattr(modified_file, "is_binary", False):
                        logging.info(f"Skipping binary file commit: {commit.hash}")
                        signal.alarm(0)  # Cancel the alarm
                        continue
                    
                    # get diff FIRST, and skip giant ones to avoid parser hangs
                    code_diff = modified_file.diff or ""
                    if len(code_diff) > 500_000:
                        logging.info("Avoid large diff >500k: %s %s", repo_url, commit.hash)
                        signal.alarm(0)  # Cancel the alarm
                        continue
                    signal.alarm(10)  # arm the alarm
                    try:
                        no_modified_method = len(modified_file.changed_methods)
                        if no_modified_method != 1:
                             continue
                        
                        if modified_file.change_type in [ModType.ADD, ModType.DELETE]:
                            continue
                        #get_prediction(commit_message) == 'LABEL_1':
                        
                        # we have single file/methodd changed file,  now check if perf commit

                        inputs, fits_flag, n_tokens = pack_inputs_once(commit_message, code_diff) 
                        is_perf, prob_perf = classify_inputs(inputs, threshold=0.5)
                        if is_perf != 1:
                            continue
                        
                        
                        #if modified_file.change_type not in [ModType.ADD, ModType.DELETE]:
                        

                        # now we have a perf commit with single changed file and method
                        # original source code
                        src_original = modified_file.source_code_before or "na"
                        if src_original != "na" and len(src_original) > 1_000_000:
                            logging.info(f"Avoid large file 1Mb: %s %s", repo_url, commit.hash)
                            continue
                        
                        src_modified = modified_file.source_code or "na"
                        key = src_original + src_modified # the idea is comes from disticnt traning data sicne we pass this code, so focus on it
                        #deduplicate based on this
                        # get commit hash
                        key_hash = hashlib.md5(key.encode('utf-8')).hexdigest()
                        if key_hash in seen_hashes:
                            logging.info(f"Skipping duplicate commit: {commit.hash}")
                            continue
                        #now proceed, extract info for this commit which met all our critera
                        # mark it seen to avoid duplicate
                        seen_hashes.add(key_hash)
                        
                        
                        total_found += 1
                        local_commit_counter += 1
                        
                        # NEW: log the commit and counter
                        logging.info(
                            "Performance commit %d found: %s/commit/%s",
                            total_found,
                            repo_url,
                            commit.hash,
                        )
                                            
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
                        orig_method_loc_start = orig_method_loc_end = None
                        func_token = None
                        for func in methods:
                            if func.name == changed_method_name:
                                orig_method_loc_start = func.start_line
                                orig_method_loc_end = func.end_line
                                #func_token = func.token_count
                                func_token = getattr(func, "token_count", None)
                                break
                        # loc_orig_method = f'[{orig_method_loc_start}:{orig_method_loc_end}]'
                        loc_orig_method = f'[{orig_method_loc_start}:{orig_method_loc_end}]' if orig_method_loc_start else "na"
                        
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
                            #'author_name': author.name,
                            'nloc': n_loc,
                            'n_added_lines': n_added_lines,
                            'n_deleted_lines': n_deleted_lines,
                            'modified_method': changed_method_name,
                            'loc_before': loc_orig_method,
                            'loc_after': loc_changed_method,
                            'src_before': src_original,
                            'src_after': src_modified,
                            'diff': code_diff,
                            'func_no_tokens': func_token,
                            'context_flag': fits_flag,
                            'n_tokens': n_tokens,
                            'probability': prob_perf,
                        }
                        # add this commit info to running list
                        commit_data.append(commit_info)
                        # cancel alarm on success
                        signal.alarm(0)
                        total_found += 1
                        local_commit_counter += 1
                        logging.info(f"Total perf found: {total_found}")

                        if len(commit_data) == data_threshold:
                            batch_id += 1
                            write_commit_data_to_file_and_upload(results_dir, file_prefix)
                    finally:
                        signal.alarm(0)  # Cancel the alarm
                    #else:
                    #    continue
            except CommitTimeout:
                signal.alarm(0)  # Cancel the alarm
                logging.warning(f"Timeout processing commit: {getattr(commit, 'hash', '?')} in {repo_url}")
                continue
            except Exception:
                #logging.error(f"Error processing commit '{commit.hash}' in repository '{repo_url}': {commit_error}")
                logging.exception("Error processing commit %s in %s", getattr(commit, "hash", "?"), repo_url)
                # Continue to the next commit despite the error
                #cancel  alarm
                signal.alarm(0)
                continue
        #repo_counter_success += 1
        return True
    except Exception:
        
        # This is a repo-level failure (clone/fetch/IO/etc.)
        logging.exception("Repository-level failure while accessing %s", repo_url)
        #repo_counter_fail += 1
        return False

        # Continue to the next repository despite the error

    finally:
        elapsed = time.time() - start_time
        logging.info("Time taken for %s: %.2fs; local_perf_found=%d",
                     repo_url, elapsed, local_commit_counter)

def _safe_write_csv(df: pd.DataFrame, path: str) -> None:
    """
    Atomically write the dataframe to CSV.
    """
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", newline="") as f:
        df.to_csv(f, index=False)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)


def _set_status(df: pd.DataFrame, idx: int, status: str) -> None:
    """
    Set status and keep 'processed' in sync for backward compatibility.
    """
    df.at[idx, "status"] = status
    df.at[idx, "processed"] = (status in ("done", "skipped"))
    
    

def _progress_counts(df: pd.DataFrame):
    vc = df["status"].value_counts()
    done     = int(vc.get("done", 0))
    failed   = int(vc.get("failed", 0))
    skipped  = int(vc.get("skipped", 0))
    in_prog  = int(vc.get("in_progress", 0))
    pending  = int(vc.get("pending", 0))
    processed = done + failed + skipped
    return processed, pending, in_prog, done, failed, skipped



import argparse

def main():
    global total_commit, batch_id, batch_id_url, total_found
    #global total_found_url
    global commit_data
    #global commit_data_url
    global repo_counter_fail
    global repo_counter_success
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--language",
        choices=["java", "python", "cpp"],
        required=True,
        help="Language to mine (affects results directory and file types)",
    )
    args = parser.parse_args()

    # choose file types based on language
    if args.language == "java":
        file_types = [".java"]
    elif args.language == "python":
        file_types = [".py"]
    else:
        file_types = [
            ".cu", ".cuh", ".c", ".h", ".cpp",
            ".hpp", ".cc", ".c++", ".cxx",
        ]

    # build the results directory and output filename
    results_dir = f"{storage_dir}/results_{args.language}"
    os.makedirs(results_dir, exist_ok=True)
    file_prefix = args.language
    out_filename = f"{args.language}_{hostname}.jsonl"
    out_file_path = os.path.join(results_dir, out_filename)
    
    
    
    logging.info("Starting mining..")

    host_ip = get_public_ip()
    date = datetime.date.today().strftime("%m%d%Y")
    
    # here we read the .csv file containg this node's split of the repo list to be mined
    input_csv_file = os.path.join(root_dir, f"github_repositories_{host_ip}.csv")
    if not os.path.exists(input_csv_file):
        logging.error(f"Input CSV not found: {input_csv_file}")
        return
    #input_csv_file = "filteredpython.csv"
    
    # Sidecar state CSV path (progress lives here, not in the original)
    state_csv_file = os.path.splitext(input_csv_file)[0] + ".state.csv"
    # Create state CSV if missing (copy columns from input and add status fields)
    if not os.path.exists(state_csv_file):
        base_df = pd.read_csv(input_csv_file)
        # Ensure expected columns exist
        for col in ("url", "size_kb", "is_fork"):
            if col not in base_df.columns:
                logging.error(f"Required column '{col}' missing in input CSV.")
                return
        state_df = base_df[["url", "size_kb", "is_fork"]].copy()
        state_df["processed"] = False
        state_df["status"] = "pending"
        state_df["retries"] = 0
        state_df["started_at"] = ""
        state_df["finished_at"] = ""
        _safe_write_csv(state_df, state_csv_file)
        logging.info(f"Initialized state file: {state_csv_file}")
    else:
        logging.info(f"Using existing state file: {state_csv_file}")
    
    # create df frame from state csv
    df = pd.read_csv(state_csv_file)
    logging.info(f"state CSV loaded into df!")
    #repo_urls = read_repository_urls_from_csv(input_csv_file)
    #unique_repo_urls = list(set(repo_urls))
    #repo_urls = ['https://github.com/opencv/opencv']  # List of repository URLs to process

    # process all the repositories in the list
    
    
    # Initialize status/processed columns (backward compatible)
    if "processed" not in df.columns:
        df["processed"] = False
        logging.info("Added 'processed' column.")

    if "status" not in df.columns:
        # Map legacy 'processed' -> 'done'/'pending'
        df["status"] = df["processed"].map(lambda x: "done" if bool(x) else "pending")
        logging.info("Added 'status' column derived from 'processed'.")
        _safe_write_csv(df, state_csv_file)

    # Crash recovery: any stale in_progress -> pending
    if (df["status"] == "in_progress").any():
        stale_idx = df.index[df["status"] == "in_progress"]
        df.loc[stale_idx, "status"] = "pending"
        # optional retry counter
        if "retries" not in df.columns:
            df["retries"] = 0
        df.loc[stale_idx, "retries"] = df.loc[stale_idx, "retries"].fillna(0) + 1
        logging.info(f"Recovered {len(stale_idx)} stale 'in_progress' rows back to 'pending'.")
        _safe_write_csv(df, state_csv_file)
    
    
    
    
    
    repo_counter = 0

    total_repo = len(df)
    
    # if 'processed' not in df.columns:
    #     df['processed'] = False
    #     logging.info(f"processed columnd added to csv")
    # df.to_csv(input_csv_file, index=False)
    # logging.info(f"CSV file updated!")
    
    


    time_start = time.time()
    #for repo_url in unique_repo_urls:
    for index, row in df.iterrows():
        #repo_url = row['url']
        repo_url = row.get('url',"")
        if not repo_url:
            logging.warning(f"Row {index} has no 'url'. Marking failed.")
            _set_status(df, index, "failed")
            _safe_write_csv(df, state_csv_file)
            continue

        status = row.get('status',"pending")
        
        if status != "pending":
            logging.info(f"Skipping repo with status {status}: {repo_url}")
            continue
        
        # Mark as in_progress BEFORE any network work, then persist
        _set_status(df, index, "in_progress")
        if "started_at" not in df.columns:
            df["started_at"] = ""
        df.at[index, "started_at"] = datetime.datetime.utcnow().isoformat()
        _safe_write_csv(df, state_csv_file)
        
        # print progress from .state.csv
        processed, pending, in_prog, done, failed, skipped = _progress_counts(df)
        logging.info(
            f"[{processed}/{total_repo}] Progress | pending={pending} "
            f"in_progress={in_prog} done={done} failed={failed} skipped={skipped} "
            f"next_repo={repo_url}"
        )



        # # if row['processed']:
        # #     logging.info(f"Skipping already processed repo: {repo_url}")
        # #     #batch_id = batch_id_nperf = 1000000
        # #     continue
        # #get meta data size is_fork
        # #get meta data size is_fork
        # df.at[index, 'processed'] = True
        # df.to_csv(input_csv_file,index=False)
        
        # get meta data size is_fork 
                # Use precomputed metadata
        try:
            fork_status = bool(int(row.get("is_fork", 0)))
        except Exception:
            fork_status = bool(row.get("is_fork", False))

        try:
            repo_size = int(row.get("size_kb", 0))  # already kB
        except Exception:
            repo_size = 0

        if fork_status:
            logging.info("Forked repo. Skipping.")
            _set_status(df, index, "skipped")
            _safe_write_csv(df, state_csv_file)
            continue

        if repo_size > 3_000_000:  # ~3 GB
            logging.info("Large repo (>~3GB). Skipping.")
            _set_status(df, index, "skipped")
            _safe_write_csv(df, state_csv_file)
            continue
        
        
        # try:
        #     meta_data = get_info(repo_url)
        #     if meta_data is not None:
        #         logging.info(f"Successfully retrieved metadata:{meta_data}")
        #         # You can access the dictionary as expected
        #         fork_status = meta_data["fork"]
        #         repo_size = meta_data["size"]
        #         logging.info(f"Fork: {fork_status}, Size: {repo_size} kB")
        #         if fork_status == True:
        #             logging.info(f"Forked skipping")
        #             continue
        #         if int(repo_size) > 3e6:
        #             logging.info(f"LargeRepo! Skipping")
        #             continue
        #     else:
        #         # Handle the case where no data was returned
        #         logging.info(f"No metadata could be retrieved.")
        # except Exception as e:
        #     logging.info(f"An error occurred while fetching the metadata: {e}")
            
            
            
        #meta_data = get_info(repo_url)
        # print progress status
        repo_counter += 1
        logging.info(f"[{repo_counter}/{total_repo}]:Progress: repository: {repo_url}")
        
        # call miner function
        
        try:
            result = mine_repo_commits(repo_url, file_types=file_types, results_dir=results_dir, file_prefix=file_prefix)
            final_status = "done" if result else "failed"
            _set_status(df, index, final_status)
            if final_status == "failed":
                repo_counter_fail += 1
            else:
                repo_counter_success += 1

        except Exception as e:
            logging.exception("Uncaught error while mining %s", repo_url)
            _set_status(df, index, "failed")
            repo_counter_fail += 1
            
        # Persist after each repo
        if "finished_at" not in df.columns:
            df["finished_at"] = ""
        df.at[index, "finished_at"] = datetime.datetime.utcnow().isoformat()
        _safe_write_csv(df, state_csv_file)
        logging.info("Updated state CSV with current repo status.")


        #result = mine_repo_commits(repo_url) 

        # df.at[index, 'processed'] = result
        # df.to_csv(input_csv_file,index=False)
        # logging.info(f"Updated csv file with current repo status!")

        # if not result:
        #     logging.info(f"Failed to process repo: {repo_url}")


        # if total_found > MAX_COMMIT:
        #     logging.info("Exiting analysis!")
        #     break
        

    logging.info(f"Writing remaining commit data if any")
    #remaining data if any
    if commit_data:
        logging.info(f"Found remaining {len(commit_data)} commit rows")
        batch_id += 1
        #write_commit_data_to_file()
        write_commit_data_to_file_and_upload(results_dir, file_prefix)
        #remaining data if any
    # time_finish = time.time()
    # total_time = time_finish - time_start
    # minutes, seconds = divmod(total_time, 60)
    # logging.info(f"Analysis is complete!. Creating poll text file..")
    
    # # record summary
    # logging.info(f"Total repository: {total_repo}")
    # logging.info(f"Total successfully processed: {repo_counter_success}")
    # logging.info(f"Total failed to process: {repo_counter_fail}")
    # logging.info(f"Total perf commit curated: {total_found}")
    # #logging.info(f"Total >20 changedFile commit curated: {total_found_url}")
    # logging.info(f"Total time taken: {int(minutes)}")
    # logging.info(f"Total commit: {total_commit}")
    
    
    # # Command to execute
    # command = 'touch script_complete.txt'

    # # Execute the command
    # result = os.system(command)

    # if result == 0:
    #     logging.info(f"File 'script_complete.txt' created successfully.")
    # else:
    #     logging.info(f"Failed to create file 'script_complete.txt'.")
    # logging.info(f'Killing the script!')
    # clear_crontab()
    
    # Summary + sentinel
    time_finish = time.time()
    total_time = time_finish - time_start
    minutes, seconds = divmod(total_time, 60)

    logging.info("Analysis complete.")
    logging.info(f"Total repository rows: {total_repo}")
    logging.info(f"Total successfully processed: {repo_counter_success}")
    logging.info(f"Total failed to process: {repo_counter_fail}")
    logging.info(f"Total perf commits curated: {total_found}")
    logging.info(f"Total time taken (min): {int(minutes)}")
    logging.info(f"Total commits traversed: {total_commit}")

    if os.system('touch script_complete.txt') == 0:
        logging.info("File 'script_complete.txt' created successfully.")
    else:
        logging.info("Failed to create file 'script_complete.txt'.")

    logging.info("Clearing crontab and exiting.")
    clear_crontab()
    logging.info(f"All crontab entries have been removed.")

if __name__ == "__main__":
    main()
