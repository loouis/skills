#!/usr/bin/env python3
"""Record supplied visual ratings and evidence; never infer beauty scores."""
import argparse
import hashlib
import json
import math
from pathlib import Path

RUBRIC = ['clear transmission', 'controlled contours and highlights', 'shape hierarchy',
          'reference feature compatibility', 'native cleanliness']


def evidence(path):
    resolved = path.expanduser().resolve(strict=True)
    return {'path': str(resolved), 'sha256': hashlib.sha256(resolved.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pass-id', required=True)
    parser.add_argument('--specimen', choices=['droplet', 'cavity', 'fold', 'contact'], required=True)
    parser.add_argument('--image', type=Path, required=True)
    parser.add_argument('--raw', type=Path, required=True)
    parser.add_argument('--reference', type=Path, action='append', required=True)
    parser.add_argument('--criteria', type=float, nargs=5, required=True)
    parser.add_argument('--defects', required=True)
    parser.add_argument('--comparison', required=True)
    parser.add_argument('--next-change', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        if any(not math.isfinite(v) or not 0 <= v <= 10 for v in args.criteria):
            raise ValueError('Five finite ratings from 0 to 10 are required')
        if any(not s.strip() for s in [args.defects, args.comparison, args.next_change, args.pass_id]):
            raise ValueError('Evidence notes must not be blank')
        output = args.output.expanduser().absolute()
        if output.exists() or output.is_symlink():
            raise ValueError('Score record exists; choose a fresh filename')
        if output.resolve().is_relative_to(Path(__file__).resolve().parents[1]):
            raise ValueError('Write new scores outside the skill')
        record = {'schema': 1, 'pass': args.pass_id, 'specimen': args.specimen,
                  'rubric': (['curved contact', 'natural local ripples', 'near-contact reflected warp', 'calm surroundings and sustained lower distortion', 'whole-shot water integration'] if args.specimen=='contact' else RUBRIC), 'criteria': args.criteria, 'score': round(sum(args.criteria) / 5, 2),
                  'scope': 'Subjective optical/contact still; not full reference reconstruction, motion or user approval',
                  'image': evidence(args.image), 'raw': evidence(args.raw),
                  'references': [evidence(p) for p in args.reference], 'defects': args.defects,
                  'reference_comparison': args.comparison, 'next_change': args.next_change,
                  'ratings_supplied_by_reviewer': True, 'technical_validation_is_separate': True}
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('x') as stream:
            stream.write(json.dumps(record, indent=2) + '\n')
        print(json.dumps({'record': str(output), 'score': record['score']}))
    except (ValueError, OSError) as error:
        parser.exit(2, str(error) + '\n')


if __name__ == '__main__':
    main()
