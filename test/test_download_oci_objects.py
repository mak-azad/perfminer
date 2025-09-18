import os
import json
import oci
from oci.object_storage import ObjectStorageClient
import socket

def get_oci_config():
    """
    Load the OCI configuration. Modify this function if you need to load a specific profile.
    """
    return oci.config.from_file()

def upload_file_to_object_storage(namespace, bucket_name, object_name, file_path, oci_config):
    """
    Uploads a file to Oracle Cloud Infrastructure Object Storage using streaming and deletes the file afterwards.
    """
    object_storage_client = ObjectStorageClient(oci_config)
    with open(file_path, 'rb') as file:
        object_storage_client.put_object(namespace, bucket_name, object_name, file)
        print(f"Upload completed: {object_name}")
    
    # Remove the file after successful upload
    try:
        os.remove(file_path)
        print(f"Successfully deleted local file: {file_path}")
    except OSError as e:
        print(f"Error deleting file {file_path}: {e}")

def write_commit_data_to_file_and_upload(namespace, bucket_name, commit_data, results_dir, batch_id):
    """
    Writes commit data to a .jsonl file, uploads it to OCI Object Storage, and removes the file locally.
    """
    hostname = socket.gethostname()
    filename = f"{hostname}_new_{batch_id}.jsonl"
    file_path = os.path.join(results_dir, filename)
    
    try:
        with open(file_path, 'w') as file:
            for commit_info in commit_data:
                file.write(json.dumps(commit_info) + '\n')
        
        oci_config = get_oci_config()  # Load the OCI configuration
        upload_file_to_object_storage(namespace, bucket_name, filename, file_path, oci_config)
    except IOError as e:
        print(f"An error occurred while writing or uploading the file: {e}")
    finally:
        commit_data.clear()



def download_all_objects_from_bucket(namespace, bucket_name, download_dir, oci_config):
    """
    Downloads all objects from a specified bucket in Oracle Cloud Infrastructure Object Storage, handling pagination.
    """
    object_storage_client = ObjectStorageClient(oci_config)

    # Create the directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Created directory {download_dir}")

    try:
        start = None
        cnt = 0
        while True:
            # List objects in the bucket with pagination
            list_objects_response = object_storage_client.list_objects(
                namespace,
                bucket_name,
                start=start
            )

            # Break loop if no objects are returned
            if not list_objects_response.data.objects:
                break

            # Process each object
            for obj in list_objects_response.data.objects:
                object_name = obj.name
                cnt += 1
                part = object_name.split('_')
                print(part[-1])
                
                # Filter and download specific objects
                if 'python' in object_name and part[-1] == 'perf.jsonl':
                    get_object_response = object_storage_client.get_object(namespace, bucket_name, object_name)
                    
                    # Write object content to a file in the specified directory
                    object_file_path = os.path.join(download_dir, object_name)
                    with open(object_file_path, 'wb') as file:
                        for chunk in get_object_response.data.raw.stream(1024 * 1024, decode_content=False):
                            file.write(chunk)
                    print(f"Downloaded {object_name} to {object_file_path}")

            # Update the start marker to fetch the next page of objects
            start = list_objects_response.data.next_start_with
            if not start:
                break

    except Exception as e:
        print(f"Failed to download objects due to: {e}")
    
    print(f"Total objects processed: {cnt}")

# Example usage (assuming you have configured oci_config dictionary and other parameters)
# download_all_objects_from_bucket('namespace', 'bucket_name', '/path/to/download_dir', oci_config)




def download_all_objects_from_bucket2(namespace, bucket_name, download_dir, oci_config):
    """
    Downloads all objects from a specified bucket in Oracle Cloud Infrastructure Object Storage.
    """
    object_storage_client = ObjectStorageClient(oci_config)

    # Create the directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Created directory {download_dir}")

    try:
        # List all objects in the bucket
        list_objects_response = object_storage_client.list_objects(namespace, bucket_name)
        if list_objects_response.data:
            cnt = 0
            print(len(list_objects_response.data.objects))
            for obj in list_objects_response.data.objects:
                object_name = obj.name
                cnt += 1
                part = object_name.split('_')
                print(part[-1])
                # Get the object
                if 'python' in object_name and part[-1] == 'perf.jsonl':
                    get_object_response = object_storage_client.get_object(namespace, bucket_name, object_name)
                    # Write object content to a file in the specified directory
                    object_file_path = os.path.join(download_dir, object_name)
                    with open(object_file_path, 'wb') as file:
                        for chunk in get_object_response.data.raw.stream(1024 * 1024, decode_content=False):
                            file.write(chunk)
                    print(f"Downloaded {object_name} to {object_file_path}")
    except Exception as e:
        print(f"Failed to download objects due to: {e}")
    print(cnt)
          
# Example usage
if __name__ == "__main__":
    namespace = 'idqgqghww6tn'
    bucket_name = 'bucket-20240414-1634'
    #commit_data = []  # Assume this is populated with your data
    # Example data
    commit_data = [{'id': 1, 'message': 'First commit'}, {'id': 2, 'message': 'Second commit'}]
    results_dir = 'down_python_perf'
    batch_id = 1
    
    #write_commit_data_to_file_and_upload(namespace, bucket_name, commit_data, results_dir, batch_id)
    oci_config = get_oci_config()  # Load the OCI configuration
    download_all_objects_from_bucket(namespace,bucket_name,results_dir,oci_config)
