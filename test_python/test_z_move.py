import bpy

# In the current jubilee.blend, the Z axis object is named "Z-axis"
obj = bpy.data.objects.get("Z-axis")
if obj is None:
    raise RuntimeError("Object 'Z-axis' not found in the scene.")

scene = bpy.context.scene

# Short test range
scene.frame_start = 1
scene.frame_end = 40

# Frame 1: keyframe current location
scene.frame_set(1)
obj.keyframe_insert(data_path="location")

# Frame 40: move +Z and keyframe
scene.frame_set(40)
obj.location.z += 0.2  # adjust for more/less travel
obj.keyframe_insert(data_path="location")

# Back to start
scene.frame_set(1)

print("Z-driver test animation ready: scrub or press Play to see Z move.")


"""
import bpy

obj = bpy.context.active_object
if obj is None:
    raise RuntimeError("Select an object (empty or mesh) first, then run this script.")

scene = bpy.context.scene

# Set a short timeline
scene.frame_start = 1
scene.frame_end = 40

# Frame 1: keyframe current location
scene.frame_set(1)
obj.keyframe_insert(data_path="location")

# Frame 40: move +Z and keyframe again
scene.frame_set(40)
obj.location.z += 0.2  # adjust value if you want a bigger move
obj.keyframe_insert(data_path="location")

# Go back to start
scene.frame_set(1)

print(f"Z-move test set up for object: {obj.name}. Scrub or press Play to see it move in Z.")

"""