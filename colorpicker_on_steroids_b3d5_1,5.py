bl_info = {
    "name": "Colorpicker on Steroids",
    "author": "Max Puliero + AI",
    "version": (2, 3),
    "blender": (5, 0, 0),
    "location": "UI & 3D View > Press E",
    "description": "Smart flat color picker for UI and 3D Viewport with priority hotkeys",
    "category": "3D View",
}

import bpy

addon_keymaps = []

class SteroidPickerPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.label(text="Personalizza le scorciatoie da tastiera:")
        
        box = layout.box()
        for km, kmi in addon_keymaps:
            row = box.row()
            row.label(text=km.name)
            row.prop(kmi, "type", text="", full_event=True)
            row.prop(kmi, "value", text="")


class UI_OT_steroid_picker(bpy.types.Operator):
    bl_idname = "ui.steroid_picker"
    bl_label = "UI Colorpicker on Steroids"
    
    space_3d = None
    original_light = 'STUDIO'
    original_cavity = True
    original_fade_inactive = False
    
    def modal(self, context, event):
        if event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
            if self.space_3d:
                self.space_3d.shading.light = self.original_light
                self.space_3d.shading.show_cavity = self.original_cavity
                self.space_3d.overlay.show_fade_inactive = self.original_fade_inactive
            return {'FINISHED'}
        return {'PASS_THROUGH'}
        
    def invoke(self, context, event):
        try:
            result = bpy.ops.ui.eyedropper_color('INVOKE_DEFAULT')
            if 'RUNNING_MODAL' not in result:
                return {'PASS_THROUGH'}
        except Exception:
            return {'PASS_THROUGH'}

        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        self.space_3d = space
                        self.original_light = space.shading.light
                        self.original_cavity = space.shading.show_cavity
                        self.original_fade_inactive = space.overlay.show_fade_inactive
                        
                        space.shading.type = 'SOLID'
                        space.shading.light = 'FLAT'
                        space.shading.show_cavity = False
                        space.overlay.show_fade_inactive = False
                        break
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class VIEW3D_OT_steroid_picker(bpy.types.Operator):
    bl_idname = "view3d.steroid_picker"
    bl_label = "3D View Colorpicker on Steroids"
    
    space_3d = None
    original_light = 'STUDIO'
    original_cavity = True
    original_fade_inactive = False
    original_fade_alpha = 0.5
    
    def modal(self, context, event):
        if event.type in {'LEFTMOUSE', 'RIGHTMOUSE', 'ESC'} and event.value == 'PRESS':
            if event.type == 'LEFTMOUSE':
                try:
                    if context.mode == 'SCULPT':
                        bpy.ops.sculpt.sample_color('INVOKE_DEFAULT')
                    elif context.mode in {'PAINT_VERTEX', 'PAINT_TEXTURE', 'PAINT_2D'}:
                        bpy.ops.paint.sample_color('INVOKE_DEFAULT')
                except Exception:
                    pass
            
            context.window.cursor_modal_restore()
            
            if self.space_3d:
                self.space_3d.shading.light = self.original_light
                self.space_3d.shading.show_cavity = self.original_cavity
                self.space_3d.overlay.show_fade_inactive = self.original_fade_inactive
                self.space_3d.overlay.fade_inactive_alpha = self.original_fade_alpha
                
            return {'FINISHED'}
            
        return {'PASS_THROUGH'}
        
    def invoke(self, context, event):
        valid_modes = {'SCULPT', 'PAINT_VERTEX', 'PAINT_TEXTURE', 'PAINT_2D'}
        if context.mode not in valid_modes:
            return {'PASS_THROUGH'}
            
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        self.space_3d = space
                        
                        self.original_light = space.shading.light
                        self.original_cavity = space.shading.show_cavity
                        self.original_fade_inactive = space.overlay.show_fade_inactive
                        self.original_fade_alpha = space.overlay.fade_inactive_alpha
                        
                        space.shading.type = 'SOLID'
                        space.shading.light = 'FLAT'
                        space.shading.show_cavity = False
                        space.overlay.show_fade_inactive = True
                        space.overlay.fade_inactive_alpha = 0.9
                        break
        
        context.window.cursor_modal_set('EYEDROPPER')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


def register():
    bpy.utils.register_class(SteroidPickerPreferences)
    bpy.utils.register_class(UI_OT_steroid_picker)
    bpy.utils.register_class(VIEW3D_OT_steroid_picker)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km_ui = kc.keymaps.new(name='User Interface', space_type='EMPTY')
        # Aggiungiamo head=True per dare priorità assoluta al tasto nell'interfaccia
        kmi_ui = km_ui.keymap_items.new(UI_OT_steroid_picker.bl_idname, 'E', 'PRESS', head=True)
        addon_keymaps.append((km_ui, kmi_ui))
        
        km_3d = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        # Aggiungiamo head=True per dare priorità assoluta al tasto nella viewport 3D
        kmi_3d = km_3d.keymap_items.new(VIEW3D_OT_steroid_picker.bl_idname, 'E', 'PRESS', head=True)
        addon_keymaps.append((km_3d, kmi_3d))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(VIEW3D_OT_steroid_picker)
    bpy.utils.unregister_class(UI_OT_steroid_picker)
    bpy.utils.unregister_class(SteroidPickerPreferences)

if __name__ == "__main__":
    register()