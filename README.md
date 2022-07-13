# DCC_protocol
It is a DCC_protocol for SCC in BU
If you want to use it without install, please contact Mintao Lin or XiaoLing to acquire the access to https://scc-ondemand1.bu.edu/pun/sys/files/fs/restricted/projectnb/ncrna/

The protocol is built based on python and STAR alignment algorithm


The manual with figures and details is availiable on https://drive.google.com/file/d/1xSAiqQcKFtrHVmI4W-nmSrejrLLqqk84/view?usp=sharing



-------------------------------------------------------------------------------------------------------------------------

Version 0.3

DCC pipeline

On BU SCC

Xiaoling’s Lab
2022-3-14
Mintao Lin
E-mail: minty@bu.edu
 
Preface
1.Environment Setting	2
1.1 DCC-kit	2
1.2 Setting for developers	2
2. How to use it	3
2.1 Preparation	3
2.2 Start from an SRA table	4
2.3 Start from fastq files	9
2.4 Start from fastq.gz files	14










1.Environment Setting
1.1 DCC-kit
DCC-kit is an All-in-one integration package, containing all gene references and programs that the pipeline needs.
Download: Bash cp -r /restricted/projectnb/ncrna/DCC_protocol .
It is highly recommended. More instructions are available in part 2.1


1.2 Setting for developers
All setting could be modified directly json files in bash_files.
 
Those json files are readable and editable. 
 
Parameter ‘Setting’ refers to a specific path or setting;
Parameter ‘Hidden’ shows the preference whether the setting should be modified. Try not to revise it please.
Parameter ‘withslash’ combines the setting with the next setting. It is the guideline for generating qsub files.
Parameter ‘silent’ is a redundant parameter for further developing needs.



2. How to use it
2.1 Preparation 
2.1.1 Installation
(1)A preferred way: install all-in-one package
Find a new directory you want to install the program
Bash cp -r /restricted/projectnb/ncrna/DCC_protocol .
You do not have to install it if you are in BU SCC and have the permission to get into the ncrna file. The permission could be acquired by E-mail to minty@bu.edu 

(2)For developers
If you don’t want to install the DCC-kit
Bash git clone https://github.com/90yearsoldcoder/DCC_protocol.git
Then build the DCC-kit by your own.

In this guideline,
We assumed the program has been download and installed at 
/restricted/projectnb/casa/mtLin/DCC_protocol/DCC_protocol/
	Please don’t submit tasks to SCC during using this pipeline. It would be fixed in future release.

2.1.2 Build Star genome index
It is unnecessary to build genome index if you use the all-in-one package.
If you want to build your own genome index, follow the instruction below.
Star alignment needs a suffix array as genome index. You could generate the index manually or use our python script. No matter which way you choose, the index SA file should be in path/to/DCC_protocol/Genome_index/GrCh38_100n/
We highly recommend you to use our python script and DCC-kit to do this.
To be specific:
Bash python /path/to/DCC_pipeline/buildSA.py
Here, since our program is installed in /restricted/projectnb/casa/mtLin/DCC_protocol/DCC_protocol/, 
we should bash python /restricted/projectnb/casa/mtLin/DCC_protocol/DCC_protocol/buildSA.py
 
Please, make sure this task is completed before starting the steps below.
It is unnecessary to generate the index every time you use the pipeline. Once the index files are generated, the files are good enough for any other jobs using this pipeline.

After generating the suffix array, you should modify the script in star.py
 
Change those two lines into  self.pro_path+"/Genome_index/GrCh38_100n" 
2.2 Start from an SRA table
2.2.1 Download SRR files
(1) In a blank working folder, upload the SRA table.
	 
(2) Open the terminal shell and cd to this working folder. Start the python program.
Bash python /path/to/DCC_pipeline/start.py 
Here, since our program is installed in /restricted/projectnb/casa/mtLin/DCC_protocol/DCC_protocol/, we should bash python /restricted/projectnb/casa/mtLin/DCC_protocol/DCC_protocol/start.py
 

(3) Type in your SCC username, and you will see the step you have finished.
 

(4) Type in ‘1’ to start your DCC-pipe. Also, you could delete the previous record of DCC-pipeline running in this folder.

