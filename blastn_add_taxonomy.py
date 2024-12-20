#!/usr/bin/env python
"""
blastn_add_taxonomy   V1.0    martenhoogeveen@naturalis.nl
This script adds the taxonomy to the BLAST output. The input is de folder path that contains the blast results.
"""
import json, sys, argparse, os, glob
from add_taxonomy_scripts.genbank import Genbank
from add_taxonomy_scripts.gbif import Gbif
from add_taxonomy_scripts.bold import Bold
from add_taxonomy_scripts.privatebold import PrivateBold
from add_taxonomy_scripts.unite import Unite
from add_taxonomy_scripts.silva import Silva
from add_taxonomy_scripts.generic import Generic
import sqlite3

# Retrieve the commandline arguments
parser = argparse.ArgumentParser(description='Add taxonomy to BLAST output')
parser.add_argument('-i', '--blast_input_folder', metavar='input folder with BLAST custom outfmt 6 output', dest='blastinputfolder', type=str,help='input folder', required=True)
parser.add_argument('-t', '--taxonomy_reference', metavar='taxonomy reference', dest='rankedlineage', type=str, required=False, nargs='?', default="taxonomy_reference.json")
parser.add_argument('-m', '--merged', metavar='merged taxonids', dest='merged', type=str, help='merged taxon id json', required=False, nargs='?', default="merged_taxonomy.json")
parser.add_argument('-ts', '--taxonomy_source', dest='taxonomy_source', type=str, required=False, nargs='?', default="default")
parser.add_argument('-o', '--output', metavar='output', dest='output', type=str, help='output file, BLAST hits with taxonomy', required=False, nargs='?', default="")
parser.add_argument('-taxonomy_db', dest='taxonomy_db', type=str, required=False)
args = parser.parse_args()

def add_taxonomy(file, genbank, bold, gbif, privatebold, unite, silva, generic):
    with open(file, "r") as blasthits, open(args.blastinputfolder.strip() + "/taxonomy_"+ os.path.basename(file), "a") as output, open(args.blastinputfolder.strip() + "/orginaltaxonomy_"+ os.path.basename(file), "a") as output2:
        for line in blasthits:
            if line.split("\t")[0] == "#Query ID":
                output.write(line.strip()+"\t#Source\t#Taxonomy\n")
                output2.write(line.strip() + "\t#Source\t#Taxonomy\n")
            else:
                if line.split("\t")[1].split("|")[0] == "BOLD":
                    line_taxonomy = bold.find_bold_taxonomy(line, "bold")
                elif line.split("\t")[1].split("|")[0] == "klasse":
                    line_taxonomy = bold.find_bold_taxonomy(line, "klasse")
                elif line.split("\t")[1].split("|")[0] == "private_BOLD":
                    line_taxonomy = privatebold.find_private_bold_taxonomy(line)
                elif line.split("\t")[1].split("|")[0] == "UNITE":
                    line_taxonomy = unite.find_unite_taxonomy(line)
                elif line.split("\t")[1].split("|")[0] == "silva":
                    line_taxonomy = silva.find_silva_taxonomy(line)
                elif line.split("\t")[1].split("|")[0].strip(">").isalpha():
                    line_taxonomy = generic.find_generic_taxonomy(line)
                else:
                    line_taxonomy = genbank.find_genbank_taxonomy(line)

                output2.write(line_taxonomy.strip()+"\n")
                if args.taxonomy_source == "GBIF":
                    line_taxonomy = gbif.find_gbif_taxonomy(line_taxonomy)
                    print(line_taxonomy)
                    output.write(line_taxonomy.strip()+"\n")
                elif args.taxonomy_source == "default":
                    print(line_taxonomy)
                    output.write(line_taxonomy.strip()+"\n")

def process_files():
    genbank = Genbank(args.rankedlineage, args.merged)
    bold = Bold()
    privatebold = PrivateBold()
    unite = Unite()
    silva = Silva()
    generic = Generic()
    if args.taxonomy_source == "GBIF":
        gbif = Gbif(args.taxonomy_db)
    else:
        gbif = ""
    files = [x for x in sorted(glob.glob(args.blastinputfolder.strip() + "/*.tabular"))]
    for file in files:
        add_taxonomy(file, genbank, bold, gbif, privatebold, unite, silva, generic)

def main():
    process_files()




if __name__ == "__main__":
    main()
