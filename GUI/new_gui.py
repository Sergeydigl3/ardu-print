import customtkinter
import os
import cv2
from tqdm import tqdm
from PIL import Image, ImageTk

import serial
from tkinter import StringVar, filedialog, IntVar
from numba import jit
import numpy as np
import time

target_x = 320
target_y = 240

target_x_milandr = 128
target_y_milandr = 64

serial_port = None

def process_img(image, invert=False):
    frame = image
    
    height, width, channels = frame.shape
    if height > width:
        # Rotate the image by 90 degrees counter-clockwise
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    frame = cv2.resize(frame, (target_x, target_y), fx=0, fy=0,
                       interpolation=cv2.INTER_CUBIC)
    if invert:
        frame = cv2.bitwise_not(frame)
    bit16frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGR565)
    return bit16frame

@jit(nopython=True)
def floyd_steinberg(image):
    # image: np.array of shape (height, width), dtype=float, 0.0-1.0
    # works in-place!
    h, w = image.shape
    for y in range(h):
        for x in range(w):
            old = image[y, x]
            new = np.round(old)
            image[y, x] = new
            error = old - new
            # precomputing the constants helps
            if x + 1 < w:
                image[y, x + 1] += error * 0.4375  # right, 7 / 16
            if (y + 1 < h) and (x + 1 < w):
                image[y + 1, x + 1] += error * 0.0625  # right, down, 1 / 16
            if y + 1 < h:
                image[y + 1, x] += error * 0.3125  # down, 5 / 16
            if (x - 1 >= 0) and (y + 1 < h):
                image[y + 1, x - 1] += error * 0.1875  # left, down, 3 / 16
    return image

def no_dither(image):
    # image: np.array of shape (height, width), dtype=float, 0.0-1.0
    # works in-place!
    h, w = image.shape
    for y in range(h):
        for x in range(w):
            image[y, x] = 1.0 - image[y, x] # round(image[y, x])
    return image


def pil_to_np(pilimage):
    return np.array(pilimage) / 255


def np_to_pil(image):
    return Image.fromarray((image * 255).astype('uint8'))

# def process_img_millandr_old(image, invert=False):
#     frame = image
    
#     height, width, channels = frame.shape
#     if height > width:
#         # Rotate the image by 90 degrees counter-clockwise
#         frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
#     frame = cv2.resize(frame, (target_x_milandr, target_y_milandr), fx=0, fy=0,
#                        interpolation=cv2.INTER_CUBIC)
#     if invert:
#         frame = cv2.bitwise_not(frame)
#     # bit8frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGR565)

    
def process_img_millandr(image, invert=False):
    frame = image.copy()
    
    height, width, channels = frame.shape
    if height > width:
        # Rotate the image by 90 degrees counter-clockwise
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    frame = cv2.resize(frame, (target_x_milandr, target_y_milandr), fx=0, fy=0,
                       interpolation=cv2.INTER_CUBIC)
    # if invert:
    #     frame = cv2.bitwise_not(frame)
    # bit8frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGR565)


   
    return frame

class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self,*args, photo_path=None,**kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x300")
        self.photo_path = photo_path
        self.send_button = customtkinter.CTkButton(self, text="Send", command=self.on_send_button_click)
        self.send_button.pack(side=customtkinter.LEFT, padx=20, pady=20)

        self.label = customtkinter.CTkLabel(self, text=photo_path )
        self.label.pack(padx=20, pady=20)

        # Load the image and pack without title
        self.image = Image.open(photo_path)
        self.image.thumbnail((300, 300))
        self.photo = ImageTk.PhotoImage(self.image, )
        
        self.image_label = customtkinter.CTkLabel(self, text="",image=self.photo)
        self.image_label.pack(padx=20, pady=20)
        

    def on_send_button_click(self):
        print(f"Sending data: {self.photo_path}")
        img = cv2.imread(self.photo_path)
        img = process_img(img)

        for x in tqdm(range(target_x-1, -1, -1)):
            for y in range(0, target_y):
                
                color2 = img[y][x][::-1].tobytes()
                serial_port.write(color2)
            
    

        # Add code here to send the data

class MilandrToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self,*args, photo_path=None,**kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x300")
        self.photo_path = photo_path
        self.send_button = customtkinter.CTkButton(self, text="Send", command=self.on_send_button_click)
        self.send_button.pack(side=customtkinter.LEFT, padx=20, pady=20)

        self.label = customtkinter.CTkLabel(self, text=photo_path )
        self.label.pack(padx=20, pady=20)

        # Load the image and pack without title
        self.image = Image.open(photo_path)
        self.image.thumbnail((300, 300))
        self.photo = ImageTk.PhotoImage(self.image, )
        
        self.image_label = customtkinter.CTkLabel(self, text="",image=self.photo)
        self.image_label.pack(padx=20, pady=20)
        

    def on_send_button_click(self):
        print(f"Sending data: {self.photo_path}")
        img = cv2.imread(self.photo_path)
        img = process_img_millandr(img)
        cv2.imwrite("temp.jpg", img)



        img = Image.open("temp.jpg").convert('L')
        img_array = pil_to_np(img)
        new_img = floyd_steinberg(img_array)
        new_img = no_dither(new_img)
        new_img_pil = np_to_pil(new_img)
        new_img_pil.save("testttt.jpg")


        image = Image.open("testttt.jpg").convert('L')

        image = np.array(image) / 255
        image = image.astype(int)
        image = np.split(image, 8, axis=0)
        image = [byte for row in image for byte in np.packbits(
            row, axis=0, bitorder='little')]
        image = np.array(image).reshape(8, 128)
        arr = ', '.join(', '.join('0x{:02x}'.format(byte)
                        for byte in row) for row in image)
        arr_str = '{' + arr + '}'
        print(arr_str)
        images = [arr_str]

        arr = f'#define FRAMES_COUNT {images.__len__()}\n\n'
        arr += f'const uint8_t frames[FRAMES_COUNT][{128 * 8}] = ' + '{\n'
        arr += '\t' + arr_str + ',\n'
        arr += '};\n'
        
        with open("frames.h", 'w', encoding='utf-8') as f:
            f.write(arr)


        with open("base/Main.c", 'r', encoding='utf-8') as f:
            base = f.read()
        
        with open("flash/display/user/Main.c", 'w', encoding='utf-8') as f:
            # f.write("  ")
            base = base.replace("<codeblock>", arr_str+";")
            f.write(base)

        os.system("C:\\Keil_v5\\UV4\\UV4.exe -b C:\\codePack\\kursach\GUI\\flash\\display\\display.uvprojx")

        time.sleep(2)

        os.system("C:\\Keil_v5\\UV4\\UV4.exe -f C:\\codePack\\kursach\GUI\\flash\\display\\display.uvprojx")
        # new_img_pil.save(f'{folder}/{i}')

        # img = cv2.imread(self.photo_path)
        # img = process_img_millandr(img)
        # cv2.imwrite("temp.jpg", img)

        # img = Image.open("temp.jpg").convert('L')
        # img_array = pil_to_np(img)
        # new_img = floyd_steinberg(img_array)
        # img.close()
        # img = no_dither(new_img)
        # # new_img_pil = np_to_pil(new_img)
        # # new_img_pil.save(f'{folder}/{i}')

        # image = np.split(img, 8, axis=0)
        # # for x in tqdm(range(target_x-1, -1, -1)):
        # #     for y in range(0, target_y):
                
        # #         color2 = img[y][x][::-1].tobytes()
        # #         serial_port.write(color2)
            













        # image = [byte for row in image for byte in np.packbits(
        # row, axis=0, bitorder='little')]
        # image = np.array(image).reshape(8, 128)
        # arr = ', '.join(', '.join('0x{:02x}'.format(byte)
        #             for byte in row) for row in image)
        # print( '{' + arr + '}')

        # Add code here to send the data



