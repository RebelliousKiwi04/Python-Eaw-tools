import math, bpy, os

class Unit:
    def __init__(self, xml_entry, file, modpath):
        self.entry = xml_entry
        self.fileLocation = file
        self.modpath = modpath
        self.aicp = self.get_aicp()
        self.model_path = self.get_model_path()
        self.bones = None
        self.name = self.get_name()
        self.category_masks = self.get_category_masks()
        self.variant = self.set_variant()
        self.type = self.entry.tag
        # if self.model_path != None:
        #     self.bones = self.get_bones()
    def get_aicp(self) -> int:
        for item in self.entry:
            if item.tag == 'AI_Combat_Power':
                if item.text != None:
                    return int(math.floor(float(item.text)))
        return 0
    def get_name(self) -> str:
        return self.entry.get('Name')
    def get_category_masks(self):
        for item in self.entry:
            if item.tag == 'CategoryMask':
                outputList = [] 
                if item.text != None:
                    for text in item.text.split():
                        newText = text.replace('|','')
                        if len(newText) > 3:
                            outputList.append(newText)
                    return outputList
    def set_variant(self):
        for item in self.entry:
            if item.tag == 'Variant_Of_Existing_Type':
                return item.text
        return None
    def get_model_path(self):
        for item in self.entry:
            if item.tag == 'Space_Model_Name':
                return os.path.abspath(self.modpath + """/Art/Models/""" + item.text)
            if item.tag == 'Land_Model_Name':
                return os.path.abspath(self.modpath + """/Art/Models/""" + item.text)
        return None
    def get_bones(self): 
        if not os.path.isfile(self.model_path):
            return None
        bpy.ops.preferences.addon_enable(module='io_alamo_tools')
        bpy.ops.import_mesh.import_alo(filepath=self.model_path)
        armatureName = bpy.context.scene.ActiveSkeleton.skeletonEnum
        if armatureName == 'None':
            print("No Armature")
            return None
        armature = bpy.data.objects[armatureName]
        print(armature.data)
        for bone in armature.data.bones:
            print(bone.name)
        return armature.data.bones
    