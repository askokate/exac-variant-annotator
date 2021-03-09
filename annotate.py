#!/usr/bin/env python3.7.1
"""Python script for annotating VCF files.

The output file is tab-delimited and each variant will be annotated with the
following pieces of information output:
1. Type of variation and their effect. Multiple effects are annotated with the
most deleterious possibility
2. Depth of sequence coverage at the site of variation
3. Number of reads supporting the variant
4. Percentage of reads supporting the variant versus those supporting reference
5. Allele frequency of variant from ExAC API

  Usage: python annotate.py --in_vcf in.vcf --annotated_tsv out.tsv

"""

import argparse
import vcf
import aiohttp
import asyncio
import variant
import exac


async def async_annotate(bulk_variants_list):
    """Wrapper for annotating bulk variants list in an asynchronous manner .

    Args:
      bulk_variants_list: List of grouped variants to be annotated.

    Returns:
      Annotation results from ExAC API.

    """
    async with aiohttp.ClientSession() as session:
        runner = exac.ExAC(session)
        results = await asyncio.gather(*[runner.query(v)
                                         for v in bulk_variants_list])
    return results


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_vcf', required=True, type=str,
                        help='Input vcf')
    parser.add_argument('--annotated_tsv', required=True, type=str,
                        help='Output vcf file')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    in_vcf = vcf.VCF(args.in_vcf)
    variants = dict()
    # Parse input vcf file
    for record in in_vcf:
        alts = record.ALT.split(',')
        types = record.INFO['TYPE'].split(',')
        aos = list(map(int, record.INFO['AO'].split(',')))
        for i, alt in enumerate(alts):
            var = variant.Variant(record.CHROM, record.POS, record.REF, alt)
            ro = float(record.INFO['RO'])
            pct = aos[i] / (ro + aos[i])
            var.annotate_from_vcf(
                types[i],
                str(record.INFO['DP']),
                str(aos[i]),
                '%#.4G' % pct,
            )
            variants[var.identifier()] = var

    # Group variants together in batches of 400 (ExAC API limit)
    bulk_variants_list = []
    ids = [r'\"' + vid + r'\"' for vid in list(variants.keys())]
    for i in range(0, len(ids), 400):
        bulk_variants = r'"[' + ",".join(ids[i:i+400]) + r']"'
        bulk_variants_list.append(bulk_variants)

    # Annotate variants asynchronously
    loop = asyncio.get_event_loop()
    all_results = loop.run_until_complete(async_annotate(bulk_variants_list))

    # Write the annotations in output tsv file
    out_fh = open(args.annotated_tsv, 'w')
    header = '\t'.join(variant.ANNOTATION_HEADER)
    out_fh.write(f'{header}\n')
    for bulk_results in all_results:
        for result in bulk_results:
            var = variants[result[0]]
            var.annotate_from_exac(result[2], '%#.4G' % result[1])
            out_fh.write(f'{var}\n')


if __name__ == '__main__':
    main()
