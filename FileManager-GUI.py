import PySimpleGUI as sg
import time
from os import listdir
from os.path import isfile, join
import logging
import os
import shutil

pollTime = 1

def file_in_directory(watchingPath: str):
    newFiles = [f for f in os.listdir(watchingPath) if isfile(join(watchingPath,f))]
    return(newFiles)

# ---- Listing files in Directory ---- #
def list_all_files_in_directory(watchingPath: str):
    allFiles = [f for f in os.listdir(watchingPath) if isfile(join(watchingPath,f))]
    none_list = "\n".join(allFiles)
    window["-OUTPUT_WINDOW-"].print(">>> Listing all Files:")
    return(none_list)

# ---- Function for Comparing two lists ---- #

def comparison_list_of_files(originalList: list, newList: list):
    differencesList = [x for x in newList if x not in originalList] #Note if files get deleted, this will not highlight them
    return(differencesList)

#---- Function where the files get listed, cut, concated etc. ----#

def do_things_with_new_files(newFiles: list):
    
    global file_name_without_extension # Gets the Filename with it's extension
    global file_name_with_extension # Gets the Filename with the extension cut out

    file_name_with_extension = newFiles[0]
    file_name_without_extension = newFiles[0].split(".")[0]
    
    window["-OUTPUT_WINDOW-"].print(f">>> Filename with Extension: {file_name_with_extension}")

#---- Main Function for the Folder Observer which starts with the Start and Stop button ----#

def file_observer(watchingPath: str, pollTime: int):
    
    global stop
    x = 0
    
    while x < 1200 and not stop:  # New statement
        time.sleep(1)
        x += 1
        if "watching" not in locals():
            previousFileList = file_in_directory(watchingPath) 
            watching = 1
            
        time.sleep(pollTime)
        
        newFileList = file_in_directory(watchingPath)
        fileDiff = comparison_list_of_files(previousFileList, newFileList)
        previousFileList = newFileList
        
        if len(fileDiff) == 0: continue
        do_things_with_new_files(fileDiff)

#---- Function for listing all files in the selected Folder which is being watched ----#
    
def file_type (ends_with: str, watchingPath: str):
    sourcefiles = os.listdir(watchingPath)
    for file in sourcefiles:
        if file.endswith(ends_with):
            window["-OUTPUT_WINDOW-"].print(os.path.join(file))

#---- Function for moving all or set filetype files to a new destination with the Move Button ----#

def move_all_file_to_new_destination(ends_with: str, move_file_to_new_dest: str, watchingPath: str):
    for file in os.listdir(watchingPath):
        if file.endswith(ends_with):
            shutil.move(os.path.join(watchingPath,file), os.path.join(move_file_to_new_dest,file))
            window["-OUTPUT_WINDOW-"].print(f"Moved File: {file}")

#---- Function for moving a single file which the Folder Observer catches (Optional)  ----#
           
def move_single_file_to_new_destination(move_file_to_new_dest: str, watchingPath: str):
    file = watchingPath + "/" + file_name_with_extension
    shutil.move(file,move_file_to_new_dest)
    window["-OUTPUT_WINDOW-"].print(f"\n >>> Moved file {file_name_with_extension} FROM DESTINATION {watchingPath} to NEW DESTINATION {move_file_to_new_dest}")

    #----GUI Definition and Layout----#
