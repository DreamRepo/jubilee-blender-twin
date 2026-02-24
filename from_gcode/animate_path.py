

import bpy
import csv
import numpy as np

# Path to the CSV file (relative to the .blend file)
csv_path = bpy.path.abspath("//from_gcode/pathout.csv")

# Animate 'X-axis' in X, 'Y-axis' in Y, and 'Z-axis' in Z if present
x_axis = bpy.data.objects.get("X-axis")
y_axis = bpy.data.objects.get("Y-axis")
z_axis = bpy.data.objects.get("Z-axis")
if x_axis is None:
    raise Exception("No object named 'X-axis' in the scene!")
if y_axis is None:
    raise Exception("No object named 'Y-axis' in the scene!")

# Clean up existing actions/keyframes
for obj in [x_axis, y_axis, z_axis]:
    if obj is not None:
        obj.animation_data_clear()

# Read all points to determine minimums
points = []
with open(csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        points.append(tuple(map(float, row)))
points = np.array(points)

# Read all points
points = []
with open(csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        points.append(tuple(map(float, row)))
points = np.array(points)

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


x_min = get_axis_min(x_axis, 'X')
y_min = get_axis_min(y_axis, 'Y')
z_max = get_axis_max(z_axis, 'Z') if z_axis is not None else 0.0


# Move axes to minimum positions at start
x_axis.location.x = x_min
y_axis.location.y = y_min
if z_axis is not None:
    z_axis.location.z = z_max

print(f"Axis minimums: X={x_min}, Y={y_min}, Z={z_max}")



# Animate with shifted origin and spread keyframes
for frame, (x, y, z) in enumerate(points, start=1):
    keyframe = frame
    x_axis.location.x = x/1000 + x_min
    #print("X:", x_axis.location.x)
    x_axis.keyframe_insert(data_path="location", frame=keyframe)
    y_axis.location.y = y/1000 + y_min
    #print("Y:", y_axis.location.y)
    y_axis.keyframe_insert(data_path="location", frame=keyframe)
    if z_axis is not None:
        z_axis.location.z = z_max - z/1000
        #print("Z:", z_axis.location.z)
        z_axis.keyframe_insert(data_path="location", frame=keyframe)

    print(frame)

# Set scene end frame to match animation
scene = bpy.context.scene
scene.frame_end = len(points)