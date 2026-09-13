"""
KEGG ingestion placeholder script.
This script demonstrates how to use the KEGGAdapter for on-demand lookups and how an ingestion pipeline
could be structured. It does NOT perform bulk downloads and warns about KEGG licensing.
"""
from src.kegg_adapter import KEGGAdapter
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--ko', help='KO id to look up, e.g. K00001', required=False)
    p.add_argument('--gene', help='Gene id to look up, e.g. hsa:10458', required=False)
    args = p.parse_args()

    adapter = KEGGAdapter(rate_limit_per_minute=30)
    if args.ko:
        print('Looking up KO', args.ko)
        res = adapter.get_pathway_by_ko(args.ko)
        print(res.get('text','')[:1000])
    if args.gene:
        print('Looking up gene', args.gene)
        res = adapter.get_gene_info(args.gene)
        print(res.get('text','')[:1000])

    if not args.ko and not args.gene:
        print('No query specified. This is a placeholder demonstrating the KEGGAdapter usage.')
        print('Reminder: For bulk KEGG ingestion you must obtain the appropriate license from KEGG and adhere to their terms.')


if __name__ == '__main__':
    main()
