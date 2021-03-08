"""Tests for variant.py"""
import pytest
import variant


def test_variant():
    var1 = variant.Variant('1', '10', 'G', 'T')
    var1.annotate_from_vcf('snp', '20', '10', '0.5')
    var1.annotate_from_exac('stop_gained', '0.9')
    var1_str = '1\t10\tG\tT\tsnp, stop_gained\t20\t10\t0.5\t0.9'
    var2 = variant.Variant('1', '20', 'CTGTGTGTGTGT', 'CTGTGTGTGT')
    var2.annotate_from_vcf("del", '30', '15', '0.5')
    var2.annotate_from_exac('', '0.8')
    var2_str = '1\t20\tCTGTGTGTGTGT\tCTGTGTGTGT\tdel\t30\t15\t0.5\t0.8'
    assert str(var1) == var1_str
    assert str(var2) == var2_str
