import os
import shutil
import hou


def set_unity_hda_folder(force=False):
    unity_hda_path = hou.getenv("UNITY_PROJECT_HDA_PATH")
    if unity_hda_path == None or force:
        unity_hda_path = _select_folder_popup()       
    return unity_hda_path

def _select_folder_popup():
    hou.ui.setStatusMessage("Please select your Unity project HDA folder", hou.severityType.ImportantMessage)
    path = hou.ui.selectFile(file_type=hou.fileType.Directory)
    if path:
        hou.hscript("set -g UNITY_PROJECT_HDA_PATH=%s"%(path))
        hou.ui.setStatusMessage("")
    else:
        hou.ui.setStatusMessage("Cancelled folder selection...")
    return path

def save_and_push_to_unity(kwargs):
    node = kwargs["node"]
    unity_hda_path = set_unity_hda_folder()            
    if unity_hda_path:
        hda_def = node.type().definition()
        node_type_name = hda_def.nodeTypeName()
        lib_file_path = hda_def.libraryFilePath()
        base_name = os.path.basename(lib_file_path)
        hda_def.updateFromNode(node)
        target_file = os.path.join(unity_hda_path, base_name)
        try:	
            shutil.copy2(lib_file_path, target_file)
            hou.ui.setStatusMessage(f"{node_type_name} saved to {lib_file_path} and pushed to {target_file}")
        except OSError as err:
            print(f"{err}. Cannot push {node_type_name} to {target_file}.")