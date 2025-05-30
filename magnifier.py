import time
import tkinter as tk
from PIL import Image,ImageTk
from picamera2 import Picamera2

ZOOMFACTOR=2.0 

camera = Picamera2()
camera.preview_configuration.main.size = (1920, 1080)
camera.preview_configuration.main.format = "RGB888"
camera.configure("preview")
camera.start()
print ("camera starting.. please wait..")
time.sleep(2)
camera.set_controls({"AwbEnable" : False, "ColourTemperature" : 4000})


root=tk.Tk()
root.attributes("-fullscreen", True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

label = tk.Label(root)
label.pack()

overlay = Image.open("/home/russell/MagnifiedFrame.png").convert("RGBA")

def zoom_center(image: Image.Image,zoom:float) -> Image.Image:
	w, h = image.size
	crop_w = int(w / zoom)
	crop_h = int(h / zoom)
	left = (w - crop_w) // 2
	top = (h - crop_h) // 2
	cropped = image.crop((left, top, left + crop_w, top + crop_h))
	return cropped.resize((w, h), Image.LANCZOS)
	
def update_image():
	img = camera.capture_array()
	pil_image = Image.fromarray(img).convert("RGBA")
	
	zoomed = zoom_center(pil_image, ZOOMFACTOR)

	if overlay.size != zoomed.size:
		frame = overlay.resize(zoomed.size)
	else:
		frame = overlay

	composed = Image.alpha_composite(zoomed, frame)
	composed_resized = composed.resize((screen_width, screen_height), Image.LANCZOS)
	
	tk_img = ImageTk.PhotoImage(composed_resized)
	label.config(image=tk_img)
	label.image = tk_img
	root.after(5000, update_image)

def on_key(event):
	if event.char.lower() == "q":
		root.destroy()

root.bind("<Key>", on_key)
root.after(0, update_image)
root.mainloop()
