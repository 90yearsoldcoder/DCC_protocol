import os
from break_point import break_point_recorder
from star import star_helper

def check_missing_files(file_path, prefix_suffix_list):
    missing_files = []
    current_directory = os.getcwd()
    
    with open(file_path, 'r') as file:
        for line in file:
            sample_id = line.strip()
            for prefix, suffix in prefix_suffix_list:
                checking_file_path = os.path.join(prefix, sample_id + suffix)
                #print(checking_file_path)
                if os.path.exists(checking_file_path) == False or os.path.getsize(checking_file_path) == 0:
                    missing_files.append(sample_id)
                    break

    return missing_files

def run_STAR_fix():
    flag = input("Do you want to resubmit the tasks to fix the STAR failure?(y/n): ")

    if (flag != 'y' and flag != 'Y'):
        return
    
    dic=break_point_recorder.read(os.getcwd())
    star_helper.func(dic['project_name'],dic['download_name'], user=dic['user'], fix = True)

if __name__ == "__main__":
    current_directory = os.getcwd()
    sample_name = input("Input the sample name: ")
    paired_flag = True
    while True:
        tmp = input("Single or Paired (S or P): ")
        if tmp == 'S':
            paired_flag = False
            break
        elif tmp == 'P':
            paired_flag = True
            break
        else:
            print("Please tell me the paired/string information with P or S")
    
    prefix_suffix_list_paired = [
                        (os.path.join(current_directory, f"Run/Star/{sample_name}/mate1"), '_1.fastq.gz_Aligned.sortedByCoord.out.bam'), 
                        (os.path.join(current_directory, f"Run/Star/{sample_name}/mate1"), '_1.fastq.gz_Chimeric.out.junction'), 
                        (os.path.join(current_directory, f"Run/Star/{sample_name}/mate2"), '_2.fastq.gz_Aligned.sortedByCoord.out.bam'), 
                        (os.path.join(current_directory, f"Run/Star/{sample_name}/mate2"), '_2.fastq.gz_Chimeric.out.junction'), 
                        (os.path.join(current_directory, f"Run/Star/{sample_name}/sample_sheet"), '_Aligned.sortedByCoord.out.bam'), 
                        (os.path.join(current_directory, f"Run/Star/{sample_name}/sample_sheet"), '_Chimeric.out.junction'), 
                        ]
    prefix_suffix_list_single= [
                        (os.path.join(current_directory, f"Run/Star/{sample_name}/sample_sheet"), '_Aligned.sortedByCoord.out.bam'), 
                        (os.path.join(current_directory, f"Run/Star/{sample_name}/sample_sheet"), '_Chimeric.out.junction'), 
                        ]
    list_path = os.path.join(current_directory, f"Cache/{sample_name}.txt")
    
    if paired_flag == True:
        missing = check_missing_files(list_path, prefix_suffix_list_paired)
    else:
        missing = check_missing_files(list_path, prefix_suffix_list_single)

    if len(missing) == 0:
        print("STAR Alignment result check: Passed")
    else:
        print("STAR Alignment result check: Failed")
        print("The following samples do not have STAR result: Check the file, ./Cache/STAR_fix.txt")
        print(missing)

        pwd = os.getcwd()
        fix_txt_path = os.path.join(pwd, 'Cache', "STAR_fix.txt")

        with open(fix_txt_path, "w") as f:
            for sample_id in missing:
                f.write(f"{sample_id}\n")

        run_STAR_fix()
                        