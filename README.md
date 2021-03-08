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

## Output

```

The output file is tab-delimited and has 9 columns:
chrom: Reference chromosome
pos: Reference position
ref: Reference sequence
alt: Alternate (variant) sequence
variant_type: Variant type composed of one or two items separated by ','. The first item comes 
    from the VCF file and is either snp, mnp, ins, del or complex. The optional 
    second item is a Sequence Ontology (SO) term that describes the consequence 
    of the variant, if the variant is in the ExAC database. If several SO terms 
    are possible, only the most severe one is reported.
seq_depth: Depth of sequence coverage at the site of variation
num_variant_reads: Number of reads supporting the variant
pct_variant_reads: Percentage of reads supporting the variant versus those 
    supporting the reference
exac_allele_freq: Allele frequency of variant from Broad Institute ExAC Project

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
