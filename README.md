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