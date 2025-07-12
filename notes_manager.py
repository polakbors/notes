import notes
import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--title", type=str, default="Note from Manager")
args = parser.parse_args()

# Build command
cmd = [
    "python3", "notes.py",
    "--title", args.title,
]

# Launch as subprocess (non-blocking)
subprocess.Popen(cmd)