class PhotoGallery(customtkinter.CTkScrollableFrame):
    def __init__(self, master, folder_path, board_type, **kwargs):

        super().__init__(master, **kwargs)

        self.folder_path = folder_path
        self.board_type = board_type
        self.photo_list = []
        self.photo_button_list = []
        self.toplevel_window = None
        self.load_photos()

    def load_photos(self):
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith(".jpg") or file_name.endswith(".png"):
                photo_path = os.path.join(self.folder_path, file_name)
                photo = Image.open(photo_path)
                photo.thumbnail((400, 400))
                photo_tk = ImageTk.PhotoImage(photo)
                self.photo_list.append(photo_tk)
                self.add_photo_button(photo_tk, photo_path)

    def add_photo_button(self, photo_tk, photo_path):
        photo_button = customtkinter.CTkButton(self, image=photo_tk, text=photo_path, command=lambda: self.on_photo_button_click(photo_tk, photo_path), anchor="w", compound="top")
        photo_button.grid(row=len(self.photo_button_list), column=0, pady=(0, 10), sticky="ew")
        self.photo_button_list.append(photo_button)

    def on_photo_button_click(self, photo_tk, photo_path):
        # if not (self.board_type.get() == 2 and serial_port and serial_port.is_open):
        #     print("Serial port not open")
        #     return

        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            if self.board_type.get() == 2:
                self.toplevel_window = ToplevelWindow(self, photo_path=photo_path)  # create window if its None or destroyed
            elif self.board_type.get() == 1:
                print("Milandr board")
                self.toplevel_window = MilandrToplevelWindow(self, photo_path=photo_path)
            self.toplevel_window.focus()  # focus the window
        else:
            self.toplevel_window.focus() 
        # Add code here to open the selected photo


    def get_selected_photos(self):
        return [photo_tk for photo_tk in self.photo_list if photo_tk in [photo_button.cget("image") for photo_button in self.photo_button_list]]

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.var_comport = StringVar(value="COM4")
        self.var_keil_path = StringVar(value="C:\\Keil_v5\\UV4\\UV4.exe")
        self.second_frame_radio_var = IntVar()
        self.second_frame_radio_var.set(2)
        self.title("image_example.py")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        # self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
        #                                          dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Image Example", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.settings_frame = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Settings",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.settings_frame_event)
        self.settings_frame.grid(row=2, column=0, sticky="ew")

        # self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
        #                                               fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
        #                                               image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        # self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        self.home_frame.grid_rowconfigure(1, weight=1)
        # self.home_frame.grid(sticky="nsew")
        
        self.home_frame_label = customtkinter.CTkLabel(self.home_frame, text="Home", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.home_frame_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.home_frame_gallery = PhotoGallery(self.home_frame, folder_path=".", board_type=self.second_frame_radio_var)
        self.home_frame_gallery.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")


        
        

        
        
        # self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        # self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        # self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="", image=self.image_icon_image)
        # self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        # self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="right")
        # self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="top")
        # self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        # self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="CTkButton", image=self.image_icon_image, compound="bottom", anchor="w")
        # self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)
        self.second_frame.grid_rowconfigure(5, weight=1)

        self.second_frame_label = customtkinter.CTkLabel(self.second_frame, text="Settings", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.second_frame_label.grid(row=0, column=0, padx=20, pady=10)

        
        self.second_frame_input_field = customtkinter.CTkEntry(self.second_frame, textvariable = self.var_comport, placeholder_text="Com port")
        self.second_frame_input_field.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.second_frame_input_connect_btn = customtkinter.CTkButton(self.second_frame, text="Connect", compound="right", command=self.second_frame_connect_button_event)
        self.second_frame_input_connect_btn.grid(row=1, column=1, padx=0, pady=10)
        self.second_frame_input_disconnect_btn = customtkinter.CTkButton(self.second_frame, text="Disconnect", compound="right", state="disabled" , command=self.second_frame_disconnect_button_event)
        self.second_frame_input_disconnect_btn.grid(row=1, column=2, padx=10, pady=10)

        self.second_frame_keil_path_input_field = customtkinter.CTkEntry(self.second_frame, textvariable = self.var_keil_path, placeholder_text="Keil path")
        self.second_frame_keil_path_input_field.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.second_frame_keil_path_input_field_btn = customtkinter.CTkButton(self.second_frame, text="Browse", compound="right", command=self.second_frame_browse_button_event)
        self.second_frame_keil_path_input_field_btn.grid(row=2, column=1, padx=0, pady=10)

        self.second_frame_select_board_label = customtkinter.CTkLabel(self.second_frame, text="Select board", font=customtkinter.CTkFont(size=10, weight="bold"))
        self.second_frame_select_board_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        # Milandr board and Arduino board radio buttons
        self.second_frame_radio_1 = customtkinter.CTkRadioButton(self.second_frame, text="Milandr board", variable=self.second_frame_radio_var, value=1, command=self.radiobutton_event)
        self.second_frame_radio_1.grid(row=4, column=0, padx=30, pady=10, sticky="w")
        self.second_frame_radio_2 = customtkinter.CTkRadioButton(self.second_frame, text="Arduino board", variable=self.second_frame_radio_var, value=2, command=self.radiobutton_event)
        self.second_frame_radio_2.grid(row=4, column=1, padx=0, pady=10, sticky="e")

        # right bottom button save
        self.second_frame_save_btn = customtkinter.CTkButton(self.second_frame, text="Save", compound="right",)
        self.second_frame_save_btn.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        # create third frame
        # self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def second_frame_browse_button_event(self):
        value = filedialog.askopenfile(initialdir=self.var_keil_path.get(),title = "Select file",filetypes = (("exe files","*.exe"),("all files","*.*")))
        if value:
            self.var_keil_path.set(value)

    def radiobutton_event(self):
        if self.second_frame_radio_var.get() == 1: # Milandr board
            self.second_frame_disconnect_button_event()

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.settings_frame.configure(fg_color=("gray75", "gray25") if name == "settings" else "transparent")
        # self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "settings":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        # if name == "frame_3":
        #     self.third_frame.grid(row=0, column=1, sticky="nsew")
        # else:
        #     self.third_frame.grid_forget()
    
    def second_frame_connect_button_event(self):
        global serial_port
        print("Connect button pressed")
        self.second_frame_input_connect_btn.configure(state="disabled")
        try:
            serial_port = serial.Serial(self.var_comport.get(), 200000)
            self.second_frame_input_disconnect_btn.configure(state="normal")
            self.second_frame_radio_var.set(2)
        except:
            print("Error opening serial port")
            self.second_frame_input_connect_btn.configure(state="normal")

    def second_frame_disconnect_button_event(self):
        print("Disconnect button pressed")
        self.second_frame_input_disconnect_btn.configure(state="disabled")
        try:
            serial_port.close()
            self.second_frame_input_connect_btn.configure(state="normal")
        except:
            print("Error closing serial port")
            self.second_frame_input_disconnect_btn.configure(state="normal")
            

    def home_button_event(self):
        self.select_frame_by_name("home")

    def settings_frame_event(self):
        self.select_frame_by_name("settings")

    # def frame_3_button_event(self):
    #     self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()