import tkinter
import threading
import imageio
from PIL import Image, ImageTk

video_name = 'F:\\未备备，未整理未更名，未备注，唯一 MP4_1539files\\1521470065008.mp4'
video = imageio.get_reader(video_name)

def stream(label):

    frame = 0
    for image in video.iter_data():
        frame += 1                                    #counter to save new frame number
        image_frame = Image.fromarray(image)
        image_frame.save('frame_%d.png' % frame)      #if you need the frame you can save each frame to hd
        frame_image = ImageTk.PhotoImage(image_frame)
        label.config(image=frame_image)
        label.image = frame_image
        if frame == 1: break                         #after 40 frames stop, or remove this line for the entire video

if __name__ == "__main__":

    root = tkinter.Tk()
    my_label = tkinter.Label(root)
    my_label.pack()
    thread = threading.Thread(target=stream, args=(my_label,))
    thread.daemon = 1
    thread.start()
    root.mainloop()