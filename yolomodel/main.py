import subprocess
import os
import shutil
from .send_notification import notification_main
from dotenv import load_dotenv

def model_main():
    load_dotenv()

    folder_path = 'test-model'

    print("**",os.getcwd())
     # Define the directory
    dir_name = 'test-model'

    # Make sure the directory exists
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    

    folder_path = '/yolomodel/yolov5/runs/detect'
    cp = os.getcwd()
    # fp = os.path.join(cp , folder_path)
    fp = cp+folder_path
    if os.path.exists(fp):
        # Remove the entire directory
        shutil.rmtree(fp)
        # Recreate the directory
        os.makedirs(fp)

    # command = [
    #     'python', 'yolov5/detect.py',
    #     '--weights', 'yolov5/best.pt',
    #     '--conf', '0.50',
    #     '--max-det', '1',
    #     '--source', '0',
    #     '--frame_saved_interval', '13800' #every 3hr 50 min
    # ]

    command = [
        'python', 'yolomodel/yolov5/detect.py',
        '--weights', 'yolomodel/yolov5/best.pt',
        '--conf', '0.1',
        '--max-det', '1',
        '--source', f'{os.getcwd()}'+'/captured/req-image.jpg',
    ]

    result = subprocess.run(command, check=True)
    if result.returncode == 0:
        print("Detection completed successfully")
        notification_main()
        return "success"
    else:
        print("Detection failed")
        return "success"
        
if __name__ == "__main__":
    main()
