import mset
import os
import re
import time

file_field = mset.UITextField()
file_field.value = ""

def set_displacement_map():
    path = mset.showOpenFileDialog(["tif"])
    if path != '':
        file_field.value = path
        # change the extension to .tga
        output_path = os.path.splitext(path)[0] + ".tga"
        
        material = mset.getSelectedMaterial()
        displacement = material.getSubroutine("displacement")
        displacement.setField("Displacement Map", path)
        
        object = mset.getSelectedObject()
        if isinstance(object, mset.BakerObject):
            object.outputPath = output_path
            
def get_displacement_map():
    materials = mset.getSelectedMaterialGroup()
    for material in materials:
        
        material_nummer = material.name
               
        objects = [object for object in mset.getAllObjects() if isinstance(object, mset.BakerObject) and object.name == material_nummer]
        for object in objects:
            displacement = material.getSubroutine("displacement")
            displacement_map = displacement.getField("Displacement Map")
            if displacement_map is None:
                continue
            
            displacement_map_path = displacement_map.path
            
            object.outputPath = os.path.splitext(displacement_map_path)[0] + ".tga"
            
# Main UI
window = mset.UIWindow(name="Auto Material to BakeOutput")
window.width = 400
window.height = 1000
window.addStretchSpace()
window.addReturn()
# Get Output Folder
window.addElement(mset.UILabel("Select Displacement Map"))
window.addElement(file_field)
file_button = mset.UIButton("...")
file_button.onClick = set_displacement_map
window.addElement(file_button)

file_button = mset.UIButton("Copy")
file_button.onClick = get_displacement_map
window.addElement(file_button)

window.addReturn()