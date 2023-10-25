import bpy

from bpy.props import StringProperty, IntProperty, CollectionProperty, PointerProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel

def get_layer_collection(collection, view_layer=None):
    '''Returns the view layer LayerCollection for a specificied Collection'''
    def scan_children(lc, result=None):
        for c in lc.children:
            if c.collection == collection:
                return c
            result = scan_children(c, result)
        return result

    if view_layer is None:
        view_layer = bpy.context.view_layer
    return scan_children(view_layer.layer_collection)

class Logger_Result_ListItem(PropertyGroup):
    """Group of properties representing an item in the list.""" 
    logType: StringProperty(
        name = "Name", 
        description = "Logger Result item log type.", 
        default = ""
    ) 
    message: StringProperty( 
        name = "", 
        description = "Logger Result item message.", 
        default = ""
    )
    object: PointerProperty(
        name = "Object",
        type = bpy.types.Object,
    )

class LoggerList_Select(Operator):
    r"""Select objects from log"""
    bl_idname = "log.selectobject"
    bl_label = ""
    bl_description = "Select the object that an log/warning/error is giving."

    index: IntProperty(name="Select object", default=0)

    @classmethod
    def poll(cls, context):
        return context.scene.logger_results_list

    def execute(self, context):
        object = context.scene.logger_results_list[self.index].object
        view_layer = context.scene.view_layers.get("ViewLayer")

        if view_layer:
            if object and object.name not in view_layer.objects:
                #Object not found in active collection, enable that collection
                collections = object.users_collection
                for collection in collections:
                    LayerCollection = get_layer_collection(collection)
                    LayerCollection.exclude = False
        else:
            print("view layer not found")
            return {'ERROR'}
        
        bpy.ops.object.select_all(action='DESELECT')
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.view3d.view_selected(use_all_regions=False)
        return {'FINISHED'}

class UL_LoggerList(UIList):
    """UL_LoggerList""" 
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            split = layout.split(factor=0.1)
            split.label(text = item.logType)
            split = split.split(factor=0.95)
            split.label(text = item.message)
            
            if context.scene.logger_results_list[index].object is not None:
                op = split.operator("log.selectobject", icon = "RESTRICT_SELECT_OFF")
                op.index = index

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text = "")

class Pnl_Logger(bpy.types.Panel):
    bl_label = "QA Bot"
    bl_idname = "VIEW_3D_PT_Log"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'QA Bot'
    bl_order = 2

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        box = layout.box()

        col = box.column(align=False)

        row = col.row(align=True)
        split = row.split(factor = 0.8)
        split.operator("logger.run", icon='AUTO', text="Run QA Bot")
        
        split.operator("logger.clear", text="Clear")
        row = col.row(align=True)

class Pnl_LoggerLog(bpy.types.Panel):
    bl_parent_id = "VIEW_3D_PT_Log"
    bl_label = "Logger Log"
    bl_idname = "VIEW_3D_PT_LogLog"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'QA Bot'
    bl_order = 5

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        box = layout.box()

        col = box.column(align=False)

        row = col.row(align=True)
        row.split(factor = 0.2)
        row.label(text = scene.str_LoggerEndResult)
        row.label(text = "Logs: " + str(scene.int_LoggerLogCount) + ", Warnings: " + str(scene.int_LoggerWarningCount) + ", Errors: " + str(scene.int_LoggerErrorCount))
        #row.prop(context.scene, "enum_ShowErrorTypes")

        row = col.row(align=True)
        row.template_list("UL_LoggerList", "The_List", scene, "logger_results_list", scene, "logger_results_index")


classes = (
    UL_LoggerList,
    Pnl_Logger,
    Pnl_LoggerLog,
    LoggerList_Select,
    Logger_Result_ListItem,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.logger_results_list = CollectionProperty(type = Logger_Result_ListItem)
    bpy.types.Scene.logger_results_index = IntProperty(name = "Index for Logger Results", default = 0)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.logger_results_list
    del bpy.types.Scene.logger_results_index