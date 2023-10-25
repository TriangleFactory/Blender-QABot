import bpy
from bpy.props import EnumProperty, StringProperty, FloatVectorProperty, BoolProperty, IntProperty, CollectionProperty

def register():
    bpy.types.Scene.str_LoggerEndResult = StringProperty(
        name = "",
        default = ""
    )
    bpy.types.Scene.int_LoggerErrorCount = IntProperty(
        name = "",
        description = "Amount of errors Logger has found.",
        default = 0,
    )
    bpy.types.Scene.int_LoggerWarningCount = IntProperty(
        name = "",
        description = "Amount of warnings Logger has found.",
        default = 0,
    )
    bpy.types.Scene.int_LoggerLogCount = IntProperty(
        name = "",
        description = "Amount of logs Logger has found.",
        default = 0,
    )
    bpy.types.Scene.enum_ShowErrorTypes = EnumProperty(
        name="",
        description="Filter for showing different kinds of error types in the Logger log.",
        items=[
            ('Logger_Log_All', 'All', ''),
            ('Logger_Log_Logs', 'Logs', ''),
            ('Logger_Log_Warnings', 'Warnings', ''),
            ('Logger_Log_Errors', 'Errors', ''),
        ]
    )

def unregister():
    del bpy.types.Scene.str_LoggerEndResult
    del bpy.types.Scene.int_LoggerErrorCount
    del bpy.types.Scene.int_LoggerWarningCount
    del bpy.types.Scene.int_LoggerLogCount
    del bpy.types.Scene.enum_ShowErrorTypes