my_new_theme = {'BACKGROUND': '#1c1e23',
                'TEXT': '#d2d2d3',
                'INPUT': '#3d3f46',
                'TEXT_INPUT': '#d2d2d3',
                'SCROLL': '#c7e78b',
                'BUTTON': ('#6fb97e', '#313641'),
                'PROGRESS': ('#778eca', '#6fb97e'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

# Add your dictionary to the PySimpleGUI themes
sg.theme_add_new('MyGreen', my_new_theme)

# Switch your theme to use the newly added one. You can add spaces to make it more readable
sg.theme("MyGreen")

combo_list = ["all",".xls",".docx",".pak",".csv",".xml",".zip",".pdf",".txt",".jar",".jpg",".png",".icon"]

frame_output_window = [[sg.Multiline(write_only=True,size=(90, 10), key="-OUTPUT_WINDOW-")]]
frame_layout_one = [[sg.Text("Main Settings", font="Arial 20 bold underline",text_color="#6fb97e")],
        [sg.Text("Source Path is used for the Folder Observer and for Listing Files in the Path.")],
        [sg.Text("Select Folder to watch for:"),sg.Input(do_not_clear=True,key="-PATH_INPUT-"), sg.FolderBrowse()],
        [sg.Text("Select a specific file type to list or move:"), sg.Combo(combo_list, default_value= "all", size=(5, 5),key="-EXTENSION_TYPE-"),sg.Button("List files",tooltip="List all Files that the Folder Observer is watching.")]]
frame_layout_three = [[sg.Text("Folder Observer Main", font="Arial 20 bold underline",text_color="#6fb97e")],
        [sg.Text("Monitoring the specified Watching Path (5min) for new Files and listing them in the Output Window.")],
        [sg.Button("Clear Output Window",tooltip="Clears main output Window."),sg.Text("|"),sg.Button("Start",tooltip="Starts the Folder Observer"), sg.Button("Stop",tooltip="Stops the Folder Observer"),sg.Button("Move"),sg.Text("|"),sg.Text("Folder Observer Status:"),sg.StatusBar("Waiting for an Event",text_color="#778eca",key="-OBSERVER_STATUS-", size=(22,1)),sg.Button("Exit",size=(8,1),tooltip="Exit the Program.", expand_x=True)]]
frame_layout_two = [[sg.Text("Optional: Moving files from Source Path to the set Moving Path.")],
        [sg.Text("Select Folder to move to:"),sg.Input(do_not_clear=True, key="-MOVE_INPUT-", size=(47,5)),sg.FolderBrowse()]]
frame_layout_move_button = [[sg.Text("Confirm moving of Files?"), sg.Button("Move Files"),sg.Button("Switch Move/Watch")]]

layout = [[sg.Column(frame_layout_one)],
        [sg.Column(frame_layout_two)],
        [sg.Column(frame_layout_move_button)],
        [sg.HSeparator()],
        [sg.Column(frame_layout_three)],
        [sg.Column(frame_output_window)]]

    #----Execution of Functions and the Workflow Code of the Program----#

window = sg.Window("Compliance Checker", layout, font = "Roboto 16",resizable=True,finalize=True)

# Event loop to process "events" and get the "values" of the inputs
stop = False
while True:
    
    event,values = window.read(timeout=1)
    
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    
    watchingPath = values["-PATH_INPUT-"]
    move_file_to_new_dest = values["-MOVE_INPUT-"]
    ends_with = values["-EXTENSION_TYPE-"]
    
    
     #----START Folder Observer starting code START----#
    if event == "Start":
        if len(watchingPath) > 0:
            window["-OBSERVER_STATUS-"].update("Observer has started", text_color="#6fb97e")
            stop = False
            window.perform_long_operation(lambda: file_observer(watchingPath, pollTime),"-OUTPUT_WINDOW-")
            window["-OUTPUT_WINDOW-"].print(">>> Observer successfully started.")
        else:
            window["-OBSERVER_STATUS-"].update("Error: No folder path set", text_color="red")
            window["-OUTPUT_WINDOW-"].print(">>> Error: Please select a Folder above for the Observer to watch.")

    if event == "Stop":
        if len(watchingPath) > 0:
            window["-OBSERVER_STATUS-"].update("Observer has stopped", text_color="red")
            window["-PATH_INPUT-"].update("")
            window["-OUTPUT_WINDOW-"].print(">>> Observer successfully stopped.")
            stop = True
        else:
            window["-OBSERVER_STATUS-"].update("Error: No folder path set", text_color="red")
            window["-OUTPUT_WINDOW-"].print(">>> Error: Please select a Folder above for the Observer to watch.")
            
    #----END Folder Observer starting code END----#
            
    #----START For clearing the main output window START----#
    if event == "Clear Output Window":
        window["-OUTPUT_WINDOW-"].update("")
        window["-OBSERVER_STATUS-"].update("Waiting for an Event", text_color="#778eca")
    #----END For clearing the main output window END----#
    
    #---- START Moving Files Button START ----#
    if event == "Move Files":
        if len(move_file_to_new_dest) > 0 and len(watchingPath) > 0:
             window.perform_long_operation(lambda: move_all_file_to_new_destination(ends_with,move_file_to_new_dest, watchingPath),"-OUTPUT_WINDOW-")
        else:
            window["-OUTPUT_WINDOW-"].print(">>> No Watching and Moving path set, running on errors. Please set both paths.")
     #---- END Moving Files Button END ----#
     
     #----- START Folder Observer button to move the file that the Observer caught START ----#
    if event == "Move":
        try:
            file_name_with_extension
        except NameError:
            window["-OUTPUT_WINDOW-"].print(">>> Error, can't move nothing!")
        else:
            if len(move_file_to_new_dest) == 0:
                window["-OUTPUT_WINDOW-"].print(">>> Error, the move path input is empty!")
            else:
                window.perform_long_operation(lambda: move_single_file_to_new_destination(move_file_to_new_dest, watchingPath),"-OUTPUT_WINDOW-")
     #----- END Folder Observer button to move the file that the Observer caught END----#
    
     #----START List all files in the directory that you're watching START----#       
    if event == "List files":
        if len(watchingPath) > 0 and ends_with == "all":
            window["-OUTPUT_WINDOW-"].print(list_all_files_in_directory(watchingPath))
        elif ends_with == ".xls" and len(watchingPath) > 0:
            window["-OUTPUT_WINDOW-"].print(f">>> Files with filetype: {ends_with}")
            window.perform_long_operation(lambda: file_type (ends_with, watchingPath),"-OUTPUT_WINDOW")
        elif ends_with == ".xml" and len(watchingPath) > 0:
            window["-OUTPUT_WINDOW-"].print(f">>> Files with filetype: {ends_with}")
            window.perform_long_operation(lambda: file_type (ends_with, watchingPath),"-OUTPUT_WINDOW")
        elif ends_with == ".zip" and len(watchingPath) > 0:
            window["-OUTPUT_WINDOW-"].print(f">>> Files with filetype: {ends_with}")
            window.perform_long_operation(lambda: file_type (ends_with, watchingPath),"-OUTPUT_WINDOW")
        elif ends_with == ".pdf" and len(watchingPath) > 0:
            window["-OUTPUT_WINDOW-"].print(f">>> Files with filetype: {ends_with}")
            window.perform_long_operation(lambda: file_type (ends_with, watchingPath),"-OUTPUT_WINDOW")
        elif ends_with == ".pak" and len(watchingPath) > 0:
            window["-OUTPUT_WINDOW-"].print(f">>> Files with filetype: {ends_with}")
            window.perform_long_operation(lambda: file_type (ends_with, watchingPath),"-OUTPUT_WINDOW")
        elif ends_with == ".jar" and len(watchingPath) > 0:
            window["-OUTPUT_WINDOW-"].print(f">>> Files with filetype: {ends_with}")
            window.perform_long_operation(lambda: file_type (ends_with, watchingPath),"-OUTPUT_WINDOW")
        elif ends_with == ".txt" and len(watchingPath) > 0:
            window["-OUTPUT_WINDOW-"].print(f">>> Files with filetype: {ends_with}")
            window.perform_long_operation(lambda: file_type (ends_with, watchingPath),"-OUTPUT_WINDOW")
        elif ends_with == ".jpg" and len(watchingPath) > 0:
            window["-OUTPUT_WINDOW-"].print(f">>> Files with filetype: {ends_with}")
            window.perform_long_operation(lambda: file_type (ends_with, watchingPath),"-OUTPUT_WINDOW")
        elif ends_with == ".png" and len(watchingPath) > 0:
            window["-OUTPUT_WINDOW-"].print(f">>> Files with filetype: {ends_with}")
            window.perform_long_operation(lambda: file_type (ends_with, watchingPath),"-OUTPUT_WINDOW")
        elif ends_with == ".csv" and len(watchingPath) > 0:
            window["-OUTPUT_WINDOW-"].print(f">>> Files with filetype: {ends_with}")
            window.perform_long_operation(lambda: file_type (ends_with, watchingPath),"-OUTPUT_WINDOW")
        elif ends_with == ".icon" and len(watchingPath) > 0:
            window["-OUTPUT_WINDOW-"].print(f">>> Files with filetype: {ends_with}")
            window.perform_long_operation(lambda: file_type (ends_with, watchingPath),"-OUTPUT_WINDOW")
        elif ends_with == ".docx" and len(watchingPath) > 0:
            window["-OUTPUT_WINDOW-"].print(f">>> Files with filetype: {ends_with}")
            window.perform_long_operation(lambda: file_type (ends_with, watchingPath),"-OUTPUT_WINDOW")
        elif ends_with == "" and len(watchingPath) > 0:
            window["-OUTPUT_WINDOW-"].print(f">>> Error, use the listbox to set a filetype to look for.")
        else:
            window["-OUTPUT_WINDOW-"].print(">>> No path set, running on errors :)")
    #----END List all files in the directory that you're watching END----#
    
    #----START Swapping Watching folder path with Move folder path event START----#
    if event == "Switch Move/Watch" and len(move_file_to_new_dest) > 0 and len (watchingPath) > 0:
        window["-PATH_INPUT-"].update(move_file_to_new_dest)
        window["-MOVE_INPUT-"].update(watchingPath)
    #----END Swapping Watching folder path with Move folder path event END----#   
