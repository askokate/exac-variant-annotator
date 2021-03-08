# annotate.py
Tool for annotating variants with annotations from ExAC database.

## Set up

A virtual environment called exac_va can then be created using the following command:

```

./create_conda_env.sh

conda activate exac_va

```

## Run


```
Usage: python3.7.1 main.py --in_vcf in.vcf --annotated_tsv out.tsv

arguments:
  --in_vcf              Path for input VCF file to be annotated. 
  --annotated_tsv       Path for output file with annotated variants. 
```
## Implementation 
Annotation tool groups input variants in groups of 400 and queries using bulk
endpoint of ExAC API. The tool improves the performance by also running queries
asynchronously since this execution is IO bound. For the large.vcf (~7000
variants) in testdata, this implementation takes 20s (large.vcf is the 
Challenge_data.vcf). Annotation results (annotated.tsv) for Challenge_data.vcf is in testdata
folder.

## Testing
To run unit tests run `python3.7.1 -m pytest`
