import bpy

Z_AXIS_NAME = "Z-axis"
X_AXIS_NAME = "X-axis"
Y_AXIS_NAME = "Y-axis"

scene = bpy.context.scene

def get_obj(name):
    obj = bpy.data.objects.get(name)
    if obj is None:
        raise RuntimeError(f"Object '{name}' not found in the scene.")
    return obj

def get_limit_min_max(obj, axis):
    """axis: 'X', 'Y', or 'Z' — returns (min, max) from Limit Location."""
    for c in obj.constraints:
        if c.type == 'LIMIT_LOCATION':
            if axis == 'X':
                if c.use_min_x and c.use_max_x:
                    return c.min_x, c.max_x
                elif c.use_min_x:
                    return c.min_x, c.min_x
                elif c.use_max_x:
                    return c.max_x, c.max_x
            elif axis == 'Y':
                if c.use_min_y and c.use_max_y:
                    return c.min_y, c.max_y
                elif c.use_min_y:
                    return c.min_y, c.min_y
                elif c.use_max_y:
                    return c.max_y, c.max_y
            elif axis == 'Z':
                if c.use_min_z and c.use_max_z:
                    return c.min_z, c.max_z
                elif c.use_min_z:
                    return c.min_z, c.min_z
                elif c.use_max_z:
                    return c.max_z, c.max_z
    raise RuntimeError(f"No Limit Location {axis} min/max found on {obj.name}")

z_axis = get_obj(Z_AXIS_NAME)
x_axis = get_obj(X_AXIS_NAME)
y_axis = get_obj(Y_AXIS_NAME)

home_z, max_z = get_limit_min_max(z_axis, 'Z')
home_x, max_x = get_limit_min_max(x_axis, 'X')
home_y, max_y = get_limit_min_max(y_axis, 'Y')

scene.frame_start = 1
scene.frame_end   = 80

# Frame 1: at min (home)
scene.frame_set(1)
z_axis.location.z = home_z
x_axis.location.x = home_x
y_axis.location.y = home_y
z_axis.keyframe_insert(data_path="location")
x_axis.keyframe_insert(data_path="location")
y_axis.keyframe_insert(data_path="location")

# Frame 40: at max
scene.frame_set(40)
z_axis.location.z = max_z
x_axis.location.x = max_x
y_axis.location.y = max_y
z_axis.keyframe_insert(data_path="location")
x_axis.keyframe_insert(data_path="location")
y_axis.keyframe_insert(data_path="location")

# Frame 80: back to min
scene.frame_set(80)
z_axis.location.z = home_z
x_axis.location.x = home_x
y_axis.location.y = home_y
z_axis.keyframe_insert(data_path="location")
x_axis.keyframe_insert(data_path="location")
y_axis.keyframe_insert(data_path="location")

scene.frame_set(1)

print(f"Z-axis anim: Z from {home_z} -> {max_z} -> {home_z}.")
print(f"CoreXY anim: X-axis {home_x} -> {max_x} -> {home_x}, "
      f"Y-axis {home_y} -> {max_y} -> {home_y}. Scrub/Play to see full travel.")