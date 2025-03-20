# DCC_protocol
It is a DCC_protocol for SCC in BU.
If you want to use it without install, please contact Mintao Lin or XiaoLing to acquire the access to [the link](https://scc-ondemand1.bu.edu/pun/sys/files/fs/restricted/projectnb/ad-portal/)<br>

The protocol is built based on [DCC](https://github.com/dieterich-lab/DCC) and [STAR](https://github.com/alexdobin/STAR) alignment. <br>

The manual with figures and details is availiable on https://drive.google.com/file/d/1xSAiqQcKFtrHVmI4W-nmSrejrLLqqk84/view?usp=sharing <br>
\
Docker is not necessary but prefered


# Dependency
### 1. DCC-kit
DCC-kit is an All-in-one integration package, containing all gene references and programs that the pipeline needs.
```
cp -r /restricted/projectnb/ad-portal/DCC_protocol .
```
It is highly **recommended**.


### 2. Settings for developers
All setting could be modified directly json files in bash_files.
 
Those json files are readable and editable. 
 
* Parameter ‘Setting’ refers to a specific path or setting;
* Parameter ‘Hidden’ shows the preference whether the setting should be modified. Try not to revise it please.
* Parameter ‘withslash’ combines the setting with the next setting. It is the guideline for generating qsub files.
* Parameter ‘silent’ is a redundant parameter for further developing needs.



# Usage
## 1. Preparation 
### 1.1 A **preferred** way: install all-in-one package
Find a new directory where you want to install the program
```
cp -r /restricted/projectnb/ad-portal/DCC_protocol .
```
You do not have to install it, if you are in BU SCC and have the permission to get into the ncrna file. The permission could be acquired by E-mail to minty@bu.edu 

### 1.2 The way for developers
If you don’t want to install the DCC-kit
```
git clone https://github.com/90yearsoldcoder/DCC_protocol.git
```
Then build the DCC-kit by your own. Check the [document](https://drive.google.com/drive/u/1/search?q=DCC) for more details.

## 2 Prepare your fastq.gz files
**Note:** You may start from SRA numbers or fastq files as well. please check [document](https://drive.google.com/drive/u/1/search?q=DCC) for more details. However, the document might not be updated to the latest, thus, some new functions are not explained as well as we did in the current `README.md`.<br>

All fastq.gz files should be in only one fold. 
If they are paired_end samples, their names should be like ‘<samplename>_1.fastq.gz’ and ‘<samplename>_2.fastq.gz’
If they are single_end samples, their names should be like ‘<samplename>_1.fastq.gz’ 
Example:
```
SRR001_1.fastq.gz //for pair 1
SRR001_2.fastq.gz //for pair 2
```
 

## 3. Start the pipeline
Choosing a new directory as your working directory.
```
python /path/to/DCC_protocol/start_fastqgz.py
```

## 4. Follow the pipeline to provide the necessary information
You may see the following instruction after starting the program
```
$ python /restricted/projectnb/ad-portal/DCC_protocol/start_fastqgz.py 
Hi, I am the DCC_pipeline helper
Version: v0.2
Hope you have already read the manual.
----------------------
Starting a new DCC-pipeline.
Please give me your SCC username(for submitting qsub tasks): <user>
Please tell me your SCC project name(eg casa): <SCC_project>
```
Please provide the `<user>` and `<SCC_project>` information

## 5. Follow the pipeline to copy the fastqgz files
In most cases, we don’t want to do any operation on your original files, so we copy them to the working directory.<br>
* What you should do is just `entering 1` in the program.<br>
* Then, it will ask you the path to your original fastq.gz files, and the name of those samples. The name is all defined by you. In our example, I call it `DC1`, which is nonsense. After that, it will double check you choose those samples. You could press y to continue.
```
You have finished:  Step 0: begin
------------------------------------
What can I do for you:
1. Go to the next step
2. Delete records
3. Enviorment Setting (Not full developed)
4. Quit the program
------------------------------------
Input the number before the function you need: 1
--------------------------
Please give me the path to Fastqgz files(eg home/test/samples):/restricted/projectnb/ad-portal/soft_link_to_dataSets/DC1
Please give me the name of those samples(eg ES_cell):DC1
--------------------------
--------------------------
If those samples are paired-ends, the name should be like <..>_1.fastqgz and <...>_2.fastqgz
If those samples are single-ends, the name should be like <..>_1.fastqgz
Example: SRR001_1.fastq.gz, SRR001_2.fastq.gz
--------------------------
We detected those samples: 
['29488_TCX.FCHMLWMDSX2_paired_2.fastq.gz', '246108_paired_1.fastq.gz'.....]
Do you want to use those samples?(y/n):y
Saved to /restricted/projectnb/ad-portal/mtlin/DCC_rerun_2024Nov/test_selfCheck/Cache/DC1.txt
```

## 6. STAR alignment
* `Enter 1` to do STAR. Paired-end or double-end is selected automatically.<br>

* When your tasks are submitted, you could quit the program and come back later.
The program will make sure you have finished all tasks before allowing you to start the next step.
It is a better choice to check the situation of tasks using `watch qstat -u <username>`

* Any time you want to come back and continue, use bash `python /path/to/DCC_protocol/start_fastq.py`

## (Optional) 7. STAR alignment check
It is likely to have aligment failure due to SCC failure, especially when your sample size is quite large. So we provide script to fix the problem automatically.
At the same working directory
```
$ python /restricted/projectnb/ad-portal/DCC_protocol/check_star.py // run the check script
Input the sample name: DC1 // enter the sample name
Single or Paired (S or P): P // enter the paired info
STAR Alignment result check: Failed  // Do all Alignment pass the check?
The following samples do not have STAR result: Check the file, ./Cache/STAR_fix.txt
['1937_TCX.FCHML2TDSX2_paired']
Do you want to resubmit the tasks to fix the STAR failure?(y/n): y // enter `y` to fix it
program_path: /restricted/projectnb/ad-portal/DCC_protocol
Please give me the length of the sequence(50, 75, 100): 100 //length of the fastq file
Your job 3173970 ("star_paired.qsub") has been submitted
```

If STAR alignment meets no failure, you will see
```
$ python /restricted/projectnb/ad-portal/DCC_protocol/check_star.py 
Input the sample name: DC1
Single or Paired (S or P): P
STAR Alignment result check: Passed
```

## 8.Generate merge_tables
* Merge_tables are several tables containing the path to Star results. It will be used for DCC process.
Enter 1 to do this part. 
* Since our program is **multi-process** program which split samples into multiple groups to speed it up, the size of the group should be provided. We recommend the size of the group is about `max(10, total number of samples/10)`. The number is actually quite variable; the smaller it is, the faster it goes and more resource it takes.

```
$ python /restricted/projectnb/ad-portal/DCC_protocol/start_fastqgz.py // resume the process
Hi, I am the DCC_pipeline helper
Version: v0.2
Hope you have already read the manual.
----------------------
Recovering the previous running DCC-pipeline.
----------------------------------------
Current qsub tasks are finished. You could go to the next step.
------------------------------------
You have finished:  Step 3: STAR alignment
------------------------------------
What can I do for you:
1. Go to the next step
2. Delete records
3. Enviorment Setting (Not full developed)
4. Quit the program
------------------------------------
Input the number before the function you need: 1
----------------------------------------
Current qsub tasks are finished. You could go to the next step.
I think they are paired-end sequences.
The number of Samples per group, for qsub running only(not for phenotype): 3 // the group size
```

## 9.DCC 
`Enter 1` to move to the DCC step, and type in the parameter 1 and parameter 2.
The detail of parameter 1 and parameter 2 could be found at https://github.com/dieterich-lab/DCC.

The two parameters refer to the Nr setting in DCC program:
```
-NR 5 6 \ MINIMUM COUNT IN ONE REPLICATE [1] AND NUMBER OF REPLICATES THE CANDIDATE HAS TO BE DETECTED IN [2]
```

## 10. (Optional) DCC result check
* Sometimes some failures happen due to SCC problem, especially when the sample size is quite large. We provide self check script to fix this.
```
$ python /restricted/projectnb/ad-portal/DCC_protocol/check_DCC.py 
Enter the sample name: DC1 //sample name
Enter the first parameter: 2 // p1
Enter the second parameter: 2 // p2
Error: /restricted/projectnb/ad-portal/mtlin/DCC_rerun_2024Nov/test_selfCheck/Run/DCC/DC1_2_2_ver2_3/CircRNACount does not exist
/restricted/projectnb/ad-portal/mtlin/DCC_rerun_2024Nov/test_selfCheck/Run/DCC/DC1_2_2_ver2_3 failed
please run the following command to fix the jobs
bash DCC_fix/submit.sh
```

To fix the failure
```
bash DCC_fix/submit.sh
```
 
# DEV Notes
Genome: /restricted/projectnb/ad-portal/aknyshov/BU_ADRC_RiboM/DCC_ncRNAatlas_ref/DCC_protocol/Genome_index
/restricted/projectnb/amp-ad/aknyshov/ncRNAatlas/reference/GRCh38.p14.genome.fa
/restricted/projectnb/amp-ad/aknyshov/ncRNAatlas/reference/agat_combined.gff

This is a branch version of DCC protocol
I revised the following files in order to adapt new reference
1. Genome, and gtf file
2. DCC.py: 
    * line 54, /DCC-kit/GRCh38.primary_assembly.genome.fa -> /DCC-kit/GRCh38.p14.genome.fa
    * line 76, /DCC-kit/GRCh38.primary_assembly.genome.fa -> /DCC-kit/GRCh38.p14.genome.fa
    
3. module_DCC_paired.json
    * line 147, 
    ```
    "Setting": "\t\t-an ${gtf_dir}/gencode.v26.primary_assembly.annotation.gtf  ",
    ```
    ->
    ```
    "Setting": "\t\t-an ${gtf_dir}/agat_combined.gff ",
    ```
4. module_DCC_single.json
    * line 147, 
    ```
    "Setting": "\t\t-an ${gtf_dir}/gencode.v26.primary_assembly.annotation.gtf  ",
    ```
    ->
    ```
    "Setting": "\t\t-an ${gtf_dir}/agat_combined.gff ",
    ```