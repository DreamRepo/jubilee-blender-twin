import bpy

# -------------------------------------------------------------------
# CONFIG — change names here if your empties use different names
# -------------------------------------------------------------------
# In the current jubilee.blend, the Y axis object is named "Y-axis"
Y_GANTRY_NAME = "Y-axis"
X_AXIS_NAME = "X-axis"
XY_CARRIAGE_NAME = "XY-carriage"

START_FRAME = 1
STEP_FRAMES = 40  # gap between motion segments


# -------------------------------------------------------------------
# Helper: get object or fail loudly
# -------------------------------------------------------------------
def get_obj(name):
    obj = bpy.data.objects.get(name)
    if obj is None:
        raise ValueError(f"Object '{name}' not found in the scene.")
    return obj


def key_loc(obj, frame):
    bpy.context.scene.frame_set(frame)
    obj.keyframe_insert(data_path="location")


# -------------------------------------------------------------------
# Build a simple test animation
# -------------------------------------------------------------------
scene = bpy.context.scene

y_gantry = get_obj(Y_GANTRY_NAME)
x_axis = get_obj(X_AXIS_NAME)
xy_carriage = get_obj(XY_CARRIAGE_NAME)

print("\n--- SETTING UP TEST ANIMATION ---")
print("Initial positions:")
print("  Y gantry:", y_gantry.matrix_world.translation)
print("  X axis:", x_axis.matrix_world.translation)
print("  XY carriage:", xy_carriage.matrix_world.translation)

f0 = START_FRAME
f1 = f0 + STEP_FRAMES
f2 = f1 + STEP_FRAMES
f3 = f2 + STEP_FRAMES

# Set timeline range so Play shows the full sequence
scene.frame_start = f0
scene.frame_end = f3

# 1) Hold initial pose at f0
scene.frame_set(f0)
for obj in (y_gantry, x_axis, xy_carriage):
    obj.keyframe_insert(data_path="location")

# 2) Move Y gantry in +Y by 20 mm over f0→f1
print("\n--- TEST 1: Animate Y gantry +20mm in Y ---")
scene.frame_set(f1)
y_gantry.location.y += 0.2
key_loc(y_gantry, f1)

# Keep others pinned so curves look nice
key_loc(x_axis, f1)
key_loc(xy_carriage, f1)

# 3) Move X axis in +X by 30 mm over f1→f2
print("\n--- TEST 2: Animate X axis +30mm in X ---")
scene.frame_set(f2)
x_axis.location.x += 0.2
key_loc(x_axis, f2)
key_loc(y_gantry, f2)
key_loc(xy_carriage, f2)

# 4) Move XY carriage in +X by 10 mm over f2→f3
print("\n--- TEST 3: Animate XY carriage +10mm in X ---")
scene.frame_set(f3)
xy_carriage.location.x += 0.2
key_loc(xy_carriage, f3)
key_loc(y_gantry, f3)
key_loc(x_axis, f3)

# Jump back to start so you can just hit Play
scene.frame_set(f0)

print("\n--- TEST ANIMATION READY ---")
print(f"Timeline: frames {scene.frame_start} to {scene.frame_end}")
print("Scrub or press Play to see the gantry / axes move.\n")