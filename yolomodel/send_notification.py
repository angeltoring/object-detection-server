import subprocess
from pathlib import Path
import os
import re
import requests
import shutil
import cv2
import time
import glob
import datetime
import json
from dotenv import load_dotenv


# Set this when user have signed up
USER_ID = int(os.getenv('USER_ID'))
PLANT_ID = int(os.getenv('PLANT_ID'))
DISEASES_DICT = {
    '0': "Tip Burn",
    '1': "Brown Spots",
    '2': "Yellowing and Wilting",
    '3': "Gray White",
    '4': "Healthy"
}

send_codes = {
    "Tip Burn": "T",
    "Brown Spots": "B",
    "Yellowing and Wilting": "Y",
    "Gray White": "N"
}

def take_arduino_actions(dis):
    url = "https://nft-hydrophonic-delta.vercel.app/sent-from-pi"
    headers = {}
    payload = {
        'diseases': dis,
        'id': USER_ID
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return "success"


def send_notification(current_dir, result_folder_path,first_line,largest_number):

    url = "https://nft-hydrophonic-delta.vercel.app/image-diseases-upload"
    # url = "http://localhost:3000/image-diseases-upload"
    print('Class ID:', first_line)
    payload = {
        'notification_type': DISEASES_DICT[first_line[-1]],
        'user_id': USER_ID
    }
    
    with open(current_dir + f'/test-model/capture-image-{largest_number}.jpg', 'rb') as image_file:
        image_data = image_file.read()

    current_time = datetime.datetime.now()
    files = [
        ('diseases-image', (f'notification-image-{current_time.strftime("%Y%m%d%H%M%S")}.jpg', image_data, 'image/jpeg'))
    ]

    
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)
    return "success"

def set_system_as_safe(isSafe):
    url = "https://nft-hydrophonic-delta.vercel.app/safe"
    payload = {
        'is_safe': isSafe,
        'plant_id': PLANT_ID
    }
    
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    return "success"
        
def is_currently_safe():
    url = f"https://nft-hydrophonic-delta.vercel.app/get-variables/{PLANT_ID}"
    
    headers = {}

    response = requests.request("GET", url, headers=headers)

    print("currently safe? : ", json.loads(response.text)['data']['is_system_safe'])
    return  json.loads(response.text)['data']['is_system_safe']

def is_folder_empty(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        return False

    # Check if the folder is empty
    return len(os.listdir(folder_path)) == 0


def notification_main():
    current_dir = os.getcwd()
    result_folder_path = current_dir+'/test-model'

    # Check if the folder is empty
    if is_folder_empty(result_folder_path):
        print("The folder is empty.")
    else:
        # Get a list of all "doc-*.txt" files
        txt_files = glob.glob('test-model/detection-info-*.txt')
        print('Files:', txt_files)


        # Extract the number from each filename and find the file with the maximum number
        latest_file = max(txt_files, key=lambda filename: int(os.path.splitext(os.path.basename(filename))[0].split('-')[2]))
        print("Latest File: ",latest_file)
        largest_number = int(os.path.splitext(os.path.basename(latest_file))[0].split('-')[2])

        # Read and print the content of the latest file
        with open(latest_file, 'r') as file:
            first_line = file.readline().strip().split()
            print("First Line -> : ",first_line)

            if(len(first_line) != 0):
                if(first_line[-1] != '4'):
                    send_notification(current_dir, result_folder_path,first_line,largest_number)
                    if is_currently_safe():
                        set_system_as_safe(False)
                        take_arduino_actions(send_codes[DISEASES_DICT[first_line[-1]]])
                        return "success"
                else:
                    set_system_as_safe(True)
                    print("Healthy")
                    return "success"
            else:
                print("File Empty")
                return "success"

# def delete_folder_if_exists(path):
#     if os.path.exists(path) and os.path.isdir(path):
#         try:
#             shutil.rmtree(path)
#             print(f'Successfully deleted the folder: {path}')
#         except Exception as e:
#             print(f'Failed to delete the folder: {path}. Reason: {e}')
#     else:
#         print(f'The folder: {path} does not exist')


# if __name__ == '__main__':
#     main()
    # is_currently_safe()
    
