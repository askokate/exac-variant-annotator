"""Tests for vcf.py"""
import pytest
import vcf


def test_record_init():
    test_info = {
        'AF': '0',
        'AO': '95',
        'CIGAR': '1X',
        'DP': '4124',
        'RO': '4029',
        'TYPE': 'snp',
    }
    chrom = '1'
    pos = '931393'
    ref = 'G'
    alt = 'T'
    tmp_list = []
    for k, v in test_info.items():
        tmp_list.append(k + '=' + v)
    info_str = ';'.join(tmp_list)
    test_line = '\t'.join([
        chrom,
        pos,
        '.',
        ref,
        alt,
        '16866.7',
        '.',
        info_str,
    ])
    record = vcf.Record(test_line)
    assert chrom == record.CHROM
    assert pos == record.POS
    assert ref == record.REF
    assert alt == record.ALT
    assert test_info.items() == record.INFO.items()


def test_vcf_iter():
    test_vcf = vcf.VCF('testdata/small.vcf')
    rec1 = '19\t1220300\t.\tG\tA\t100\tPASS\tAN=25;DP=264\tAD\t243'
    rec2 = '19\t1220499\t.\tGGGG\tA\t100\tPASS\tAN=23;DP=374\tAD\t143'
    it1 = iter(test_vcf)
    assert it1.line == rec1
    assert next(it1).line == rec2
    with pytest.raises(StopIteration):
        next(it1)
