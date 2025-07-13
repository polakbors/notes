import notes
import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--name", type=str, default="Note from Manager", help="Path to the note file")
parser.add_argument("--color", type=str, default="#fff9a0", help="choose color of your note  default=#fff9a0")
parser.add_argument("--fontcolour", type=str, default="#000000", help="[British accent] Colour of the font default=#000000")

#parser.add_argument("--sticky", default=True, help="sticks")


args = parser.parse_args()

cmd = [
    "python3", "notes.py",
    "--name", args.name,
    "--color", args.color,
    "--fontcolour", args.fontcolour,

]

# Launch as subprocess (non-blocking)
subprocess.Popen(cmd,start_new_session=True)
##TODO add logic for tmp and pernanment files ->add state of notes , maybe location , implement stickinesss 
