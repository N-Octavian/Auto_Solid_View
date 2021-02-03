import bpy

# We import driver_namespace so we can manage our handlers by using keys
from bpy.app import driver_namespace
# We import this so we can make our handlers persistent, meaning that we dont' have to run the script again
# when opening a new file. Still have to run the script again when reopening Blender.
from bpy.app.handlers import persistent


# We define the key for our handler
pre_render_view_handler_key = "GPU_PRE_RENDER_VIEW"


# This function will be our handler
# As the name suggests, this handler activates right before we start rendering

# We define our handler as persistent
@persistent
def pre_render_view(self):
    #No way to access global settings VIEW_3D as far as I know, so we do it for every screen, and every area
    for screen in bpy.data.screens:
        for area in screen.areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = "SOLID"


# We have to make a function for deleting our handler via its key, so we don't have multiple handlers conflicting
def delete_handler(handler_key):
    if handler_key in driver_namespace:
        if driver_namespace[handler_key] in bpy.app.handlers.render_pre:
            bpy.app.handlers.render_pre.remove(driver_namespace[handler_key])
            del driver_namespace[handler_key]


# We first delete any handler using our key, so we are sure there isn't one present
delete_handler(pre_render_view_handler_key)

# We add our handler                    
bpy.app.handlers.render_pre.append(pre_render_view)

# We add our handler key which is needed for managing it
driver_namespace[pre_render_view_handler_key] = pre_render_view