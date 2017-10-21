import tkinter as tk

import cv2
import numpy as np
from PIL import ImageTk, Image

global points, window, u_in
points = []


def get_origin(eventorigin):
    global points, window
    x = eventorigin.x
    y = eventorigin.y
    points.append([x, y])
    if len(points) == 4:
        window.quit()
        window.destroy()


def get_input():
    global u_in
    u_in = entry.get()
    window.quit()


if __name__ == '__main__':
    window = tk.Tk()

    # path = "./sample.jpg"
    entry = tk.Entry(window)
    btn = tk.Button(window, command=get_input)
    entry.pack()
    btn.pack()
    window.mainloop()
    # entry.
    img = ImageTk.PhotoImage(Image.open(u_in))

    label = tk.Label(image=img)
    label.image = img  # keep a reference!
    label.pack()

    label.bind("<Button 1>", get_origin)
    window.mainloop()

    min_x = min([x[0] for x in points])
    min_y = min([x[1] for x in points])
    max_x = max([x[0] for x in points])
    max_y = max([x[1] for x in points])

    pts1 = np.float32(points)
    pts2 = np.float32([[min_x, min_y], [min_x, max_y], [max_x, min_y], [max_x, max_y]])

    M = cv2.getPerspectiveTransform(pts1, pts2)

    img = cv2.imread(u_in)
    dst = cv2.warpPerspective(img, M, (max_x + 100, max_y + 100))

    img_path = u_in.rsplit(".", 1)
    cv2.imwrite(img_path[-2] + "_out." + img_path[-1], dst)
    exit(0)
