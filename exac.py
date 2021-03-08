#!/usr/bin/env python3.7.1
"""
Class and methods for ExAC database query runner.
"""

import json
import urllib
import warnings
import numpy as np

# ExAC API URL for bulk query
EXAC_URL = 'http://exac.hms.harvard.edu/rest/bulk/variant'


# Set of consequence terms, defined by the Sequence Ontology (SO), that can be
# currently assigned to each combination of an allele and a transcript are
# listed below. They are listed in order of severity (more severe to less
# severe) as estimated by Ensembl.
# Source:
# https://uswest.ensembl.org/info/genome/variation/prediction/predicted_data.html
ENSEMBL_SO_SEVERITY_ORDER = (
    'transcript_ablation',
    'splice_acceptor_variant',
    'splice_donor_variant',
    'stop_gained',
    'frameshift_variant',
    'stop_lost',
    'start_lost',
    'transcript_amplification',
    'inframe_insertion',
    'inframe_deletion',
    'missense_variant',
    'protein_altering_variant',
    'splice_region_variant',
    'incomplete_terminal_codon_variant',
    'start_retained_variant',
    'stop_retained_variant',
    'synonymous_variant',
    'initiator_codon_variant',
    'coding_sequence_variant',
    'mature_miRNA_variant',
    '5_prime_UTR_variant',
    '3_prime_UTR_variant',
    'non_coding_transcript_exon_variant',
    'intron_variant',
    'NMD_transcript_variant',
    'non_coding_transcript_variant',
    'upstream_gene_variant',
    'downstream_gene_variant',
    'TFBS_ablation',
    'TFBS_amplification',
    'TF_binding_site_variant',
    'regulatory_region_ablation',
    'regulatory_region_amplification',
    'feature_elongation',
    'regulatory_region_variant',
    'feature_truncation',
    'intergenic_variant'
)


def severity(so_term):
    """Get the severity ranking of an SO term.

    Args:
      so_term: Sequence Ontology term.

    Returns:
      Severity rank of SO term.

    """
    try:
        return ENSEMBL_SO_SEVERITY_ORDER.index(so_term)
    except ValueError:
        warnings.warn('Unexpected Sequence Ontology term: %s' % so_term)
        # If the SO term is not in ENSEMBL_SO_SEVERITY_ORDER, its severity
        # ranking is assumed to be +inf (least severe)
        return np.inf


def parse_bulk_response(bulk_response):
    """Parse ExAC API's response.

    Args:
      bulk_response: Response of a bulk query via ExAC API.

    Returns:
      A tuple of:
        1: variant id (chrom-pos-ref-alt).
        2: Allele frequency of variant from Broad Institute ExAC Project.
        3: Sequence Ontology (SO) term that describes consequence of variant.
    """
    wanted_info = []
    for variant in bulk_response:
        if 'allele_freq' in bulk_response[variant]['variant']:
            allele_freq = float(
                bulk_response[variant]['variant']['allele_freq'])
        else:
            allele_freq = np.nan
        d = bulk_response[variant]['consequence']
        consequence = min(d.keys(), key=severity) if d else ''
        wanted_info.append((variant, allele_freq, consequence))
    return wanted_info


async def fetch(data, session, url):
    """Fetch response from the url.

    Args:
      data: Data for post request.
      session: Session is a connection pool (connector instance).

    Returns:
      Response in json format.

    """
    try:
        response = await session.request(method='POST', url=url,
                                         data=eval(data))
        response.raise_for_status()
    except urllib.error.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error ocurred: {err}")
    return await response.json()


class ExAC(object):
    """Represents a ExAC query session.

    Attributes:
        session: Session is a connection pool (connector instance).
    """
    def __init__(self, session):
        self.session = session

    async def query(self, bulk_variants):
        """Wrapper for running ExAC API queries in an asynchronous manner.

        Args:
          bulk_variants: Group of variants separated by ','.
          session: Session is a connection pool (connector instance).

        Returns:
          Parsed response from ExAC API.

        """
        try:
            bulk_response = await fetch(bulk_variants, self.session, EXAC_URL)
            parsed_response = parse_bulk_response(bulk_response)
        except Exception as err:
            print(f"Exception occured: {err}")
            pass
        return parsed_response
