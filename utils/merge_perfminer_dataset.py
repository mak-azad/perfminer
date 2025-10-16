#!/usr/bin/env python3
"""
Usage:
  python3 merge_by_context_sharded.py <input_dir> [--shard-gib N]

Example:
  python3 merge_by_context_sharded.py /nfs/results_cpp --shard-gib 2

Creates:
  /nfs/zipped/ctx1.part0001.jsonl.gz, ctx1.part0002.jsonl.gz, ...
  /nfs/zipped/ctx0.part0001.jsonl.gz, ctx0.part0002.jsonl.gz, ...
"""

import sys, json, gzip, argparse
from pathlib import Path

def gz_writer(path: Path):
    # text-mode gzip writer
    return gzip.open(path, "wt", encoding="utf-8")

class ShardedWriter:
    def __init__(self, prefix: Path, shard_bytes: int):
        self.prefix = prefix
        self.shard_bytes = shard_bytes
        self.idx = 0
        self.w = None
        self.bytes = 0  # bytes written in current shard (approx)
        self._open_next()

    def _open_next(self):
        if self.w:
            self.w.close()
        self.idx += 1
        name = f"{self.prefix}.part{self.idx:04d}.jsonl.gz"
        self.cur_path = Path(name)
        self.w = gz_writer(self.cur_path)
        self.bytes = 0

    def write_jsonl(self, obj):
        s = json.dumps(obj, ensure_ascii=False)
        self.w.write(s + "\n")
        self.bytes += len(s.encode("utf-8")) + 1
        if self.bytes >= self.shard_bytes:
            self._open_next()

    def close(self):
        if self.w:
            self.w.close()
            self.w = None

def iter_jsonl_files_once(root: Path):
    # Snapshot .jsonl files present at start (non-recursive)
    return sorted([p for p in root.glob("*.jsonl") if p.is_file()])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir", type=Path)
    ap.add_argument("--shard-gib", type=float, default=2.0,
                    help="Max uncompressed bytes per shard (GiB). Default: 2.0 GiB")
    args = ap.parse_args()

    input_dir = args.input_dir
    output_dir = Path("/nfs/zipped")
    output_dir.mkdir(parents=True, exist_ok=True)

    ctx1_prefix = output_dir / "ctx1"
    ctx0_prefix = output_dir / "ctx0"

    if not input_dir.is_dir():
        print(f"Error: {input_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    shard_bytes = int(args.shard_gib * (1024**3))
    files = iter_jsonl_files_once(input_dir)
    print(f"Found {len(files)} JSONL files in {input_dir}")

    w1 = ShardedWriter(ctx1_prefix, shard_bytes)
    w0 = ShardedWriter(ctx0_prefix, shard_bytes)

    skipped = 0
    for i, fp in enumerate(files, start=1):
        print(f"[{i}/{len(files)}] Processing: {fp.name}")
        with fp.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    skipped += 1
                    continue
                flag = obj.get("context_flag", None)
                if flag == 1:
                    w1.write_jsonl(obj)
                elif flag == 0:
                    w0.write_jsonl(obj)
                else:
                    skipped += 1

    w1.close()
    w0.close()

    if skipped:
        print(f"Skipped {skipped} lines without a valid context_flag or malformed JSON.", file=sys.stderr)

if __name__ == "__main__":
    main()
