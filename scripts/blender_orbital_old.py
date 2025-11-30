import bpy
import numpy as np
from typing import Any, cast

data = np.loadtxt("../../electron_positions.csv", delimiter=",")
q_m = -2  # the quantum number m
context = cast(Any, bpy.context)

# instance object
bpy.ops.mesh.primitive_ico_sphere_add()
ico = cast(Any, context.object)

# new material for the ico
mat = bpy.data.materials.new(name="matGreen")  # type: ignore[attr-defined]
mat.diffuse_color = (1, .402756, .00158945, 1)
# assign the material to ico
ico.data.materials.append(mat)  # type: ignore[attr-defined]

ico.hide_set(True)
ico.hide_render = True

# nucleus sphere
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5)
nuc = cast(Any, context.object)
# new material for the nuc
mat = bpy.data.materials.new(name="matBlue")  # type: ignore[attr-defined]
mat.diffuse_color = (0.0292951, 0.00549398, 0.8, 1)
# assign the material to nuc
nuc.data.materials.append(mat)  # type: ignore[attr-defined]

# cube object
bpy.ops.mesh.primitive_cube_add()
cube = cast(Any, context.object)

# ps
ps = cast(Any, cube.modifiers.new("Electron", 'PARTICLE_SYSTEM').particle_system)
psname = ps.name
ps.settings.count = 20000  # len(data)
ps.settings.lifetime = 1000
ps.settings.particle_size = 0.45
ps.settings.display_size = 0.45
ps.settings.frame_start = ps.settings.frame_end = 1
ps.settings.render_type = "OBJECT"
ps.settings.instance_object = ico

cube.show_instancer_for_render = False
cube.show_instancer_for_viewport = False

# to calculate the velocity of the particles. Related to the orbital probability current.
x0, y0, z0 = data[:, 0], data[:, 1], data[:, 2]
r_xy = np.sqrt(x0 * x0 + y0 * y0)
q_xy = np.arccos(x0 / np.where(r_xy == 0, 1e-12, r_xy))
for m in range(len(data)):
    if (y0[m] >= 0):
        q_xy[m] = np.arccos(x0[m] / (r_xy[m] if r_xy[m] != 0 else 1e-12))
    else:
        if (x0[m] < 0):
            q_xy[m] = -np.arccos(x0[m] / (r_xy[m] if r_xy[m] != 0 else 1e-12)) + np.pi * 2.0
        else:
            q_xy[m] = -np.arccos(x0[m] / (r_xy[m] if r_xy[m] != 0 else 1e-12))
r = np.sqrt(x0 * x0 + y0 * y0 + z0 * z0)
q = np.arccos(z0 / np.where(r == 0, 1e-12, r))
w = q_m * 10.0 / (r * np.sin(q))  # velocity

def particle_handler(scene, depsgraph):
    ob = depsgraph.objects.get(cube.name)
    if ob:
        ps_local = cast(Any, ob.particle_systems[psname])
        f = scene.frame_current
        dt = 1.0 / 60.0
        t = f / 60.0

        for m, particle in enumerate(cast(Any, ps_local.particles)):
            xp = r_xy[m] * np.cos(w[m] * t + q_xy[m])
            if (xp > 0 and z0[m] > 0):
                q_xy[m] += -np.pi
            x = r_xy[m] * np.cos(w[m] * t + q_xy[m])
            y = r_xy[m] * np.sin(w[m] * t + q_xy[m])
            setattr(particle, "location", (x, y, z0[m]))

# clear the post frame handler
handlers = cast(Any, bpy.app.handlers.frame_change_post)
handlers.clear()

# register orbital particle handler with post frame handler
handlers.append(particle_handler)

# trigger frame update
bpy.context.scene.frame_current = 0
