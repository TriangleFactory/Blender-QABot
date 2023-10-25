import bpy
from datetime import datetime

ltError = "Error:"
ltWarning = "Warning:"
ltLog = "Log:"

def addItemToLogger(context, logType, logText, *args):
    item = context.scene.logger_results_list.add()
    item.logType = logType
    item.message = logText
    context.scene.logger_results_index = len(context.scene.logger_results_list) - 1
    for ar in args:
        item.object = ar

    if(logType == ltLog):
        context.scene.int_LoggerLogCount += 1
    elif(logType == ltWarning):
        context.scene.int_LoggerWarningCount += 1
    elif(logType == ltError):
        context.scene.int_LoggerErrorCount += 1

class Logger(bpy.types.Operator):
    #Only allow in object mode
    bl_idname = 'logger.run'
    bl_label = 'Logger > Run Logger'
    bl_options = {"REGISTER", "UNDO"}


    def execute(self, context):
        first_time = datetime.now()
        scene = context.scene
        context.scene.logger_results_list.clear()

        #Reset vars & checks
        scene.int_LoggerLogCount = 0
        scene.int_LoggerWarningCount = 0
        scene.int_LoggerErrorCount = 0


        #Do your own checks in here
        #---------------------------------
        #This is a generic log without any object specific context.
        addItemToLogger(context, ltLog, "This is an example log.")
        addItemToLogger(context, ltWarning, "This is an example warning.")
        addItemToLogger(context, ltError, "This is an example error.")

        #You can also add an object to your log message in case you want the user to be able to click on it and be redirected to that object
        for obj in bpy.data.objects:
            addItemToLogger(context, ltError, "Object in scene: " + obj.name + " has errors.", obj)
        #---------------------------------
                   
        #Print out Logger result
        if context.scene.int_LoggerErrorCount > 0:
            context.scene.str_LoggerEndResult = "Logger is not happy ʘ︵ʘ"
        elif context.scene.int_LoggerWarningCount > 0:
            context.scene.str_LoggerEndResult = "Logger is semi happy ¯\_(ツ)_/¯"
        else:
            context.scene.str_LoggerEndResult = "Logger happy ʘ‿ʘ"

        duration = datetime.now() - first_time
        duration_in_s = duration.total_seconds()

        addItemToLogger(context, ltLog, "Logger finished processing in " + str(duration_in_s) + " seconds.")
        return {"FINISHED"}
    
class LoggerClear(bpy.types.Operator):
    #Only allow in object mode
    bl_idname = 'logger.clear'
    bl_label = 'Logger > Clear Logger'
    bl_options = {"REGISTER", "UNDO"}
    bl_description = "Clear the Logger list."

    def execute(self, context):
        context.scene.logger_results_list.clear()
        context.scene.str_LoggerEndResult = ""
        context.scene.int_LoggerErrorCount = 0
        context.scene.int_LoggerWarningCount = 0
        context.scene.int_LoggerLogCount = 0
        return {"FINISHED"}
    
class LoggerSelect(bpy.types.Operator):
    #Only allow in object mode
    bl_idname = 'logger.select'
    bl_label = 'Logger > Select Logger objects'
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def description(cls, context, properties):
        ans = ''
        objects = context.scene.coll_LoggerObjects[properties.index]
        for x in objects.objects:
            ans += x.name + '\n'
        return ans
    
    def invoke(self, context, event):
        scene = context.scene
        scene.coll_LoggerObjects.select()
        return {"FINISHED"}


# Classes
classes = (
    Logger,
    LoggerClear,
    LoggerSelect,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)