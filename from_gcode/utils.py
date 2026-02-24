"""
helper functions for path_follower
Adapted from: https://github.com/TanmayChhatbar/blender_3d_print_animation/blob/main/utils.py
Original author: Tanmay Chhatbar
"""
from math import sqrt
import numpy as np

def _extract_numeric_after(token: str) -> float | None:
    token = token.split(";", 1)[0]
    parts = [p for p in token.strip().split() if p]
    if not parts:
        return None
    try:
        return float(parts[0])
    except ValueError:
        return None

def find_coord(line, curcoord):
    nl = curcoord.copy()
    checks = ["X", "Y", "Z", "F"]
    for i, axis in enumerate(checks):
        if axis in line:
            after = line.split(axis, 1)[1]
            val = _extract_numeric_after(after)
            if val is not None:
                nl[i] = val
    return nl

def dis(loc1, loc2):
    return sqrt(sum((np.array(loc1)-np.array(loc2))[0:3]**2))


# Get axis minimums from Blender constraints
def get_axis_min(obj, axis):
    for constraint in obj.constraints:
        if constraint.type == 'LIMIT_LOCATION':
            if axis == 'X':
                return constraint.min_x if constraint.use_min_x else 0.0
            elif axis == 'Y':
                return constraint.min_y if constraint.use_min_y else 0.0
            elif axis == 'Z':
                return constraint.min_z if constraint.use_min_z else 0.0
    return 0.0

# Get axis minimums from Blender constraints
def get_axis_max(obj, axis):
    for constraint in obj.constraints:
        if constraint.type == 'LIMIT_LOCATION':
            if axis == 'X':
                return constraint.max_x if constraint.use_max_x else 0.0
            elif axis == 'Y':
                return constraint.max_y if constraint.use_max_y else 0.0
            elif axis == 'Z':
                return constraint.max_z if constraint.use_max_z else 0.0
    return 0.0