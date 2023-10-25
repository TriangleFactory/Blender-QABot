import bpy
from . import ui
from . import Logger
from . import props

bl_info = {
	"name": "QA Bot",
	"description": "Validation tool.",
	"author": "Triangle Factory BV",
	"version": (3, 0, 1),
	"blender": (3, 2, 0),
	"location": "Object > QA Bot",
	"warning": "",
	"category": ""
}

def register():
	props.register()
	ui.register()
	Logger.register()

def unregister():
	props.unregister()
	ui.unregister()
	Logger.unregister()