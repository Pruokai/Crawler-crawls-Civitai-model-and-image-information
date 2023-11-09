import os
import shutil

# 创建目标文件夹
def create_target_folders(num_folders):
    for i in range(1, num_folders + 1):
        folder_name = f"models{i}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

# 移动文件到各文件夹
def move_files_to_folders(folder_limit):
    files = os.listdir("models")
    file_count = len(files)
    folder_count = (file_count // folder_limit) + 1 if file_count % folder_limit != 0 else file_count // folder_limit

    for i in range(folder_count):
        folder_name = f"models{i+1}"
        os.makedirs(folder_name, exist_ok=True)
        start_index = i * folder_limit
        end_index = (i + 1) * folder_limit if i < folder_count - 1 else file_count

        for file in files[start_index:end_index]:
            source_path = os.path.join("models", file)
            dest_path = os.path.join(folder_name, file)
            if not os.path.exists(dest_path):
                shutil.copy(source_path, dest_path)

if __name__ == "__main__":
    create_target_folders(9)  # 创建9个文件夹，每个文件夹放10000个文件
    move_files_to_folders(10000)  # 将文件移动到各文件夹
