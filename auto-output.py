import mset
import os
import re
import time

file_field = mset.UITextField()
file_field.value = ""

frame_folder_field = mset.UITextField()
frame_folder_field.value = ""

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
 
def set_frame_folder():
    # open a folder dialog
    path = mset.showOpenFolderDialog()
    if path != '':
        frame_folder_field.value = path
 
def set_material_frames():
    frameRootPath = frame_folder_field.value #"c:\\frame_6-8-9-10" # ex. C:\Users\enemy\Desktop\maps\house\Houset_Edit\Frame_6-8-9-10
    material_range: tuple = (0, 30)
    materials = mset.getSelectedMaterialGroup()
    materials_count = len(materials)
    for material in materials:
        material_nummer = material.name
        
        #if not material_range[0] <= int(material_nummer) <= material_range[1]:
        #    continue
        
        rootFrameFolderName = os.path.basename(os.path.normpath(frameRootPath))
        material_number_new_format = str('%03d' % int(material_nummer)) # 0 to 000
        currentFrameFolderName = rootFrameFolderName + "_" + material_number_new_format
        currentFrameName = material_number_new_format + ".tif"
        currentFramePath = os.path.normpath(os.path.join(frameRootPath, currentFrameFolderName, currentFrameName)).replace(os.sep, "/")
        print(currentFramePath)
        displacement = material.getSubroutine("displacement")
        if displacement is None:
            material.setSubroutine("displacement", "Height")
            displacement = material.getSubroutine("displacement")
        
        displacement.setField("Displacement Map", currentFramePath)
        #displacement.setField("Displacement Map", "C:/tests/frames/frame_4_5_6/frame_4_5_6_000/000.tif")
            
# Main UI
window = mset.UIWindow(name="Auto Material to BakeOutput")
window.width = 600
window.height = 1000
window.addStretchSpace()
window.addReturn()
# Get Output Folder
window.addElement(mset.UILabel("Select Displacement Map"))
window.addElement(file_field)
file_button = mset.UIButton("...")
file_button.onClick = set_displacement_map
window.addElement(file_button)

copy_button = mset.UIButton("Copy")
copy_button.onClick = get_displacement_map
window.addElement(copy_button)

window.addReturn()

window.addElement(mset.UILabel("Select Root Frame Folder"))
window.addElement(frame_folder_field)

frame_folder_button = mset.UIButton("...")
frame_folder_button.onClick = set_frame_folder
window.addElement(frame_folder_button)

copy_material_frames_button = mset.UIButton("Copy Material Frames")
copy_material_frames_button.onClick = set_material_frames
window.addElement(copy_material_frames_button)

window.addReturn()