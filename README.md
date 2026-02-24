# Jubilee Blender Twin

This repository contains a Blender-based *digital twin* of the Jubilee open‑source motion platform, plus Python helper scripts to drive and record motion tests.


![Jubilee test animation](docs/jubilee_test.gif)


## Who this is for (and what this is for)

This repo targets people who:

- Have (or plan to build) a Jubilee and want a **digital twin** they can control from Python.
- Care more about **motion, animation, and experimentation** than full parametric CAD.
- Want to script repeatable motion tests and record GIFs of the resulting animations, with metadata tracked in a database.

The main goals are:

- Visualize Jubilee motion in 3D from Python.
- Prototype motion / control ideas safely before touching hardware.
- Produce reproducible, documented GIFs of those experiments that you can embed (e.g. in this README).


## Why Blender, and its limitations as CAD

Blender is used here because it has:

- A powerful, embedded **Python API** (`bpy`).
- Good support for **keyframed animation** and constraints.
- A broadly available, cross‑platform UI.

However, Blender is *not* a mechanical CAD tool. Key limitations of this setup:

- The Jubilee geometry comes from an imported **STEP** file, converted to a mesh format (glTF `.glb`) and imported into Blender.
  - You do **not** get parametric history or feature trees.
  - Editing dimensions precisely (e.g. hole locations, plate thickness) is much harder than in SolidWorks/FreeCAD/Fusion.
- This scene is **not the authoritative CAD source** for Jubilee:
  - Tolerances, fasteners, BOM, and fabrication exports still live in the original Jubilee repo.
  - Round‑tripping changes back into mechanical CAD is non‑trivial.
- Motion constraints model only the **high‑level axis travel**, not detailed joint compliance, belt elasticity, etc.

So: this repo is for **motion visualization and scripted animation**, not for editing the canonical Jubilee CAD.


## What is in `jubilee.blend`

### Geometry source

The 3D model is based on the Jubilee STEP file from the upstream project:

- Source STEP: `frame/cads/STEP/jubilee.STEP` in the Jubilee repo
  - https://github.com/machineagency/jubilee/blob/rel/jubilee_2.1.0/frame/cads/STEP/jubilee.STEP

The STEP file was converted to a glTF/GLB mesh (via FreeCAD) and imported into Blender, then organized into collections.

### Kinematic empties and parenting

Blender "empties" are non‑rendered objects that only carry a **transform** (location/rotation/scale). Here they represent reference frames for moving parts of the machine.

Key empties/objects in the scene:

- `Z-axis` – represents the Z carriage motion.
- `Y-axis` – represents the Y gantry motion.
- `X-axis` – represents the X carriage motion.
- `XY-carriage` – represents the toolhead / moving carriage.

Parenting encodes the motion stack:

- `Y-axis` is the parent of `X-axis`.
- `X-axis` is the parent of `XY-carriage`.

So moving `Y-axis` moves everything above it, just like on the real machine.

### Travel limits via constraints

Axis travel is modeled using **Limit Location** constraints on these empties. For example, the Z axis object has a Limit Location on Z; the Python tests query these min/max values and keyframe motion between them.

This gives a simple, scriptable model of:

- Home position (min limit).
- Maximum travel.
- Motion paths between those positions.


## Python control and motion tests

The `test_python/` folder contains small scripts that exercise the digital twin:

- `test_home_and_move.py`
  - Reads Limit Location constraints on `X-axis`, `Y-axis`, and `Z-axis`.
  - Animates each axis from home (min) → max → home over a short timeline.

- `test_motion.py`
  - Uses three empties: `Y-axis`, `X-axis`, and `XY-carriage`.
  - Builds a multi‑step test animation:
    - Move Y in +Y.
    - Then move X in +X.
    - Then move `XY-carriage` in +X.

- `test_z_move.py`
  - Quick test moving `Z-axis` in +Z over a short frame range.

- `animation_to_gif.py`
  - Config‑driven script (reads `animation_config.json` if present).
  - Sets camera, lighting/brightness, resolution, renders a PNG frame sequence and converts it to a GIF (`docs/jubilee_test.gif`) via `ffmpeg`.

### Running tests directly in Blender

1. Open `jubilee.blend` in Blender.
2. Open the **Text Editor** in any area.
3. Load one of the scripts from `test_python/`.
4. Press **Run Script**.
5. Scrub the timeline or press **Play** to see the motion.

All scripts expect axis‑object names:

- `X-axis`
- `Y-axis`
- `Z-axis`


