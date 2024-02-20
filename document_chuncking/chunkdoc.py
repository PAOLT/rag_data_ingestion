from tqdm import tqdm
import os
import json 
import glob
from pathlib import Path 
from adi_chunker import adi_chunker
from txt_chunker import txt_chunker
import argparse

def chunk_file(path: str, method: str, params):
    if method in ['adi_par', 'adi_md']:
        return adi_chunker(path, method)
    elif method == 'txt':
        return txt_chunker(path, **params)
    else:
        ValueError("Unknown method: {method}")

methods={}
methods['adi_par']="uses Document Intelligence to identify document paragraphs and split on headers"
methods['adi_md']="uses Document Intelligence to convert the document to markdown and split on headers"
methods['txt']="uses python to extract document to plain text"

parser = argparse.ArgumentParser(description="A simple argparse example.")

parser.add_argument('--source_dir', type=str, required=True, help='Input directory')
parser.add_argument('--out_dir', type=str, required=True, help='Output directory')
parser.add_argument('--method', type=str, choices=list(methods.keys()), default='adi_par', help=str(methods))
parser.add_argument('--extension', type=str, default='pdf', help='File type')

args, unknown = parser.parse_known_args()
params = {unknown[i].lstrip('-'): unknown[i + 1] for i in range(0, len(unknown), 2)}

assert Path(args.source_dir).exists()
os.makedirs(args.out_dir, exist_ok=True)

pattern = os.path.join(args.source_dir, f"*.{args.extension}")

for f in tqdm(glob.glob(pattern, recursive=False)):
    sub_documents = chunk_file(f, args.method, params)
    json_path = os.path.join(args.out_dir, f"{Path(f).stem}.json")
    with open(json_path, 'w') as f:
        for d in sub_documents:
            json.dump(d, f)
            f.write('\n')
