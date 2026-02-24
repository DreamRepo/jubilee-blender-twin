"""
path_follower.py
Adapted from: https://github.com/TanmayChhatbar/blender_3d_print_animation/blob/main/path_follower.py
Original author: Tanmay Chhatbar
"""
import sys
import numpy as np
from utils import *
from gcodedata import *

def parse_locs(lines):
    cur = [np.array([0.,0.,0.,0.])]
    for line in lines:
        # record all G0 and G1 moves
        if line.startswith("G0") or line.startswith("G1"):
            cur.append(find_coord(line, cur[-1]))
    return cur

def get_frame_locs(locs, dps):
    locs_frame = [locs[0][0:3]]
    pr_loc = locs[0]
    dslp = 0.0
    lenloc = len(locs)
    i = 1
    loc = locs[1]
    pr_loc = locs[0]
    while i <= lenloc:
        cdd = dis(loc[0:3], pr_loc[0:3])
        md = dps-dslp
        if cdd < md:
            dslp = dslp + cdd
            if i == lenloc-1:
                break
            else:
                i += 1
            pr_loc = loc
            loc = locs[i]
        else:
            nl = pr_loc[0:3] + (loc[0:3]-pr_loc[0:3])*md/cdd
            dslp = 0.0
            pr_loc = nl
            locs_frame.append(nl)
    return locs_frame

def main():
    if len(sys.argv) == 1:
        fn = 'path.gcode'
    else:
        fn = sys.argv[1]
    try:
        distance_per_step = float(sys.argv[2])
    except:
        distance_per_step = 100.0
    with open(fn, 'r') as f:
        locs = parse_locs(f.readlines())
        locs_frames = get_frame_locs(locs, distance_per_step)
    with open('pathout.csv','w') as f2:
        e = 1
        for loc in locs:
            if e != 1:
                f2.write('\n')
            f2.write(f"{loc[0]},{loc[1]},{loc[2]}")
            e += 1

if __name__ == "__main__":
    main()
