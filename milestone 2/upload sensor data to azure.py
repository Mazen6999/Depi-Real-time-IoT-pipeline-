import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# --- Configuration ---
load_dotenv()  # Load variables from the .env file into the environment

# Read the connection string from the .env file
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# The name of the container you created in Azure
CONTAINER_NAME = "raw-data" 

# Get the current script directory to create a relative path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# The file you want to upload
LOCAL_FILE_PATH = os.path.join(BASE_DIR, 'milestone 1', 'sensors.csv')

# The name you want the file to have in Azure
BLOB_NAME = "sensors.csv" 
# --------------------

def upload_file_to_blob():
    """Connects to Azure, uploads the file, and overwrites if it exists."""
    try:
        # 1. Create a client to interact with the blob service
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

        # 2. Get a client to interact with a specific container
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)

        print(f"Uploading '{LOCAL_FILE_PATH}' to container '{CONTAINER_NAME}'...")

        # 3. Get a client to interact with a specific blob (file)
        blob_client = container_client.get_blob_client(BLOB_NAME)

        # 4. Upload the local file
        with open(LOCAL_FILE_PATH, "rb") as file:
            # The overwrite=True argument tells Azure to replace the file if it's already there
            blob_client.upload_blob(file, overwrite=True)

        print("Upload complete!")

    except FileNotFoundError:
        print(f"Error: The file '{LOCAL_FILE_PATH}' was not found.")
        print("Please ensure your generator.py has created the CSV file.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Run the upload function ---
if __name__ == "__main__":
    upload_file_to_blob()
    input("Press Enter to continue...")