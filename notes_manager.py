import notes
import subprocess
import argparse
import sys,os
from datetime import datetime

now = datetime.now()
parser = argparse.ArgumentParser()
parser.add_argument("--name", type=str, default=f"Untitled{now.strftime("%Y-%m-%d %H:%M:%S.%f")}", help="Path to the note file")
parser.add_argument("--color", type=str, default="#fff9a0", help="choose color of your note  default=#fff9a0")
parser.add_argument("--fontcolour", type=str, default="#000000", help="[British accent] Colour of the font default=#000000")
parser.add_argument("--pernament", action="store_true", help="This flag is used to save the content of the note permanently")
parser.add_argument("--bringup", action="store_true", help="This flag is used to bring up the note if it already exists , this flag doesnt create a new note")

#parser.add_argument("--sticky", default=True, help="sticks")


args = parser.parse_args()
if os.path.exists(f"/tmp/{args.name}") and not args.pernament:
    args.name=f"{args.name} {now.strftime("%Y-%m-%d %H:%M:%S.%f")}"

cmd = [
    "python3", "notes.py",
    "--name", args.name,
    "--color", args.color,
    "--fontcolour", args.fontcolour,

]
if args.pernament:
    cmd.append("--pernament")
    filename = f"{args.name}"  # Assuming the file name is derived from the arg
    file_path = os.path.join('.', filename)
    print(f"File path: {file_path}")
    if os.path.exists(file_path):
        print("File with that name already exists. Choose non-pernament option or change the name.")
        sys.exit(1)
    subprocess.run( f'echo "name:{args.name} color:{args.color} fontcolour:{args.fontcolour}" >> conf.txt', shell=True, check=True)

if  args.bringup:
    with open("conf.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            print(parts)
            args.name = parts[0].split(":")[1]
            args.color = parts[1].split(":")[1]
            args.fontcolour = parts[2].split(":")[1]
            print(f"Bringing up note with name: {args.name}, color: {args.color}, fontcolour: {args.fontcolour}")
            cmd= [
                "python3", "notes.py",
                "--name", args.name,
                "--color", args.color,
                "--fontcolour", args.fontcolour,
            ]
            subprocess.Popen(cmd,start_new_session=True)
else:
    subprocess.Popen(cmd,start_new_session=True)


# This flag is used to bring up the note if it already exists

# Launch as subprocess (non-blocking)
##TODO  -> choose nice icon  ->  if there are files in the dir they should be used  -> if file is empty file gets deleted ->add state of notes , maybe location , implement stickinesss
