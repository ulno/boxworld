

from boxworld.FrameFileJoiner import FrameFileJoiner
import sys

timestep = int(sys.argv[1])
fileNames = sys.argv[2:]
files = [open(n, "r") for n in fileNames]

joiner = FrameFileJoiner(files)

print joiner.getFrameAsVTK(timestep)

exit(0)