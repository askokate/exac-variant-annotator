#!/usr/bin/env python3.7.1
"""
Classes for representing vcf file
---------------------------------------------------------------------------
Module Contents
~~~~~~~~~~~~~~~
The module contains the following public classes:
    - :class:`~vcf.Record` -- container class for a variant record in vcf file.
    - :class:`~vcf.VCF` -- container class for a vcf file.
"""

import sys
import os


class Record(object):
    """Record represents information for each variant in vcf file.

    Attributes:
        CHROM: Name of the chromosome.
        POS: Position on the chromosome.
        REF: Reference allele.
        ALT: Variant alleles.
        INFO: Dictionary with various vcf tags as keys and their values.
    """

    def __init__(self, line):
        """Inits Record with a line from vcf file."""
        self.line = line
        info = line.split("\t")
        self.CHROM = info[0]
        self.POS = info[1]
        self.REF = info[3]
        self.ALT = info[4]
        self.INFO = dict()
        for pair_lst in [pair.split("=") for pair in info[7].split(";")]:
            if len(pair_lst) > 1:
                self.INFO[pair_lst[0]] = pair_lst[1]
            else:
                self.INFO[pair_lst[0]] = ""


class VCF(object):
    """VCF represents a vcf file.

    Attributes:
        reader: vcf file reader.
        line: Current line from vcf file.
        record: Current variant from vcf file.
    """
    def __init__(self, uncompressed_vcf):
        """Inits VCF with an uncompressed vcf file."""
        self.reader = open(uncompressed_vcf, 'r')
        self.line = self.reader.readline().strip()
        while self.line.startswith('#'):
            self.line = self.reader.readline().strip()
        self.record = Record(self.line)

    def __iter__(self):
        return self

    def __next__(self):
        """Returns next variant record in vcf file"""
        self.line = self.reader.readline().strip()
        if self.line != "":
            self.record = Record(self.line)
            return self.record
        else:
            self.reader.close()
            raise StopIteration()
