import os
import numpy as np
import shutil
import matplotlib.pyplot as plt
import cv2
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg, which avoids Qt


def process(dataset):
    #154,206
    #237,255
    print(dataset.shape)
    if len(dataset.shape)!=7:
        dataset=dataset[:,:,:,:,3:23,58:413,143:471]
        image=dataset[0][0][0][0][3]
    else:
        dataset=dataset[:,:,:,3:23,58:413,143:471]
        image=dataset[0][0][0][3]
    #grayscale
    grey=np.zeros((*dataset.shape[:-1],))
    print(grey.shape)
    for i in range(dataset.shape[0]):
        for ii in range(dataset.shape[1]):
            for iii in range(dataset.shape[2]):
                for iv in range(dataset.shape[3]):
                    if len(dataset.shape)!=7:
                        for v in range(dataset.shape[4]):
                            img=dataset[i][ii][iii][iv][v]
                            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            grey[i][ii][iii][iv][v]=gray_img
                    else:
                        img=dataset[i][ii][iii][iv]
                        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        grey[i][ii][iii][iv]=gray_img

    return grey
    #np.save("/home/dexter/Documents/data/TTB/processed/TTB_bubble_P60",grey)

def process_npy_files_in_directory(directory,processed_dir):
    # Path to the "processed" directory
    #processed_dir = os.path.join(directory, 'processed')

    # Create the processed folder if it doesn't exist
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        # Skip the processed directory
        if 'processed' in root:
            continue

        # Process each .npy file
        for file in files:
            if file.endswith('.npy'):
                # Full path to the original .npy file
                npy_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, directory)
                processed_folder_path = os.path.join(processed_dir, relative_path)
                if not os.path.exists(os.path.join(processed_folder_path, file)):
                    print(file)
                    # Load the numpy array from the file
                    np_array = np.load(npy_file_path)
                    
                    # Apply the processing function
                    processed_array = process(np_array)

                    # Determine the relative path to the processed directory
                    relative_path = os.path.relpath(root, directory)
                    processed_folder_path = os.path.join(processed_dir, relative_path)

                    # Create the subfolder in the processed directory if it doesn't exist
                    if not os.path.exists(processed_folder_path):
                        os.makedirs(processed_folder_path)

                    # Save the processed numpy array to the corresponding folder
                    processed_file_path = os.path.join(processed_folder_path, file)
                    
                    np.save(processed_file_path, processed_array)

                    print(f"Processed and saved: {processed_file_path}")
                    os.remove(npy_file_path)
                else: 
                    print("skipping...")

# Example usage:
directory_path = '/home/dexter/Documents/data/TTB/'
process_npy_files_in_directory(directory_path,'/home/dexter/Documents/data/TTB_processed')