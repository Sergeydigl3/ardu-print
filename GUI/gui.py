import os
import customtkinter as tk
from PIL import ImageTk, Image
from customtkinter import CTkImage
from customtkinter import StringVar 
import serial
import cv2
from tqdm import tqdm
# tk.deactivate_automatic_dpi_awareness()
tk.set_widget_scaling(100.0) 
tk.set_window_scaling(100.0)

# read com port from text file
with open("comport.txt", "r") as f:
    comport_file = f.read()
    print(comport_file)


ser = serial.Serial(comport_file, 200000)

target_x = 320
target_y = 240

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

class ToplevelWindow(tk.CTkToplevel):
    def init(self,*args, photo_path=None,**kwargs):
        super().init(*args, **kwargs)
        self.geometry("400x400")
        self.photo_path = photo_path
        self.send_button = tk.CTkButton(self, text="Send", command=self.on_send_button_click)
        self.send_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.label = tk.CTkLabel(self, text=photo_path )
        self.label.pack(padx=20, pady=20)

        # Load the image and pack without title
        self.image = Image.open(photo_path)
        self.photo = ImageTk.PhotoImage(self.image, )
        self.image_label = tk.CTkLabel(self, text="",image=self.photo)
        self.image_label.pack(padx=20, pady=20)
        

    def on_send_button_click(self):
        print(f"Sending data: {self.photo_path}")
        img = cv2.imread(self.photo_path)
        img = process_img(img)

        for x in tqdm(range(target_x-1, -1, -1)):
            for y in range(0, target_y):
                
                color2 = img[y][x][::-1].tobytes()
                ser.write(color2)
            
    

        # Add code here to send the data


class PhotoGallery(tk.CTkScrollableFrame):
    def init(self, master, folder_path, **kwargs):

        super().init(master, **kwargs)

        self.folder_path = folder_path
        self.photo_list = []
        self.photo_button_list = []
        self.toplevel_window = None
        self.load_photos()

    def load_photos(self):
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith(".jpg") or file_name.endswith(".png"):
                photo_path = os.path.join(self.folder_path, file_name)
                photo = Image.open(photo_path)
                photo.thumbnail((200, 200))
                photo_tk = ImageTk.PhotoImage(photo)
                self.photo_list.append(photo_tk)
                self.add_photo_button(photo_tk, photo_path)

    def add_photo_button(self, photo_tk, photo_path):
        photo_button = tk.CTkButton(self, image=photo_tk, command=lambda: self.on_photo_button_click(photo_tk, photo_path))
        photo_button.grid(row=len(self.photo_button_list), column=0, pady=(0, 10))
        self.photo_button_list.append(photo_button)

    def on_photo_button_click(self, photo_tk, photo_path):
        print(f"Opening photo: {photo_tk}")
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self, photo_path=photo_path)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus() 
        # Add code here to open the selected photo


    def get_selected_photos(self):
        return [photo_tk for photo_tk in self.photo_list if photo_tk in [photo_button.cget("image") for photo_button in self.photo_button_list]]


    

    
# Example usage
root = tk.CTk()

folder_path = "."
gallery = PhotoGallery(root, folder_path)

gallery.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
root.mainloop()