#### Important:
- **Z min and axis direction:**
  - The Z minimum (from the Z-axis object's LIMIT_LOCATION constraint) determines the lowest position for Z in the animation. Make sure this matches your machine's physical zero.
  - Double-check that the positive direction of each axis in Blender matches the real Jubilee machine. For Z, positive should be up (away from the bed); if not, adjust your Blender object orientation or the script accordingly.
- **Units and dimensions:**
  - Ensure your G-code, Blender scene, and machine all use the same units (typically millimeters). If your Blender scene is in meters but your G-code is in millimeters, scale accordingly or set Blender's unit system to millimeters for accurate visualization.
- The script expects Blender objects named `X-axis`, `Y-axis`, and optionally `Z-axis`.
- Axis minimum positions are read from Blender's axis constraints (LIMIT_LOCATION).
- The animation speed can be adjusted by changing `SPEED_FACTOR` in `from_gcode/animate_path.py`.
- The scene's end frame is set automatically to fit the animation.


## Animating the Jubilee with G-code

This project allows you to visualize and animate Jubilee toolpaths directly from G-code using Blender.
This is heavily inspired from: https://github.com/TanmayChhatbar/blender_3d_print_animation.
### Workflow

1. **Generate G-code**
  - Use your preferred tool (e.g., science-jubilee) to generate a G-code file. The latest G-code should be saved as `science_jubilee/gcode_logs/latest.gcode`.

2. **Run the Animation Batch Script**
  - Execute `from_gcode/run_latest_gcode_animation.bat`.
  - This will:
    - Copy the latest G-code to the animation folder
    - Parse the G-code and generate a toolpath CSV
    - Launch Blender, open `jubilee.blend`, and animate the axes using the toolpath

3. **View the Animation**
  - Blender will open with the animation ready to play.
  - Use the timeline/play controls to watch the axes move according to the G-code.

### Notes
- The script expects Blender objects named `X-axis`, `Y-axis`, and optionally `Z-axis`.
- Axis minimum positions are read from Blender's axis constraints (LIMIT_LOCATION).
- The animation speed can be adjusted by changing `SPEED_FACTOR` in `from_gcode/animate_path.py`.
- The scene's end frame is set automatically to fit the animation.

## Recording GIFs and experiment metadata with Sacred

The `sacred_runner.py` script is for **recording GIFs**, together with the parameters used to produce them, into MongoDB via [Sacred](https://github.com/IDSIA/sacred).

At a high level it:

1. Reads base settings (experiment name, Mongo URL/DB) from `animation_config.json`.
2. Uses Sacred to manage a run, with configurable parameters (frame range, resolution, target object, etc.).
3. Writes a full `animation_config.json` (including paths and animation settings).
4. Launches Blender in **background** mode (`-b`) with `jubilee.blend` and `animation_to_gif.py`.
5. After Blender finishes:
   - Collects `docs/jubilee_test.gif` as a Sacred artifact.
   - Optionally collects the first rendered frame.

These GIFs can then be embedded in documentation (including this README), and the corresponding Sacred run in MongoDB tells you exactly **which parameters** produced each GIF.

### Setup: Python virtualenv with Sacred

From the repo root on Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install sacred pymongo
```

You will run `sacred_runner.py` from this virtualenv. Sacred **does not** need to be installed into Blender's Python.

### Setup: MongoDB Community Edition

Install MongoDB Community Edition from the official site (Windows installer):

- https://www.mongodb.com/try/download/community

During setup you can accept the defaults so that a local server runs on `mongodb://localhost:27017`.

### Configure Sacred + Blender integration

In the repo root there is an `animation_config.json` file. At minimum it should define:

```json
{
  "experiment_name": "jubilee_blender_gif",
  "mongo_url": "mongodb://localhost:27017",
  "mongo_db_name": "animate_jubilee"
}
```

`sacred_runner.py` will read these values to construct the Sacred experiment and connect to MongoDB, then extend this JSON with all the animation and path parameters for each run.

Ensure the paths in `sacred_runner.py` match your setup:

- `blender_exe` – path to `blender.exe` (e.g. `C:\\Program Files\\Blender Foundation\\Blender 5.0\\blender.exe`).
- `blend_file` – typically this repo's `jubilee.blend`.
- `script_file` – typically this repo's `animation_to_gif.py`.

Blender is always started in **background** mode via `-b` (no GUI window), runs the script, then exits.

### Run a Sacred‑controlled GIF render

With the virtualenv active and MongoDB running:

```bash
python sacred_runner.py with test_mode=True test_max_frames=5 render_res_x=800 render_res_y=800
```

The runner will:

- Spawn Blender in background with `jubilee.blend` and `animation_to_gif.py`.
- Write an updated `animation_config.json` file with the chosen parameters **and** paths (Blender exe, `.blend`, animation script, experiment/mongo info).
- Let `animation_to_gif.py` read that JSON, render PNG frames to `render_gif/`, and build `docs/jubilee_test.gif` via ffmpeg.
- Store the resulting GIF and first frame as Sacred artifacts in MongoDB.

### Viewing Sacred runs with AltarViewer

You can browse Sacred runs stored in MongoDB using **AltarViewer** from the [Altar project](https://github.com/DreamRepo/Altar/tree/main/AltarViewer):

- https://github.com/DreamRepo/Altar/tree/main/AltarViewer

Follow that project's instructions to install and run AltarViewer, then point it at the same MongoDB database you configured in `animation_config.json` (for example, `mongo_url = mongodb://localhost:27017` and `mongo_db_name = animate_jubilee`).

### Example GIF used in this README

By default, `animation_to_gif.py` writes its output to:

- `docs/jubilee_test.gif`

It is embedded below using standard Markdown:

![Jubilee test animation](docs/jubilee_test.gif)

## Relationship to Jubilee3D

This repository is derived from and intended to complement the main Jubilee project:

- Jubilee main repo: https://github.com/machineagency/jubilee
- Jubilee documentation: https://jubilee3d.com/
- OSHWA certification for Jubilee: https://certification.oshwa.org/us002091.html

Jubilee itself is licensed under a [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Hardware design content in this repository follows the **same CC BY 4.0** license. See `LICENSE-HARDWARE.md` for details.

If you extend this project (e.g. alternate frames, tools, or fixtures), please document your changes and keep them under an OSHW-compatible license.
