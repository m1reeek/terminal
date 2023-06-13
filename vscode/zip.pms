import os
import zipfile

def zip_files_with_password(file_path, password):
    # Check if the path is a directory or file
    if os.path.isdir(file_path):
        # Get the directory name
        directory_name = os.path.basename(file_path)

        # Create the output zip file path
        zip_file_name = directory_name + '.zip'
        zip_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), zip_file_name)

        # Create a new zip file
        with zipfile.ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            # Set the password for the zip file
            zipf.setpassword(password.encode())

            # Add each file to the zip file
            for root, dirs, files in os.walk(file_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, file_path))

        print(f'Successfully created {zip_file_path} with password protection.')
    elif os.path.isfile(file_path):
        # Create the output zip file path
        zip_file_name = os.path.basename(file_path) + '.zip'
        zip_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), zip_file_name)

        # Create a new zip file
        with zipfile.ZipFile(zip_file_path, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            # Set the password for the zip file
            zipf.setpassword(password.encode())

            # Add the file to the zip file
            zipf.write(file_path, os.path.basename(file_path))

        print(f'Successfully created {zip_file_path} with password protection.')
    else:
        print('Invalid file or directory path.')

# Prompt the user for input
file_path = input('Enter the file or folder path to zip: ')
password = input('Enter a password: ')

zip_files_with_password(file_path, password)
