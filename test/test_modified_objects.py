from pydriller import Repository
import time

repo_url = 'https://github.com/opencv/opencv'

def extract_data(modified_object):
    for m in modified_object:
        print(m.filename)
        print("Source befoer:")
        print(m.source_code_before)
        print("source after:")
        print(m.source_code)
        print("=======")
        print("Method before")
        print(m.methods_before)
        print("Methods changed")
        print(m.changed_methods)
        
# Record the start time
start_time = time.time()
for commit in Repository(repo_url, only_modifications_with_file_types=['.cu', '.cuh', '.c', '.h', '.cpp', '.hpp']).traverse_commits():
    if len(commit.modified_files) == 1:
        modified_file = commit.modified_files[0]

        if modified_file.change_type != "ADD" and modified_file.change_type != "DELETE":
            print(commit.hash)
            print("BS:")
            print(modified_file.source_code_before or "NA")
            print("SC:")
            print(modified_file.source_code or "NA")
            if len(modified_file.changed_methods) == 1:
                print("CM:")
                print(modified_file.changed_methods[0].name)
                print("[" + str(modified_file.changed_methods[0].start_line) + ":"+ str(modified_file.changed_methods[0].end_line) + "]")

            

end_time = time.time()

time_taken = end_time - start_time
print(f"Time taken by the loop: {time_taken} seconds")
