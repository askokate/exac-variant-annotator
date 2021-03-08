#!/usr/bin/env python3.7.1
"""
Class for representing a variant and it's annotations.
"""

# Header for output annotation file
ANNOTATION_HEADER = [
    'chrom',
    'pos',
    'ref',
    'alt',
    'variant_type',
    'seq_depth',
    'num_variant_reads',
    'pct_variant_reads',
    'exac_allele_freq',
]


class Variant(object):
    """Represents a variant in the annotator.

    Attributes:
        chrom: Name of the chromosome.
        pos: Position on the chromosome.
        ref: Reference allele.
        alt: Variant alleles.
    """
    def __init__(self, chrom, pos, ref, alt):
        """Creates a variant object."""
        self.chrom = chrom
        self.pos = pos
        self.ref = ref
        self.alt = alt
        # annotations later assigned from vcf file
        self.variant_type = ""
        self.cov_depth = ""
        self.num_reads = ""
        self.reads_perc = ""
        # annotations later assigned from exac
        self.consequence = ""
        self.allele_freq = ""

    def __repr__(self):
        annot_type = ('%s, %s' % (self.variant_type, self.consequence)
                      if self.consequence else self.variant_type)
        vid = self.identifier().replace('-', '\t')
        return f'{vid}\t{annot_type}\t{self.cov_depth}\t{self.num_reads}\t{self.reads_perc}\t{self.allele_freq}'

    def identifier(self):
        """Generates an identifier (key) for variant in string format."""
        return "-".join((self.chrom, self.pos, self.ref, self.alt))

    def annotate_from_vcf(self, variant_type, cov_depth, num_reads,
                          reads_perc):
        """Annotate with values fetched from a vcf file.

        Args:
            variant_type: Either snp, mnp, ins, del or complex.
            cov_depth: Depth of sequence coverage at the site of variation.
            num_reads: Number of reads supporting the variant.
            reads_perc: Percentage of reads supporting the variant versus
                those supporting the reference.
        """
        self.variant_type = variant_type
        self.cov_depth = cov_depth
        self.num_reads = num_reads
        self.reads_perc = reads_perc

    def annotate_from_exac(self, consequence, allele_freq):
        """Annotate with values fetched from ExAC database.

        Args:
            consequence: Sequence Ontology (SO) term that describes the
                consequence of the variant, if the variant is in the ExAC
                database.
            allele_freq: Allele frequency of variant from Broad Institute ExAC
        """
        self.consequence = consequence
        self.allele_freq = allele_freq
