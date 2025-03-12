import os

def get_folder_list(keyword, p1, p2, DCC_folder):
    folder_name_base = f"{keyword}_{p1}_{p2}_ver2"
    folder_list = []

    # check the all the folders in the DCC_folder
    for folder in os.listdir(DCC_folder):
        if folder_name_base in folder:
            folder_list.append(os.path.join(DCC_folder, folder))
    
    return folder_list

def get_DCC_folder():
    # get current working directory
    cwd = os.getcwd()

    return os.path.join(cwd, "Run/DCC")

def check_DCC_folder(DCC_folder):
    count_file = os.path.join(DCC_folder, "CircRNACount")
    coordinates_file = os.path.join(DCC_folder, "CircCoordinates")
    LinearCount_file = os.path.join(DCC_folder, "LinearCount")

    if not os.path.exists(count_file):
        print(f"Error: {count_file} does not exist")
        return False
    if not os.path.exists(coordinates_file):
        print(f"Error: {coordinates_file} does not exist")
        return False
    if not os.path.exists(LinearCount_file):
        print(f"Error: {LinearCount_file} does not exist")
        return False

    return True

def get_command(DCC_folder):
    # find the log file which ends with .log
    log_file = None

    for file in os.listdir(DCC_folder):
        if file.endswith(".log"):
            log_file = file
            break
    
    # open log file and get the line two as the command
    with open(os.path.join(DCC_folder, log_file), "r") as f:
        command_line = f.readlines()[1]
        command = command_line.split("DCC command line: ")[1]

    return command

qsub_header = f"""#!/bin/bash -l
#$ -P   casa
#$ -pe omp 8 -o log.o -e log.e -l h_rt=100:00:00 
#$ -l mem_per_core=8G
#qsub DCC2.qsub cell_type p1 p2
module load python2/2.7.16
# move to the DCC folder
cd {os.path.join(os.getcwd(), "Run/DCC")}
"""

def write_qsub_file(command, file_path):
    with open(file_path, "w") as f:
        f.write(qsub_header)
        f.write(command)

def main():
    DCC_folder = get_DCC_folder()
    
    keyword = input("Enter the sample name: ")
    p1 = input("Enter the first parameter: ")
    p2 = input("Enter the second parameter: ")

    folder_list = get_folder_list(keyword, p1, p2, DCC_folder)
    command_list = []
    
    if len(folder_list) == 0:
        print("Error: please check the samples name")
        return

    for folder in folder_list:
        if check_DCC_folder(folder):
            continue
        
        print(f"{folder} failed")
        command = get_command(folder)
        command_list.append("python2 "+ command)
    
    if not command_list:
        print("All the DCC folders are correct")
        return

    # remove the fix folder if it exists
    if os.path.exists("DCC_fix"):
        os.system("rm -r DCC_fix")
    # create the fix folder
    os.system("mkdir DCC_fix")

    for ind, command in enumerate(command_list):
        filename = f"file_{ind}.qsub"
        file_path = os.path.join("DCC_fix", filename)
        write_qsub_file(command, file_path)
    
    # create submit file
    submit_file = os.path.join("DCC_fix", "submit.sh")
    with open(submit_file, "w") as f:
        for ind in range(len(command_list)):
            # absolute path
            file_path = os.path.join(os.getcwd(), "DCC_fix", f"file_{ind}.qsub")
            f.write(f"qsub {file_path}\n")
    
    print("please run the following command to fix the jobs")
    print(f"bash {submit_file}")

if __name__ == "__main__":
    main()
    