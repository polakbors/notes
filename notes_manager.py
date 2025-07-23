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
parser.add_argument("--txtin", type=str, default="", help="puts text in the note")
parser.add_argument("--sizex", type=int, default=300, help="X position of the note")
parser.add_argument("--sizey", type=int, default=300, help="Y position of the note")
parser.add_argument("--fontsize", type=int, default=12, help="Font size of the note")
parser.add_argument("--resize", action="store_true", help="This flag is used to enable note resizing")
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
    print("hello")
    subprocess.run( f'echo "name:{args.name} color:{args.color} fontcolour:{args.fontcolour} sizex:{args.sizex} sizey:{args.sizey} fontsize:{args.fontsize} " >> conf.txt', shell=True, check=True)

if  args.bringup:
    with open("conf.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split()
            print(parts)
            args.name = parts[0].split(":")[1]
            args.color = parts[1].split(":")[1]
            args.fontcolour = parts[2].split(":")[1]
            args.sizex = int(parts[3].split(":")[1])
            args.sizey = int(parts[4].split(":")[1])
            args.fontsize = int(parts[5].split(":")[1])
            note_file_path = os.path.join('.', args.name)
            if os.path.exists(note_file_path):
                with open(note_file_path, "r") as note_file:
                    args.txtin = note_file.read()
            else:
                args.txtin = ""            
            print(f"Bringing up note with name: {args.name}, color: {args.color}, fontcolour: {args.fontcolour} sizex: {args.sizex} sizey: {args.sizey} fontsize: {args.fontsize}")
            cmd= [
                "python3", "notes.py",
                "--name", args.name,
                "--color", args.color,
                "--fontcolour", args.fontcolour,
                "--sizex", str(args.sizex),
                "--sizey", str(args.sizey),
                "--fontsize", str(args.fontsize),
                "--txtin", args.txtin
            ]
            subprocess.Popen(cmd,start_new_session=True)
else:
    subprocess.Popen(cmd,start_new_session=True)


# This flag is used to bring up the note if it already exists

# Launch as subprocess (non-blocking)
##TODO  -> if file is empty file gets deleted -> -> resizing, maybe location -> implement stickiness
