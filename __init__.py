# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "NX_SetTime",
    "author" : "Franck Demongin",
    "description" : "Set time of animation in seconds",
    "blender" : (2, 80, 0),
    "version" : (0, 1, 0),
    "location" : "Properties > Output > Frame Range",
    "category" : "Generic"
}

import bpy

def draw(cls, context, arg):
        cls.layout.label(text=message)

class NXDURATION_OT_duration(bpy.types.Operator):
    bl_label="Set duration"
    bl_description="Update frame end"
    bl_idname="nxduration.duration"
        
    def execute(self, context):
        scene = context.scene
        duration = scene.render.fps * scene.nx_duration
        if scene.nx_inverse:
            frame_start = int(round(scene.frame_end - duration + 1))
            if frame_start > 0:
                scene.frame_start = frame_start
            else:
                scene.frame_start = 1
                self.report({'WARNING'}, f"Frame start is set to one")
        else:
            scene.frame_end = int(round((scene.render.fps * scene.nx_duration) + scene.frame_start -1))
        
        return {'FINISHED'}
    
def duration_panel(self, context):
    layout = self.layout
    scene = context.scene
    row = layout.row(align=False)
    row.prop(context.scene, 'nx_duration', text=f"{(scene.frame_end - scene.frame_start + 1) / scene.render.fps:.2f} second(s)")
    row.operator("nxduration.duration", text="", icon="PLAY")
    row = layout.row()
    row.prop(context.scene, 'nx_inverse', text="From End")
    
def register():    
    bpy.utils.register_class(NXDURATION_OT_duration)
    bpy.types.RENDER_PT_frame_range.append(duration_panel)        
    
    bpy.types.Scene.nx_duration = bpy.props.FloatProperty(name='Duration', description="Set duration", default=10.0, min=0.0, step=100)
    bpy.types.Scene.nx_inverse = bpy.props.BoolProperty(name="From End", description="Start from frame end and fixe frame start if possible", default=False)
    
def unregister():
    bpy.utils.unregister_class(NXDURATION_OT_duration)
    bpy.types.RENDER_PT_frame_range.remove(duration_panel)    
    
    del bpy.types.Scene.nx_duration    
    del bpy.types.Scene.nx_inverse 
    
if __name__ == '__main__':
    register()