(5) Specify the SRAtable you want to use.
 
Here, since the name of our SRAtable is SraRunTable.txt, we type in SraRunTable.txt
 

(6) Specify what Samples we need
In most cases, we don’t need all cell samples in the Sratable, so it is very necessary to filter out what we need.
Now, let’s have a brief look at the data, type in 1 (If you already know what you need, you could omit it):
 
If you want to know all columns’ names here, type in 2. (Not necessary)
 

If you want to know the specific values in a column, type in 3. (Not necessary)
For example, I am wondering what cell types the table have.
 
Obviously, there is only one cell type which is ES cell, but in most cases there are lots of kinds of cell types.

After you decide the key word used for filtering, type in 4.
Here, we only need ES cells for further DCC, so we type in 4, Cell_type, ES cell
 

Please type in ‘y’ to save the list and using it for later downloading.
 
(7) Downloading SRA documents
Type in ‘5’ and ‘y’ to download them
 
Downloading might take some time.
When you see this, you can leave or quit the program. 
The program will make sure you have finished all tasks before allowing you to start the next step.

2.2.2 Convert SRA file to fastq.gz files
You could come back to the pipeline any time you want, using 
python /path/to/DCC_pipeline/start.py  in your working directory.
Here, we bash 
python /restricted/projectnb/casa/mtLin/DCC_protocol/DCC_protocol/start.py
to continue our pipeline.
 
Then type in 1 to convert SRA file to fastqgz.
 
Then, wait or quit the program as we did before.

2.2.3 Star alignment
Type in 1 to do this part. Paired-end or double-end is selected automatically.

 
Wait or quit it as we did before.

2.2.4 Generate merge_tables
Merge_tables are several tables containing the path to Star results. It will be used for DCC process.
Type in 1 to do this part.

2.2.5 DCC 
Type in 1 to move to the DCC step, and type in the parameter 1 and parameter 2.
The detail of parameter 1 and parameter 2 could be found at https://github.com/dieterich-lab/DCC.

The two parameters refer to the Nr setting in DCC program:
-NR 5 6 \ MINIMUM COUNT IN ONE REPLICATE [1] AND NUMBER OF REPLICATES THE CANDIDATE HAS TO BE DETECTED IN [2]
 
When the task is running, you could quit the program any time you want.


If you want to have the result with different parameter settings
Type in 1 and set a different parameter setting. They could be calculated at the same time.
 

All DCC results could be found in ./Run/DCC/<key_word>/<key_word_p1_p2>
In this example, results are in DCCtest_path/Run/DCC/ES_cell/
 





2.3 Start from fastq files
2.3.1 Prepare your fastq files
All fastq files should be in only one fold. 
If they are paired_end samples, their names should be like ‘<samplename>_1.fastq’ and ‘<samplename>_2.fastq’
If they are single_end samples, their names should be like ‘<samplename>_1.fastq’ 
Example:
 
There could be some unrelated files, like ‘fastqgz’ and ‘log_e’ files in the example. Only fastq files are regarded as our working files.

2.3.2 Start the pipeline
Choosing a new directory as your working directory.
Then bash python /path/to/DCC_protocol/start_fastq.py
Here, our program is installed in /restricted/projectnb/casa/mtLin/DCC_protocol/DCC_protocol/
(as we mentioned in 2.1.1)
So we bash python /restricted/projectnb/casa/mtLin/DCC_protocol/DCC_protocol/start_fastq.py
 

2.3.2 Copy fastqfiles to working directory
In most cases, we don’t want to do any operation on your original files, so we copy them to the working directory.
What you should do is just pressing 1 in the program.
 
Then, it will ask you the path to your original fastq files, and the name of those samples.
The name could be your cells’ name or indicates who gives you the samples balabala.
In our example, I call it ‘ESfastq’, which is nonsense.
After that, it will double check you choose those samples. You could press y to continue.

When your tasks are submitted, you could quit the program and come back later.
 
When you see this, you can leave or quit the program. 
The program will make sure you have finished all tasks before allowing you to start the next step.
It is a better choice to check the situation of tasks using ‘watch qstat -u <username>’

Any time you want to come back and continue, use bash python /path/to/DCC_protocol/start_fastq.py

