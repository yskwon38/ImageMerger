import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import *
from tkinter import filedialog
from PIL import Image
import keyboard
from PIL import ImageGrab
import os
import time

root = Tk()
root.title("Image Merger")

# File Frame (adding files, deleting files)
file_frame = Frame(root)
file_frame.pack(fill = "both", padx = 5, pady = 5)

def add_file():
    files = filedialog.askopenfilenames(title = "Select Image Files", \
        filetypes = (("PNG", "*.png"), ("All", "*.*")), \
        initialdir = r"C:/")

    for file in files:
        list_file.insert(END, file)


def delete_file():
    print(list_file.curselection())

    for index in reversed(list_file.curselection()):
        list_file.delete(index)

def saving_path():
    folder = filedialog.askdirectory()
    if folder == "":
        return
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(END, folder)

def merge_image():
    try:
        # check width
        img_width = width_combo.get()
        if (img_width == "Original"):
            img_width = -1
        else:
            img_width = int(img_width)

        # check padding
        img_padding = padding_combo.get()
        if img_padding == "Narrow":
            img_padding = 30
        elif img_padding == "Normal":
            img_padding = 60
        elif img_padding == "Wide":
            img_padding = 90
        else:
            img_padding = 0

        # check format
        img_format = format_combo.get().upper()

        #############################################

        image = [Image.open(x) for x in list_file.get(0, END)]

        image_size = []
    
        # orig. width : orig. height = altered width : altered height
        # altered height = orig. height * altered width / orig. width

        if img_width > -1:
            image_size = [(int(img_width), int(img_width * x.size[1] / x.size[0])) for x in image]
        else:
            image_size = [(x.size[0], x.size[1]) for x in image]


        width, height = zip(*(image_size))

        max_width = max(width)
        total_height = sum(height)
        # adding paddings to the height
        if img_padding > 0:
            total_height += (img_padding * (len(image) - 1))

        merged_img = Image.new("RGB", (max_width, total_height), (255, 255, 255))
        y_offset = 0

        for idx, img in enumerate(image):
            if img_width > -1:
                img = img.resize(image_size[idx])

            merged_img.paste(img, (0, y_offset))
            y_offset += (img.size[1] + img_padding) # height of image + user set padding

            progress = ((idx + 1) / len(image)) * 100 # calculating percentage completed
            progress_var.set(progress)
            progress_bar.update()

        curr_time = time.strftime("_%Y%m%d_%H%M%S")
        save_name = "image{}.".format(curr_time) + img_format
        dest_path = os.path.join(txt_dest_path.get(), save_name)
        merged_img.save(dest_path)
        msgbox.showinfo("Alert", "Successfully merged!")
    except Exception as err:
        msgbox.showerror("Error", err)


def start():
    # first check all the options
    #print("Width: ", width_combo.get())
    #print("Padding: ", padding_combo.get())
    #print("Format: ", format_combo.get())

    # check if file list is empty
    if list_file.size() == 0:
        msgbox.showwarning("Warning", "Please add image file to be merged")
        return
    if len(txt_dest_path.get()) == 0:
        msgbox.showwarning("Warning", "Please select a folder to save to")
        return

    # now start image merging
    merge_image()


def screenshot():
    curr_time = time.strftime("_%Y%m%d_%H%M%S")
    img = ImageGrab.grab()
    img.save("screencap{}.png".format(curr_time))
    msgbox.showinfo("Alert", "Screencapture has been saved")

#file add button
btn_add_file = Button(file_frame, padx = 5, pady = 5, width = 15, text = "Add Files", command = add_file)
btn_add_file.pack(side = "left")
#file delete button
btn_delete_file = Button(file_frame, padx = 5, pady = 5, width = 15, text = "Delete Files", command = delete_file)
btn_delete_file.pack(side = "right")
#screenshot button
btn_screenshot = Button(file_frame, padx = 5, pady = 5, width = 15, text = "Screenshot", command = screenshot)
btn_screenshot.pack()


#List Frame to show added files
list_frame = Frame(root)
list_frame.pack(fill = "both", padx = 5, pady = 5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side = "right", fill = "y")

list_file = Listbox(list_frame, selectmode = "extended", height = 15, yscrollcommand = scrollbar.set)
list_file.pack(side = "left", fill = "both", expand = 1)
scrollbar.configure(command = list_file.yview)

#save path frame
path_frame = LabelFrame(root, text = "Save Path")
path_frame.pack(fill = "both", padx = 5, pady = 5, ipady = 5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side = "left", fill = "x", expand = 1, ipady = 4, padx = 5, pady = 5)

btn_dest_path = Button(path_frame, text = "Select Folder", width = 10, command = saving_path)
btn_dest_path.pack(side = "right", padx = 5, pady = 5)

#settings frame
setting_frame = LabelFrame(root, text = "Settings")
setting_frame.pack(padx = 5, pady = 5, ipady = 5)

# width option Label
width_option = Label(setting_frame, text = "Width", width = 5)
width_option.pack(side = "left", padx = 5, pady = 5)
# width option combo
width_values = ["Original", "1920", "1024", "800", "640"]
width_combo = ttk.Combobox(setting_frame, state = "readonly", values = width_values, width = 10)
width_combo.current(0)
width_combo.pack(side = "left", padx = 5, pady = 5)

# paddings between images Label
padding_option = Label(setting_frame, text = "Padding", width = 8)
padding_option.pack(side = "left", padx = 5, pady = 5)
# paddings option combo
padding_values = ["None", "Narrow", "Normal", "Wide"]
padding_combo = ttk.Combobox(setting_frame, state = "readonly", values = padding_values, width = 10)
padding_combo.current(0)
padding_combo.pack(side = "left", padx = 5, pady = 5)

# file format Label
format_option = Label(setting_frame, text = "Format", width = 6)
format_option.pack(side = "left", padx = 5, pady = 5)
# file format combo
format_values = ["PNG", "JPG", "BMP"]
format_combo = ttk.Combobox(setting_frame, state = "readonly", values = format_values, width = 10)
format_combo.current(0)
format_combo.pack(side = "left", padx = 5, pady = 5)

# progress bar
progress_frame = LabelFrame(root, text = "Progress")
progress_frame.pack(fill = "both", padx = 5, pady = 5, ipady = 5)

progress_var = DoubleVar()
progress_bar = ttk.Progressbar(progress_frame, variable = progress_var)
progress_bar.pack(fill = "both", padx = 5, pady = 5)

# running frame
running_frame = Frame(root)
running_frame.pack(fill = "both", padx = 5, pady = 5, ipady = 5)


btn_close = Button(running_frame, padx = 5, pady = 5, text = "Close", width = 10, command = root.quit)
btn_close.pack(side = "right", padx = 5, pady = 5)
btn_start = Button(running_frame, padx = 5, pady = 5, text = "Start", width = 10, command = start)
btn_start.pack(side = "right", padx = 5, pady = 5)

root.resizable(0, 0)
root.mainloop()

