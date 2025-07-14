import notes
import subprocess
import argparse
import sys,os

parser = argparse.ArgumentParser()
parser.add_argument("--name", type=str, default="Untitled", help="Path to the note file")
parser.add_argument("--color", type=str, default="#fff9a0", help="choose color of your note  default=#fff9a0")
parser.add_argument("--fontcolour", type=str, default="#000000", help="[British accent] Colour of the font default=#000000")
parser.add_argument("--pernament", action="store_true", help="This flag is used to save the content of the note permanently")
#parser.add_argument("--sticky", default=True, help="sticks")


args = parser.parse_args()

cmd = [
    "python3", "notes.py",
    "--name", args.name,
    "--color", args.color,
    "--fontcolour", args.fontcolour,
    "--pernament", args.pernament,

]
if args.pernament:
    filename = f"{args.pernament}.txt"  # Assuming the file name is derived from the arg
    file_path = os.path.join('.', filename)

    if os.path.exists(file_path):
        print("File with that name already exists. Choose non-pernament option or change the name.")
        sys.exit(1)
        
# Launch as subprocess (non-blocking)
subprocess.Popen(cmd,start_new_session=True)
##TODO add logic for tmp and pernanment files ->add state of notes , maybe location , implement stickinesss 