2.3.3 Convert them into fastqgz files
Using bash python /path/to/DCC_protocol/start_fastq.py, to come back to the program.
Then press 1 to do this step.

 
Same, you could leave the program when the program indicates those tasks are submitted.


Other steps below are exactly same with 2.2.3 – 2.2.5
2.3.4 Star alignment
Type in 1 to do this part. Paired-end or double-end is selected automatically.

 
Wait or quit it as we did before.

2.3.4 Generate merge_tables
Merge_tables are several tables containing the path to Star results. It will be used for DCC process.
Type in 1 to do this part.

2.3.5 DCC 
Type in 1 to move to the DCC step, and type in the parameter 1 and parameter 2.
The detail of parameter 1 and parameter 2 could be found at https://github.com/dieterich-lab/DCC.

The two parameters refer to the Nr setting in DCC program:
-NR 5 6 \ MINIMUM COUNT IN ONE REPLICATE [1] AND NUMBER OF REPLICATES THE CANDIDATE HAS TO BE DETECTED IN [2]
 
When the task is running, you could quit the program any time you want.


If you want to have the result with different parameter settings
Type in 1 and set a different parameter setting. They could be calculated at the same time.
 

All DCC results could be found in ./Run/DCC/<key_word>/<key_word_p1_p2>
In this example, results are in DCCtest_path/Run/DCC/ESfastq/
 

2.4 Start from fastq.gz files
Starting from fastq.gz files is very similar to part 2.3
2.4.1 Prepare your fastq.gz files
All fastq.gz files should be in only one fold. 
If they are paired_end samples, their names should be like ‘<samplename>_1.fastq.gz’ and ‘<samplename>_2.fastq.gz’
If they are single_end samples, their names should be like ‘<samplename>_1.fastq.gz’ 
Example:
 

2.4.2 Start the pipeline
Choosing a new directory as your working directory.
Then bash python /path/to/DCC_protocol/start_fastqgz.py
Here, our program is installed in /restricted/projectnb/casa/mtLin/DCC_protocol/DCC_protocol/
(as we mentioned in 2.1.1)
So we bash python /restricted/projectnb/casa/mtLin/DCC_protocol/DCC_protocol/start_fastqgz.py


 

2.4.2 Copy fastq.gz files to working directory
In most cases, we don’t want to do any operation on your original files, so we copy them to the working directory.
What you should do is just pressing 1 in the program.
 
Then, it will ask you the path to your original fastq.gz files, and the name of those samples.
The name could be your cells’ name or indicates who gives you the samples balabala.
In our example, I call it ‘ESfastqgz’, which is nonsense.
After that, it will double check you choose those samples. You could press y to continue.

When your tasks are submitted, you could quit the program and come back later.
 
When you see this, you can leave or quit the program. 
The program will make sure you have finished all tasks before allowing you to start the next step.
It is a better choice to check the situation of tasks using ‘watch qstat -u <username>’

Any time you want to come back and continue, use bash python /path/to/DCC_protocol/start_fastq.py
Other steps below are exactly same with 2.2.3 – 2.2.5
2.4.3 Star alignment
Type in 1 to do this part. Paired-end or double-end is selected automatically.

 
Wait or quit it as we did before.

2.4.4 Generate merge_tables
Merge_tables are several tables containing the path to Star results. It will be used for DCC process.
Type in 1 to do this part.

2.4.5 DCC 
Type in 1 to move to the DCC step, and type in the parameter 1 and parameter 2.
The detail of parameter 1 and parameter 2 could be found at https://github.com/dieterich-lab/DCC.

The two parameters refer to the Nr setting in DCC program:
-NR 5 6 \ MINIMUM COUNT IN ONE REPLICATE [1] AND NUMBER OF REPLICATES THE CANDIDATE HAS TO BE DETECTED IN [2]
 
When the task is running, you could quit the program any time you want.


If you want to have the result with different parameter settings
Type in 1 and set a different parameter setting. They could be calculated at the same time.
 

All DCC results could be found in ./Run/DCC/<key_word>/<key_word_p1_p2>
In this example, results are in DCCtest_path/Run/DCC/ESfastqgz/
 

