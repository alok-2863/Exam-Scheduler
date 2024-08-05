import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, filedialog, messagebox
import time
import smtplib
from itertools import permutations
import math
import firebase_admin
from firebase_admin import credentials, db
import random
import pandas as pd
from openpyxl import load_workbook
from tkinter.messagebox import showerror
import threading
from PIL import Image, ImageDraw, ImageFont, ImageTk
import socket
import os, sys
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

sys.stdout.reconfigure(encoding="utf-8")

internet = True 


def check_no_internet_access():
    """
     Check to see if we can connect to the internet. This is useful for tests that care about network connectivity.
     
     @return True if we can connect to the internet False otherwise
    """
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=1)
        return True
    except OSError:
        return False


def internet_connection():
    """
     This function creates a Tkinter window to connect to internet. If there is no internet access it returns None
    """
    # Check if there is no internet connection.
    if check_no_internet_access():
        one()
    else:
        root = tk.Tk()
        root.title("No Internet")
        root.overrideredirect(True)
        width = 500
        height = 600
        screen_width, screen_height = (
            root.winfo_screenwidth(),
            root.winfo_screenheight(),
        )
        x, y = int((screen_width / 2) - (width / 2)), int(
            (screen_height / 2) - (height / 2)
        )
        root.geometry(f"{width}x{height}+{x}+{y}")
        root.configure(bg="white")

        logo_img = tk.PhotoImage(file="logo.png").subsample(1)
        create_logo(root, width, height, logo_img)

        try:
            no_internet = tk.PhotoImage(file="no_internet.png")
            no_internet_label = tk.Label(
                root, image=no_internet, borderwidth=0, highlightthickness=0
            )
            no_internet_label.place(x=(width / 2) - 150, y=(height / 2) - 160)
        except tk.TclError as e:
            print(f"Error loading image: {e}")

        message1_label = tk.Label(
            root,
            text="Your network seems to be down!",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="black",
        )
        message1_label.place(x=20, y=(height / 2) + 160)
        message1_label.update()
        message1_label.place(
            x=(width - message1_label.winfo_width()) // 2, y=(height / 2) + 160
        )

        message2_label = tk.Label(
            root,
            text="Please check your internet connection.",
            font=("Arial", 12),
            bg="white",
            fg="black",
        )
        message2_label.place(x=20, y=(height / 2) + 185)
        message2_label.update()
        message2_label.place(
            x=(width - message2_label.winfo_width()) // 2, y=(height / 2) + 185
        )

        exit_button(root, width, height)

        root.mainloop()


try:
    cred = credentials.Certificate(
        os.path.join(os.path.dirname(__file__), "credentials.json")
    )
    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": "https://exam-scheduler-2-default-rtdb.asia-southeast1.firebasedatabase.app"
        },
    )
except Exception as e:
    internet_connection()


def exit_button(root, width, height):
    """
     Create and place an exit button. This button is used to exit the program when the user presses the exit button
     
     @param root - The Tkinter root window that will be destroyed
     @param width - The width of the button in pixels. This is a bit different from the screen width
     @param height - The height of the button in pixels. This is a
    """
    exit_button = tk.Button(
        root,
        text="EXIT",
        height=1,
        bg="red",
        fg="white",
        font=("Sitka Text Semibold", 15, "bold"),
        command=root.destroy,
    )
    exit_button.place(x=20, y=height - 65, width=130)


def create_logo(root, width, height, logo_img):
    """
     Create and return a Tkinter widget that will be used to display the exam scheduler logo
     
     @param root - The tkinter widget to which the widget will be added
     @param width - The width of the widget in pixels ( including border )
     @param height - The height of the widget in pixels ( including border )
     @param logo_img - The path to the image to be
    """
    logo_label = tk.Label(root, image=logo_img, bd=0)
    logo_label.pack(side="left", anchor="nw", padx=10, pady=10)
    text_label = tk.Label(
        root,
        text="EXAM SCHEDULER",
        bg="white",
        fg="black",
        width=35,
        height=1,
        font=("Sitka Text Semibold", 18, "bold"),
    )
    text_label.pack(pady=30, anchor="n")
    line_canvas = tk.Canvas(
        root, height=1, width=width, bg="black", highlightthickness=0
    )
    line_canvas.create_line(0, 0, width, 0, fill="black")
    line_canvas.place(x=0, y=120 - 20)


def textbox(root, message, x, y, width):
    """
     Display a text box. This is a wrapper around insert_text_with_typing_animation that allows you to insert text at the bottom of the screen without typing the text.
     
     @param root - The Tk widget to display the text in.
     @param message - The text to display. Must be a string.
     @param x - The x position of the text. Must be a number between 0 and 2 ** 30.
     @param y - The y position of the text. Must be a number between 0 and 2 ** 30.
     @param width - The width of the text in pixels. Must be a number between 0 and 2
    """
    output_box = tk.Text(
        root,
        height=1,
        bg="#f0f4f9",
        fg="black",
        font=("Cascadia Code", 12),
        wrap="word",
        state="disabled",
    )
    output_box.place(x=x, y=y, width=width)
    output_box.config(state=tk.NORMAL)
    output_box.delete("1.0", tk.END)
    insert_text_with_typing_animation(output_box, message)
    output_box.config(state=tk.DISABLED)


def insert_text_with_typing_animation(text_widget, text):
    """
     Insert text into a Tkinter widget with typing animation. This is useful for debugging the text being inserted in an interactive terminal.
     
     @param text_widget - The widget to insert into. It must be a Text widget.
     @param text - The text to insert into the widget. It must be a list of characters
    """
    text_widget.configure(state="normal")
    # Insert and update the text widget
    for char in text:
        text_widget.insert(tk.END, char)
        text_widget.see(tk.END)
        text_widget.update()
        time.sleep(0.02)
    text_widget.configure(state="disabled")


def create_back_button(root, command, x, y, back_button_image):
    """
     Creates and places a back button. This is used to show the button that is clicked when the user presses the back button
     
     @param root - The Tk widget to be used as the parent
     @param command - The command that was pressed
     @param x - The x position of the button in the screen
     @param y - The y position of the button in the screen
     @param back_button_image - The image to be used for the
    """
    style = ttk.Style()
    style.configure(
        "RoundedW.TButton", borderwidth=0, relief="flat", background="white"
    )
    back_button = ttk.Button(
        root, image=back_button_image, style="RoundedW.TButton", command=command
    )
    back_button.place(x=x, y=y)


def is_dark_color(color):
    """
     Checks if a color is dark. This is based on luminance and a threshold of 128
     
     @param color - The color to check.
     
     @return True if the color is dark False otherwise. Note that dark colors are defined as black
    """
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    luminance_threshold = 128
    return luminance < luminance_threshold


def pick_color():
    """
     Pick a color and color to use for an image. This is a helper function to make it easier to use in tests.
     
     
     @return tuple of color and foreground color ( hex string )
    """
    color = "#{:02x}{:02x}{:02x}".format(
        random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    )
    fg = "white" if is_dark_color(color) else "black"
    return color, fg


department_names = []
try:
    root_ref = db.reference("/")
    departments_ref = root_ref.child("departments")
    data = departments_ref.get()
    # Add all department names to the list of departments_ref
    if data:
        # Add the names of all department names to the list of department names.
        for department in departments_ref.get():
            department_names.append(department)

except Exception as e:
    internet = False
    internet_connection()
    print("Error reading data from Firebase:", e)

# ============================================================================================
# ============================================================================================


def one():
    """
     Create a Tk window that shows an exam scheduler. The image is centered on the top left
    """
    root = tk.Tk()
    root.overrideredirect(True)
    width = 550
    height = 450
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg="white")

    logo = Image.open("logo_1.png")
    logo_small = logo.resize((int(logo.width / 3), int(logo.height / 3)))
    logo_tk = ImageTk.PhotoImage(logo_small)
    label = tk.Label(root, image=logo_tk, bd=0)
    label.pack(pady=(screen_height / 3) - logo.height + 15)

    text_label = tk.Label(
        root,
        text="EXAM SCHEDULER",
        bg="white",
        fg="black",
        width=35,
        height=1,
        font=("Sitka Text Semibold", 18, "bold"),
    )
    text_label.place(x=9, y=height - 75)

    hello_label = tk.Label(
        root,
        text="THAPAR INSTITUTE OF ENGINEERING AND TECHNOLOGY",
        bg="white",
        fg="red",
        width=46,
        height=1,
        font=("Sitka Text Semibold", 12, "bold"),
    )
    hello_label.place(x=40, y=height - 40)

    def animate():
        """
         Resize the logo to 20px in each direction and display the result in the
        """
        width, height = logo_small.size
        target_width, target_height = logo.size
        step_width = (target_width - width) / 20
        step_height = (target_height - height) / 20
        # resize the logo and resize the logo
        for i in range(1, 21):
            new_width = int(width + i * step_width)
            new_height = int(height + i * step_height)
            new_logo = logo.resize((new_width, new_height))
            new_logo_tk = ImageTk.PhotoImage(new_logo)
            label.configure(image=new_logo_tk)
            root.update()
            root.after(100)

    animate()
    root.destroy()
    login()

    root.mainloop()


# ============================================================================================
# ============================================================================================


def two():
    """
     This is the function that creates the buttons and calls the functions to do the task.
    """
    def create_button(text, bg_color, command, y_position):
        """
         Creates a button to be used in the dialog. It is placed at the top of the screen
         
         @param text - text to be displayed in the button
         @param bg_color - color of the button in the form #RRGGBB
         @param command - command that will be executed when the button is clicked
         @param y_position - y position of the button in the
        """
        button = tk.Button(
            root,
            text=text,
            width=28,
            height=1,
            fg="black",
            bg=bg_color,
            font=("Sitka Text Semibold", 18, "bold"),
            command=command,
        )
        button.place(x=112 - 75, y=y_position - 20)

    root = tk.Tk()
    root.title("Exam Scheduler")
    root.overrideredirect(True)
    root_ref = db.reference("/dates")
    date_data = root_ref.get()
    # Create the date data button.
    if date_data is not None:
        width = 500
        height = 630
        create_button(
            "EDIT DATES", "#f2aea5", lambda: root.destroy() or dates(True), 430
        )
    else:
        width = 500
        height = 550
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = int((screen_width / 2) - (width / 2)), int(
        (screen_height / 2) - (height / 2)
    )
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg="white")

    logo_img = tk.PhotoImage(file="logo.png").subsample(1)
    create_logo(root, width, height, logo_img)
    exit_button(root, width, height)

    create_button("SCHEDULE EXAMS", "#9ab7de", lambda: root.destroy() or sche1(), 175)
    create_button(
        "MANAGE COURSES", "#f2aea5", lambda: root.destroy() or department(), 260
    )
    create_button("MANAGE SEATS", "#9ab7de", lambda: root.destroy() or seats(), 345)

    root.mainloop()


# ============================================================================================
# ============================================================================================


def sche1():
    """
     Sche1 is the top - level function that creates the Exam Scheduler
    """
    def create_button(
        text,
        bg_color,
        fg_color,
        font_size,
        command,
        x_position,
        y_position,
        width,
        height,
    ):
        button = tk.Button(
            root,
            text=text,
            fg=fg_color,
            bg=bg_color,
            font=("Sitka Text Semibold", font_size, "bold"),
            command=command,
        )
        button.place(x=x_position, y=y_position, width=width, height=height)

    def create_image_button(image_file, command, x_position, y_position, width, height):
        """
         Create a button to use an image. This is a convenience function for creating a Tk. Button with an image and a command
         
         @param image_file - Path to the image file
         @param command - Command to use for the button. Can be one of the following : tray_click
         @param x_position - X position in pixels of the button '
         @param y_position
         @param width
         @param height
        """
        img = tk.PhotoImage(file=image_file)
        button = ttk.Button(root, image=img, command=command)
        button.image = img
        button.place(x=x_position, y=y_position, width=width, height=height)

    root = tk.Tk()
    root.title("Exam Scheduler")
    root.overrideredirect(True)
    width, height = 500, 450
    x, y = int((root.winfo_screenwidth() / 2) - (width / 2)), int(
        (root.winfo_screenheight() / 2) - (height / 2)
    )
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg="white")

    def show_text(message):
        """
         Display a text box. This is a convenience function to make it easier to use it in a program's main loop
         
         @param message - The message to display
        """
        textbox(root, message, 37, height - 110, 426)

    logo_img = tk.PhotoImage(file="logo.png").subsample(1)
    create_logo(root, width, height, logo_img)

    exit_button(root, width, height)

    create_image_button(
        "select_venues.png", lambda: root.destroy() or sche2(), 37, 175, 130, 50
    )

    create_image_button("days.png", lambda: None, 377, 175, 86, 25)

    days = tk.Entry(root, bg="blue", fg="white", font=("Times New Roman", 12))
    days.insert(0, "10")
    days.place(x=453 - 75, y=195 - 20 + 30, width=84, height=18)

    odd_sem_image = tk.PhotoImage(file="oddsem.png")
    even_sem_image = tk.PhotoImage(file="even_sem.png")
    odd_sem_var, even_sem_var = tk.BooleanVar(value=False), tk.BooleanVar(value=False)

    style = ttk.Style()
    style.configure("Rounded.TButton", borderwidth=0, relief="flat")
    style.configure(
        "RoundedW.TButton", borderwidth=0, relief="flat", background="white"
    )
    style.configure("Selected.TButton", background="green")

    def sem():
        """
         This function creates the semesters.
        """
        def odd_sem():
            """
             Switch to odd semester mode and vice versa.
            """
            odd_sem_var.set(True)
            even_sem_var.set(False)
            update_buttons()

        def even_sem():
            """
             Switch even semester to odd semester. This is called by the user.
            """
            odd_sem_var.set(False)
            even_sem_var.set(True)
            update_buttons()

        def update_buttons():
            """
             Update buttons based on state of checkboxes. This is called after the user selects a button
            """
            odd_style = "Selected.TButton" if odd_sem_var.get() else "Rounded.TButton"
            even_style = "Selected.TButton" if even_sem_var.get() else "Rounded.TButton"

            odd_sem.config(style=odd_style)
            even_sem.config(style=even_style)

        odd_sem = ttk.Button(root, image=odd_sem_image, command=odd_sem)
        odd_sem.place(x=252 - 75, y=195 - 20, width=90, height=50)

        even_sem = ttk.Button(root, image=even_sem_image, command=even_sem)
        even_sem.place(x=252 - 75 + 100, y=195 - 20, width=90, height=50)

        update_buttons()

    sem()

    try:
        root_ref = db.reference("/selected_venues/capacity")
        data = root_ref.get()
        capacity = int(data)
    except:
        show_text("Choose venue.")

    def schedule_exam():
        """
         Schedule exam. This function is called when user enters schedule section in order to schedule exam
        """
        try:
            day = int(days.get())

        except:
            show_text("Enter days.")

        # Show the semester ODD EVEN.
        if (odd_sem_var.get()) or (even_sem_var.get()):
            root.destroy()
            schedule(odd_sem_var.get(), even_sem_var.get(), day, capacity)
        else:
            show_text("Choose semester ODD/EVEN.")

    create_button(
        "SCHEDULE EXAMS", "#f2aea5", "black", 18, schedule_exam, 112 - 75, 250, 426, 60
    )

    back_button_image = tk.PhotoImage(file="back.png")
    create_back_button(root, lambda: root.destroy() or two(), 7, 110, back_button_image)

    root.mainloop()


# ============================================================================================
# ============================================================================================

capacity = 0


def sche2():
    root = tk.Tk()
    root.title("Selects Seats")
    root.overrideredirect(True)
    width = 770
    height = 660
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg="white")

    logo_img = tk.PhotoImage(file="logo.png")
    logo_img = logo_img.subsample(1)
    create_logo(root, width, height, logo_img)
    exit_button(root, width, height)

    lbl = tk.Label(
        root,
        text="SELECT VENUES:",
        width=21,
        anchor="w",
        height=1,
        fg="black",
        bg="white",
        font=("Sitka Text Semibold", 15, "bold"),
    )
    lbl.place(x=125 - 75, y=130 - 20)

    scroll_height_mapping = {570: 140, 700: 270, 830: 400, 960: 530}
    nearest_height = min(
        scroll_height_mapping.keys(), key=lambda x: abs(x - screen_height)
    )
    table_frame = tk.Frame(root)
    scroll_height = scroll_height_mapping.get(nearest_height, 530)
    table_frame.place(x=0, y=170 - 20, width=width, height=scroll_height)

    canvas = tk.Canvas(table_frame, bd=0)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview, bd=0)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    table_frame_inside_canvas = tk.Frame(canvas, bd=0)
    canvas.create_window((0, 0), window=table_frame_inside_canvas, anchor="nw")

    ref = db.reference("/")
    data = ref.get()
    selected_venue = []
    ref = db.reference("/selected_venues")
    selected_venues_data = ref.get()

    def create_rounded_rect(text, clicked):
        """
         Creates a rectangular image with text rounded to the left and right. The text is divided into lines and each line is drawn using arial. ttf
         
         @param text - The text to draw.
         @param clicked - True if the text is clicked. False if it is not.
         
         @return An image with the text rounded to the left and
        """
        width = 120
        height = 50
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 12)
        text_color = (0, 0, 0)
        lines = text.split("\n")
        total_text_height = sum(
            font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines
        )
        vertical_gap = 5
        y = (height - total_text_height - (len(lines) - 1) * vertical_gap) // 2
        # Draw the text on the line.
        for line in lines:
            text_bbox = font.getbbox(line)
            x = (width - (text_bbox[2] - text_bbox[0])) // 2 - 10
            draw.text((x, y), line, fill=text_color, font=font)
            y += text_bbox[3] - text_bbox[1] + vertical_gap
        symbol = "+" if clicked else "x"
        plus_font = ImageFont.truetype("arial.ttf", 16)
        plus_symbol_x = width - plus_font.getbbox(symbol)[2] - 5
        plus_symbol_y = (height - total_text_height) // 2 + (
            total_text_height - plus_font.getbbox(symbol)[3]
        ) // 2
        draw.text(
            (plus_symbol_x, plus_symbol_y), symbol, fill=text_color, font=plus_font
        )
        photo_image = ImageTk.PhotoImage(image)
        return photo_image

    def extract_venue_info(data):
        """
         Extract venue information from JSON. This is a helper function to extract venue information from JSON data.
         
         @param data - The JSON data that will be used to extract information.
         
         @return A list of information about the venues in the data
        """
        venue_info = []
        # Add a venue to the venue_info. append f Venue info
        for key, value in data.get("seats", {}).items():
            venue = key
            rows = value.get("row", "N/A")
            columns = value.get("column", "N/A")
            capacity = int(rows) * int(columns)
            venue_info.append(f"Venue: {venue}\nCapacity: {capacity}")
        return venue_info

    venue_info_list = extract_venue_info(data)
    i = 0
    j = 0
    m = 0
    pos = []
    # Add a button to the table
    for item in venue_info_list:
        x = i * 140 + 20
        # Move to the right of the screen
        if x > width - 180:
            j += 1
            i = 0
        x = i * 140 + 20
        y = j * 50 + 20
        image = create_rounded_rect(item, True)
        pos.append(f"{i} {j}")
        button = ttk.Button(
            table_frame_inside_canvas, image=image, style="Rounded.TButton"
        )
        button.config(command=lambda num=m: button_callback(num, "add"))
        button.image = image
        button.grid(row=j, column=i, padx=(10, 10), pady=(10, 10))
        m += 1
        i += 1

    lbl = tk.Label(
        root,
        text=f"Capacity: {capacity}",
        anchor="center",
        fg="black",
        bg="white",
        font=("Arial", 12, "bold"),
    )
    lbl.place(x=315, y=height - 55, width=140)

    def button_callback(num, text):
        """
         Callback for adding / removing venue. It creates a frame and adds / removes a button to the table
         
         @param num - The number of the venue
         @param text - The text that should be displayed in the button
        """
        global capacity
        frame = tk.Frame(root, bg="white", borderwidth=0)
        frame.place(x=184, y=height - 31, width=402, height=30)
        global capacity
        input_string = venue_info_list[num]
        ven, cap = input_string.split("\n")
        venue = ven.split("Venue: ")[1]
        room_capacity = cap.split("Capacity: ")[1]
        i, j = pos[num].split(" ")
        frame = tk.Frame(table_frame_inside_canvas, borderwidth=0)
        frame.place(x=11 + (150 * int(i)), y=(11 + (80) * int(j)), width=128, height=58)
        # Add or remove a Venue to the table
        if text == "add":
            image = create_rounded_rect(input_string, False)
            button = ttk.Button(
                table_frame_inside_canvas, image=image, style="Selected.TButton"
            )
            button.config(command=lambda num=num: button_callback(num, "remove"))
            button.image = image
            button.grid(row=j, column=i, padx=(10, 10), pady=(10, 10))
            capacity += int(room_capacity)
            selected_venue.append(venue)
        # Remove the venue from the selected venue list
        if text == "remove":
            image = create_rounded_rect(input_string, True)
            button = ttk.Button(
                table_frame_inside_canvas, image=image, style="Rounded.TButton"
            )
            button.config(command=lambda num=num: button_callback(num, "add"))
            button.image = image
            button.grid(row=j, column=i, padx=(10, 10), pady=(10, 10))
            capacity -= int(room_capacity)
            selected_venue.remove(venue)
        lbl = tk.Label(
            root,
            text=f"Capacity: {capacity}",
            anchor="center",
            fg="black",
            bg="white",
            font=("Arial", 12, "bold"),
        )
        lbl.place(x=315, y=height - 55, width=140)

    style = ttk.Style()
    style.configure("Rounded.TButton", borderwidth=0, relief="flat")
    style.configure(
        "RoundedW.TButton", borderwidth=0, relief="flat", background="white"
    )
    style.configure("Selected.TButton", background="green")

    # Move to the left of the screen
    if x > width - 240:
        i = 0
        j += 1

    def show_text(message):
        """
         Display a text box on the screen. This is a convenience function to make it easier to use in conjunction with : func : ` show_button `.
         
         @param message - The message to display on the screen. Must be a string
        """
        textbox(root, message, 45, height - 100, width - 90)

    def on_canvas_configure(event):
        """
         Called when the canvas is configured. This is a callback function and should be used to reconfigure the canvas to fit the table_frame_inside_canvas
         
         @param event - The event that triggered this
        """
        canvas.configure(scrollregion=canvas.bbox("all"))
        table_frame_inside_canvas.config(width=canvas.winfo_width())

    canvas.bind("<Configure>", on_canvas_configure)

    def handle_scroll(event):
        """
         Scroll the canvas vertically. This is called when the user scrolls a view.
         
         @param event - The event that triggered this function call. It's passed to the event handler
        """
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    canvas.bind_all("<MouseWheel>", handle_scroll)

    def handle_back():
        """
         Called when back button is pressed. Destroys the window and starts the Sche1
        """
        root.destroy()
        sche1()

    back_button_image = tk.PhotoImage(file="back.png")
    create_back_button(root, handle_back, 7, 110, back_button_image)

    def handle_selected():
        """
         Handle selected venue and update database if there is one. Otherwise show message
        """
        # Show the number of venue s and previous data from the database selected.
        if len(selected_venue) != 0:
            show_text(f"{len(selected_venue)} venue(s) selected.")
            ref = db.reference("selected_venues")
            ref.set(selected_venue)
            ref.update({"capacity": f"{capacity}"})
            root.destroy()
            sche1()
        else:
            show_text("Previous data from database selected.")
            root.destroy()
            sche1()

    # Create a tk. Label for the venues selected in Database. Select new to replace it.
    if len(selected_venues_data) - 1 > 0:
        lbl1 = tk.Label(
            root,
            text=f"{len(selected_venues_data)-1} venues selected in Database. Select new to replace it.",
            anchor="center",
            fg="black",
            bg="white",
            font=("Arial", 11),
        )
        lbl1.place(x=185, y=height - 30, width=400)
        lbl = tk.Label(
            root,
            text=f"Capacity: {selected_venues_data['capacity']}",
            anchor="center",
            fg="black",
            bg="white",
            font=("Arial", 12, "bold"),
        )
        lbl.place(x=315, y=height - 55, width=140)

    done_button = tk.Button(
        root,
        text="DONE",
        height=1,
        bg="darkgreen",
        fg="white",
        font=("Sitka Text Semibold", 15, "bold"),
        command=handle_selected,
    )
    done_button.place(x=width - 150, y=height - 65, width=130)

    root.mainloop()


# ============================================================================================
# ============================================================================================

days_names = []
subject_list = []


def schedule(odd_sem, even_sem, days_allocated, capacity):
    """
     Schedule exam using Tkinter. This is a function that returns a tuple of two Tkinter objects.
     
     @param odd_sem - Semi - monotonically increasing number of exposures to schedule.
     @param even_sem - Semi - monotonically increasing number of exposures to schedule.
     @param days_allocated - Number of days allocated to the exam.
     @param capacity - Capacity of the exam. If 0 exam is scheduled without capacity
    """
    root = tk.Tk()
    root.title("Scheduling Exam")
    root.overrideredirect(True)
    width = 600
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg="white")

    logo_img = tk.PhotoImage(file="logo.png")
    logo_img = logo_img.subsample(1)
    create_logo(root, width, height, logo_img)

    def show_text1(message):
        """
         Display a text box. This is a convenience function to make it easier to use it in a program that takes a message and displays it on the screen.
         
         @param message - The message to display on the screen in bold
        """
        textbox(root, message, 40, height - 100, 520)

    def show_text(message):
        """
         Display a text box. This is a convenience function to make it easier to use it in a program's main loop
         
         @param message - The message to display
        """
        textbox(root, message, 40, height - 150, 520)

    show_text1("")
    lbl1 = tk.Label(
        root,
        text=f"Don't close this window.",
        anchor="center",
        fg="black",
        bg="white",
        font=("Arial", 12),
    )
    lbl1.place(x=185, y=height - 30)
    lbl1.update()
    lbl1.place(x=(width - lbl1.winfo_width()) // 2, y=height - 25)
    show_text1("This process can takes minutes. Thanks for patience.")

    def get_subjects_and_students(department, branch, semester):
        """
         Fetches data from the subjects and students tables. This is used to generate an API response to the API request that would be sent to the client.
         
         @param department - The name of the department. E. g.
         @param branch - The name of the branch. E. g.
         @param semester - The name of the semester. E
        """
        ref = db.reference(
            f"/departments/{department}/branches/{branch}/semesters/{semester}"
        )
        try:
            subjects = ref.child("subjects").get()
            return subjects
        except Exception as e:
            print(f"Error fetching data for {department},{branch},{semester}:{e}")
            return {}, {}

    semester1_data = {}
    semester2_data = {}
    semester3_data = {}
    semester4_data = {}
    semester5_data = {}
    semester6_data = {}
    semester7_data = {}
    semester8_data = {}
    semester9_data = {}
    semester10_data = {}
    semester11_data = {}
    semester12_data = {}
    semester13_data = {}
    semester14_data = {}
    semester15_data = {}
    semester16_data = {}

    Semester1 = []
    Semester2 = []
    Semester3 = []
    Semester4 = []
    Semester5 = []
    Semester6 = []
    Semester7 = []
    Semester8 = []
    Semester9 = []
    Semester10 = []
    Semester11 = []
    Semester12 = []
    Semester13 = []
    Semester14 = []
    Semester15 = []
    Semester16 = []
    sem = []

    departments = []
    root_ref = db.reference("/")
    departments_ref = root_ref.child("departments")
    data = departments_ref.get()
    show_text("Fetching Departments/Branches.")
    # Add all the departments to the list of departments
    if data:
        # Add all the departments to the list of departments
        for department1 in departments_ref.get():
            departments.append(department1)
    show_text("Fetching subject and student details.")
    # This function returns a list of all the students in the departments.
    for department in departments:
        branches = []

        branch_ref = root_ref.child(f"departments/{department}/branches")

        # Add branch to branch_ref list of branches
        for branch1 in branch_ref.get():
            branches.append(branch1)
        # Returns a list of all the semesters in the given branch.
        for branch in branches:
            try:
                semesters = []
                semester_ref = root_ref.child(
                    f"departments/{department}/branches/{branch}/semesters"
                )
                # Add semester to the list of semesters
                for semester1 in semester_ref.get():
                    semesters.append(semester1)
            except:
                pass

            # This function will return a list of all the semesters in the semesters.
            for semester in semesters:
                subjects = get_subjects_and_students(department, branch, semester)
                try:
                    # This function is used to generate a list of subjects.
                    if subjects is not None:
                        # This function is used to generate a list of subjects for a given student count.
                        for subject, student_count in subjects.items():
                            # Add subject to subject list
                            if subject not in subject_list:
                                subject_list.append(subject)
                            subject = subject.split(" - ", 1)[0]
                            # This function is used to generate the count of semesters
                            if semester == "Semester 1":
                                # Add a subject to semester1_data.
                                if subject not in semester1_data:
                                    semester1_data[subject] = {}
                                semester1_data[subject][branch] = student_count
                            elif semester == "Semester 2":
                                # Add a subject to semester2_data.
                                if subject not in semester2_data:
                                    semester2_data[subject] = {}
                                semester2_data[subject][branch] = student_count
                            elif semester == "Semester 3":
                                # Add subject to semester3 data.
                                if subject not in semester3_data:
                                    semester3_data[subject] = {}
                                semester3_data[subject][branch] = student_count
                            elif semester == "Semester 4":
                                # Add a subject to semester4 data
                                if subject not in semester4_data:
                                    semester4_data[subject] = {}
                                semester4_data[subject][branch] = student_count
                            elif semester == "Semester 5":
                                # Add a subject to semester5_data.
                                if subject not in semester5_data:
                                    semester5_data[subject] = {}
                                semester5_data[subject][branch] = student_count
                            elif semester == "Semester 6":
                                # Add a subject to semester6_data.
                                if subject not in semester6_data:
                                    semester6_data[subject] = {}
                                semester6_data[subject][branch] = student_count
                            elif semester == "Semester 7":
                                # Add subject to semester7 data.
                                if subject not in semester7_data:
                                    semester7_data[subject] = {}
                                semester7_data[subject][branch] = student_count
                            elif semester == "Semester 8":
                                # Add a subject to semester8 data
                                if subject not in semester8_data:
                                    semester8_data[subject] = {}
                                semester8_data[subject][branch] = student_count
                            elif semester == "Semester 9":
                                # Add subject to semester9_data if subject is not in semester9_data
                                if subject not in semester9_data:
                                    semester9_data[subject] = {}
                                semester9_data[subject][branch] = student_count
                            elif semester == "Semester 10":
                                # Add a subject to semester10_data.
                                if subject not in semester10_data:
                                    semester10_data[subject] = {}
                                semester10_data[subject][branch] = student_count
                            elif semester == "Semester 11":
                                # Add a subject to semester11_data.
                                if subject not in semester11_data:
                                    semester11_data[subject] = {}
                                semester11_data[subject][branch] = student_count
                            elif semester == "Semester 12":
                                # Add a subject to semester12 data
                                if subject not in semester12_data:
                                    semester12_data[subject] = {}
                                semester12_data[subject][branch] = student_count
                            elif semester == "Semester 13":
                                # Add a subject to semester13_data.
                                if subject not in semester13_data:
                                    semester13_data[subject] = {}
                                semester13_data[subject][branch] = student_count
                            elif semester == "Semester 14":
                                # Add a subject to semester14_data.
                                if subject not in semester14_data:
                                    semester14_data[subject] = {}
                                semester14_data[subject][branch] = student_count
                            elif semester == "Semester 15":
                                # Add a subject to semester15_data.
                                if subject not in semester15_data:
                                    semester15_data[subject] = {}
                                semester15_data[subject][branch] = student_count
                            elif semester == "Semester 16":
                                # Add a subject to semester16_data.
                                if subject not in semester16_data:
                                    semester16_data[subject] = {}
                                semester16_data[subject][branch] = student_count
                            else:
                                print("Invalid semester")
                except:
                    pass
    show_text("Choosing subjects.")

    def choose_subjects(semester_data, capacity):
        """
         Given semester data and an initial capacity choose subjects to make a balance.
         
         @param semester_data - Dict of subjects keyed by subject
         @param capacity - Capacity of subjects to choose
         
         @return Set of subjects that are in the balance with at least
        """
        selected_subjects = set()
        # Find the subject of the subject that is in semester_data.
        while semester_data:
            max_students = 0
            chosen_subject = None
            chosen_branches = set()
            # Find the subject and branch data for the subject and the branch data.
            for subject, branch_data in semester_data.items():
                branch_students = sum(branch_data.values())
                # Find the subject and branches that are chosen by the subject and the capacity of the subject.
                if (branch_students > max_students) and (branch_students <= capacity):
                    max_students = branch_students
                    chosen_subject = subject
                    chosen_branches = set(branch_data.keys())
                    # If capacity is branch_students then we can t find the first students in the branch_students list.
                    if capacity == branch_students:
                        break
            # Returns a list of subjects that are not chosen by the user.
            if chosen_subject:
                selected_subjects.add(chosen_subject)
                capacity -= max_students
                semester_data = {
                    subject: data
                    for subject, data in semester_data.items()
                    if not set(data.keys()).intersection(chosen_branches)
                }
                # Returns the selected subjects.
                if capacity == 0:
                    return selected_subjects
            else:
                break
        return selected_subjects

    def group_subjects(subjects_to_group, semester_data):
        """
         Group subjects_to_group and return semester_data with subjects grouped
         
         @param subjects_to_group - list of subjects to group
         @param semester_data - dictionary of semester data keyed by subjects
         
         @return seperator_data with subjects grouped by branch
        """
        # Returns semester data if subjects_to_group is not set.
        if not subjects_to_group:
            return semester_data
        total_students = 0
        # sum of students in the semester data
        for subject in subjects_to_group:
            total_students += sum(semester_data[subject].values())
        grouped_subject = "Grouped Subjects"
        semester_data[grouped_subject] = {}
        # This function is used to calculate the total students of all subjects in semester_data grouped_subjects_to_group 0.
        for branch in semester_data[subjects_to_group[0]]:
            semester_data[grouped_subject][branch] = total_students
        # Removes all semester data for all subjects to group
        for subject in subjects_to_group:
            del semester_data[subject]
        return semester_data

    def calculate_max_capacity(data):
        """
         Calculates the maximum capacity of a course. This is a helper function for get_capacity_from_course.
         
         @param data - Course data to calculate the maximum capacity for.
         
         @return Tuple of the maximum subject and its capacity in the course
        """
        subject_capacity = {}
        # Add capacity to each subject in the course
        for course in data.values():
            # Add capacity to subject_capacity for each subject
            for subject, capacity in course.items():
                # Add capacity to the subject capacity.
                if subject in subject_capacity:
                    subject_capacity[subject] += capacity
                else:
                    subject_capacity[subject] = capacity
        max_subject = max(subject_capacity, key=subject_capacity.get)
        return max_subject, subject_capacity[max_subject]

    def select_semester_subjects(semester_data, semester_name, capacity):
        """
         Select subjects from semester data and store them in lists. This is a loop to be used in order to select subjects from a list
         
         @param semester_data - list of data from the data file that is to be analysed. Each element is a list of subjects that are in the form of a list of integers where each integer is
         @param semester_name - string name of the semester
         @param capacity - number of subjects to be selected in the data
        """
        # This function will loop over all semester data.
        while semester_data:
            selected_subjects = choose_subjects(semester_data, capacity)
            # This function is used to add the subject names to the semester.
            if selected_subjects != set():
                sem.append(selected_subjects)
                # This function is used to create the subject names
                if semester_name == "Semester 1":
                    Semester1.append(selected_subjects)
                elif semester_name == "Semester 2":
                    Semester2.append(selected_subjects)
                elif semester_name == "Semester 3":
                    Semester3.append(selected_subjects)
                elif semester_name == "Semester 4":
                    Semester4.append(selected_subjects)
                elif semester_name == "Semester 5":
                    Semester5.append(selected_subjects)
                elif semester_name == "Semester 6":
                    Semester6.append(selected_subjects)
                elif semester_name == "Semester 7":
                    Semester7.append(selected_subjects)
                elif semester_name == "Semester 8":
                    Semester8.append(selected_subjects)
                elif semester_name == "Semester 9":
                    Semester9.append(selected_subjects)
                elif semester_name == "Semester 10":
                    Semester10.append(selected_subjects)
                elif semester_name == "Semester 11":
                    Semester11.append(selected_subjects)
                elif semester_name == "Semester 12":
                    Semester12.append(selected_subjects)
                elif semester_name == "Semester 13":
                    Semester13.append(selected_subjects)
                elif semester_name == "Semester 14":
                    Semester14.append(selected_subjects)
                elif semester_name == "Semester 15":
                    Semester15.append(selected_subjects)
                elif semester_name == "Semester 16":
                    Semester16.append(selected_subjects)
            else:
                break
            semester_data = {
                subject: data
                for subject, data in semester_data.items()
                if subject not in selected_subjects
            }

    # Show the capacity of semester.
    if odd_sem:
        # Calculate the max capacity of semester1 data
        if not semester1_data:
            max_capacity_1 = 0
        else:
            max_capacity_1 = calculate_max_capacity(semester1_data)[1]

        # Calculate the maximum capacity of the semester3 data.
        if not semester3_data:
            max_capacity_3 = 0
        else:
            max_capacity_3 = calculate_max_capacity(semester3_data)[1]

        # Calculate the maximum capacity of the semester5 data.
        if not semester5_data:
            max_capacity_5 = 0
        else:
            max_capacity_5 = calculate_max_capacity(semester5_data)[1]

        # Calculate the max capacity of semester7 data
        if not semester9_data:
            max_capacity_7 = 0
        else:
            max_capacity_7 = calculate_max_capacity(semester7_data)[1]

        # Calculate the maximum capacity of semester9 data
        if not semester9_data:
            max_capacity_9 = 0
        else:
            max_capacity_9 = calculate_max_capacity(semester9_data)[1]

        # Calculate the maximum capacity of the semester11 data.
        if not semester11_data:
            max_capacity_11 = 0
        else:
            max_capacity_11 = calculate_max_capacity(semester11_data)[1]

        # Calculate the maximum capacity of the semester13 data.
        if not semester13_data:
            max_capacity_13 = 0
        else:
            max_capacity_13 = calculate_max_capacity(semester13_data)[1]

        # Calculate the max capacity of semester15 data.
        if not semester15_data:
            max_capacity_15 = 0
        else:
            max_capacity_15 = calculate_max_capacity(semester15_data)[1]
        show_text("Calculating capacity.")
        max_capacity = max(
            max_capacity_1,
            max_capacity_3,
            max_capacity_5,
            max_capacity_7,
            max_capacity_9,
            max_capacity_11,
            max_capacity_13,
            max_capacity_15,
        )

        # Show the subjects for the current capacity.
        if (capacity / 2) < max_capacity:
            show_text(f"Sorry, Capacity should be at least {max_capacity*2}.")
            time.sleep(2)
            root.destroy()
        else:
            show_text("Selecting subjects.")
            select_semester_subjects(semester1_data, "Semester 1", capacity / 2)
            select_semester_subjects(semester3_data, "Semester 3", capacity / 2)
            select_semester_subjects(semester5_data, "Semester 5", capacity / 2)
            select_semester_subjects(semester7_data, "Semester 7", capacity / 2)
            select_semester_subjects(semester9_data, "Semester 9", capacity / 2)
            select_semester_subjects(semester11_data, "Semester 11", capacity / 2)
            select_semester_subjects(semester13_data, "Semester 13", capacity / 2)
            select_semester_subjects(semester15_data, "Semester 15", capacity / 2)

    # Show the max capacity of semester.
    if even_sem:
        # Calculate the maximum capacity of semester2 data
        if not semester2_data:
            max_capacity_2 = 0
        else:
            max_capacity_2 = calculate_max_capacity(semester2_data)[1]

        # Calculate the max capacity of the semester4 data
        if not semester4_data:
            max_capacity_4 = 0
        else:
            max_capacity_4 = calculate_max_capacity(semester4_data)[1]

        # Calculate the maximum capacity of the semester6 data.
        if not semester6_data:
            max_capacity_6 = 0
        else:
            max_capacity_6 = calculate_max_capacity(semester6_data)[1]

        # Calculate the maximum capacity of the semester8 data.
        if not semester8_data:
            max_capacity_8 = 0
        else:
            max_capacity_8 = calculate_max_capacity(semester8_data)[1]

        # Calculate the maximum capacity of the semester10 data.
        if not semester10_data:
            max_capacity_10 = 0
        else:
            max_capacity_10 = calculate_max_capacity(semester10_data)[1]

        # Calculate the maximum capacity of the semester12 data.
        if not semester12_data:
            max_capacity_12 = 0
        else:
            max_capacity_12 = calculate_max_capacity(semester12_data)[1]

        # Calculate the maximum capacity of the semester14 data.
        if not semester14_data:
            max_capacity_14 = 0
        else:
            max_capacity_14 = calculate_max_capacity(semester14_data)[1]

        # Calculate the max capacity of semester16 data.
        if not semester16_data:
            max_capacity_16 = 0
        else:
            max_capacity_16 = calculate_max_capacity(semester16_data)[1]

        max_capacity = max(
            max_capacity_2,
            max_capacity_4,
            max_capacity_6,
            max_capacity_8,
            max_capacity_10,
            max_capacity_12,
            max_capacity_14,
            max_capacity_16,
        )

        # Show the subjects for the current capacity.
        if (capacity / 2) < max_capacity:
            show_text(f"Sorry, Capacity should be at least {max_capacity*2}.")
            time.sleep(2)
            root.destroy()

        else:
            show_text("Selecting subjects.")
            select_semester_subjects(semester2_data, "Semester 2", capacity / 2)
            select_semester_subjects(semester4_data, "Semester 4", capacity / 2)
            select_semester_subjects(semester6_data, "Semester 6", capacity / 2)
            select_semester_subjects(semester8_data, "Semester 8", capacity / 2)
            select_semester_subjects(semester10_data, "Semester 10", capacity / 2)
            select_semester_subjects(semester12_data, "Semester 12", capacity / 2)
            select_semester_subjects(semester14_data, "Semester 14", capacity / 2)
            select_semester_subjects(semester16_data, "Semester 16", capacity / 2)

    semesters = [
        Semester1,
        Semester2,
        Semester3,
        Semester4,
        Semester5,
        Semester6,
        Semester7,
        Semester8,
        Semester9,
        Semester10,
        Semester11,
        Semester12,
        Semester13,
        Semester14,
        Semester15,
        Semester16,
    ]
    sem = [i for sublist in semesters for i in sublist]

    count = len(sem) // 2
    pairs = list(permutations(sem, 2))

    final = []
    # This is the heart of the program. It takes a bunch of pairs that are in semester1 semester2 semester3 semi_final and shows a message saying how to close them
    show_text("I am very close to the result.")
    while True:
        semester = sem.copy()
        semi_final = []
        random.shuffle(pairs)

        for pair in pairs:
            if (
                (pair[0] in Semester1 and pair[1] in Semester1)
                or (pair[0] in Semester2 and pair[1] in Semester2)
                or (pair[0] in Semester3 and pair[1] in Semester3)
                or (pair[0] in Semester4 and pair[1] in Semester4)
                or (pair[0] in Semester5 and pair[1] in Semester5)
                or (pair[0] in Semester6 and pair[1] in Semester6)
                or (pair[0] in Semester7 and pair[1] in Semester7)
                or (pair[0] in Semester8 and pair[1] in Semester8)
                or (pair[0] in Semester9 and pair[1] in Semester9)
                or (pair[0] in Semester10 and pair[1] in Semester10)
                or (pair[0] in Semester11 and pair[1] in Semester11)
                or (pair[0] in Semester12 and pair[1] in Semester12)
                or (pair[0] in Semester13 and pair[1] in Semester13)
                or (pair[0] in Semester14 and pair[1] in Semester14)
                or (pair[0] in Semester15 and pair[1] in Semester15)
                or (pair[0] in Semester16 and pair[1] in Semester16)
            ):
                continue
            if (pair[0] in semester) and (pair[1] in semester):
                semester.remove(pair[0])
                semester.remove(pair[1])
                semi_final.append(pair)

        if len(semi_final) > len(final):
            final = semi_final

        if len(final) == count:
            if len(semester) != 0:
                final.append(semester[0])
            break

    shift = math.ceil(len(final) / days_allocated)

    show_text(f"Minimum {shift} shift per day is needed.")

    a = []
    for day in range(1, days_allocated + 1):
        for s in range(1, shift + 1):
            a.append(f"Day {day} Shift {s}")
    show_text("Shuffling dates.")

    b = final

    random.shuffle(a)

    allocation = {}

    for i in range(len(b)):
        if i < len(a):
            allocation[a[i]] = b[i]
        else:
            break

    ref = db.reference("/dates")
    ref.delete()
    show_text("Just few seconds more.")

    for key in sorted(allocation):
        user_input = f"{key}:{allocation[key]}"
        key, value = user_input.split(":")
        value = value.replace("(", "[").replace(")", "]")
        value = eval(value)
        formatted_value = tuple([list(subset) for subset in value])
        formatted_data = {key.strip(): formatted_value}
        data = formatted_data
        ref.update(data)
    show_text("DONE")
    global days_names
    days_names = []
    try:
        root_ref = db.reference("/dates")
        data = root_ref.get()
        keys = list(data.keys())
        if data:
            for days in keys:
                days_names.append(days)
    except Exception as e:
        print("Error reading data from Firebase:", e)
    root.destroy()
    dates(False)


# ============================================================================================
# ============================================================================================

last_send_time = 0
resend_count = 0


def login():
    """
     Login to exam scheduler. This is a function that returns a Tk widget to be used as a context manager.
     
     
     @return A Tk widget to be used as a context
    """
    root = tk.Tk()
    root.title("Exam Scheduler")
    root.overrideredirect(True)

    width = 500
    height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    root.geometry(f"{width}x{height}+{x}+{y}")

    root.configure(bg="white")

    def validate_input(P):
        """
         Validates input to be used in an AIMS program. This is a helper function to make sure the user is trying to use the AIMS program as a user.
         
         @param P - A string of length 6 that is the program's input.
         
         @return True if P is a valid input False otherwise. Note that P may be empty
        """
        return P.isdigit() and len(P) <= 6

    def generate_otp():
        """
         Generate OTP for an authentication request. This is used to generate a random one time password.
         
         
         @return A randomly generated OTP string in range 100000 to 999999
        """
        return str(random.randint(100000, 999999))

    def send_otp(email, otp):
        """
         Send OTP verification email to email. This function is used to send OTP verification e - mail in Gmail
         
         @param email - Email address to send to
         @param otp - OTP to be verified.
         
         @return True if email was sent False if error. Error will be printed
        """
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "noreply.examscheduler@gmail.com"
        sender_password = "gvim cads mfrx svpq"
        message = f"Subject: OTP Verification\n\nYour OTP is: {otp}"

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message)
            server.quit()
            return True
        except Exception as e:
            print("Error sending email:", str(e))
            return False

    def send_otp_button():
        """
         Send OTP to user. This is called when user clicks send otp button.
         
         
         @return True if send otp was successful False otherwise. The function returns True if send otp was successful
        """
        root_ref = db.reference("/")
        permissible_accounts_ref = root_ref.child("permissible_accounts")
        permissible_accounts = permissible_accounts_ref.get()
        p_accounts = []
        # Add an email to the permissible_accounts list
        for key, email in permissible_accounts.items():
            p_accounts.append(email)

        global otp
        global last_send_time
        global resend_count

        current_time = time.time()
        email = username_entry.get()

        # If the user is not authorized
        if email not in p_accounts:
            show_text("Not authorized user.", "f")
            time.sleep(0.2)
            refresh()
            return
        show_text("Sending OTP...", "y")
        # Send OTPs to the server.
        if resend_count > 5:
            # Send OTP to the user.
            if current_time - last_send_time < 3600:
                wait_time = 3600 - int(current_time - last_send_time)
                show_text(f"Please wait for {wait_time//60} minutes.", "f")
                time.sleep(0.2)
                refresh()
            else:
                resend_count = 1
                otp = generate_otp()

                # Send OTP to the user.
                if not email:
                    show_text("Please enter an email address.", "f")
                    time.sleep(0.2)
                    refresh()
                else:
                    # Send OTP to the email.
                    if send_otp(email, otp):
                        last_send_time = current_time
                        show_text("Success! OTP sent to your email.", "s")
                        time.sleep(0.2)
                        refresh()
        else:
            # Send OTP to the email.
            if current_time - last_send_time < 60 * resend_count:
                wait_time = 60 * resend_count - int(current_time - last_send_time)
                show_text(
                    f"Please wait for {str(wait_time//60).zfill(2)}:{wait_time-60*(wait_time//60)} minute(s).",
                    "f",
                )
                time.sleep(0.2)
                refresh()
            else:
                otp = generate_otp()
                # Send OTP to the email.
                if send_otp(email, otp):
                    last_send_time = current_time
                    resend_count += 1
                    show_text(f"Success! OTP sent to your email.", "s")
                    time.sleep(0.2)
                    refresh()

    def login_and_verify():
        """
         Checks the OTP entered by the user and verifies it. If it's correct the user is redirected to the login page.
         
         
         @return True if login is successful
        """
        entered_otp = password_entry.get()
        correct_otp = otp

        # This function is called when the user enters the OTP.
        if not entered_otp:
            show_text("Error, Please enter the OTP.", "f")
            time.sleep(0.2)
            refresh()
            return
        elif entered_otp == correct_otp:
            show_text("Login Sucessful.", "s")
            time.sleep(0.2)
            refresh()
            root.destroy()
            two()
        elif entered_otp != correct_otp:
            show_text("Wrong OTP.", "f")
            time.sleep(0.2)
            refresh()
            return

    logo_img = tk.PhotoImage(file="logo.png")
    logo_img = logo_img.subsample(1)

    create_logo(root, width, height, logo_img)
    exit_button(root, width, height)

    sign_in_image = Image.open("images\\hyy.png")
    photo = ImageTk.PhotoImage(sign_in_image)
    sign_in_image_label = tk.Label(root, image=photo, bg="#ffffff")
    sign_in_image_label.image = photo
    sign_in_image_label.place(x=100, y=110)
    sign_in_image_label.update()
    sign_in_image_label.place(x=(width - sign_in_image_label.winfo_width()) // 2, y=110)

    sign_in_label = tk.Label(
        root, text="Login", bg="white", fg="black", font=("yu gothic ui", 17, "bold")
    )
    sign_in_label.place(x=100, y=102)
    sign_in_label.update()
    sign_in_label.place(
        x=(width - sign_in_label.winfo_width()) // 2,
        y=(sign_in_image_label.winfo_height()) + 110,
    )

    subtitle_label = tk.Label(
        root, text="*Only authorised users", bg="white", fg="black"
    )
    subtitle_label.place(x=100, y=102)
    subtitle_label.update()
    subtitle_label.place(
        x=(width - subtitle_label.winfo_width()) // 2,
        y=(sign_in_image_label.winfo_height()) + 106 + sign_in_label.winfo_height(),
    )

    username_label = tk.Label(
        root,
        text="Email ID",
        bg="#ffffff",
        fg="#000000",
        font=("yu gothic ui", 13, "bold"),
    )
    username_label.place(x=100, y=280)

    username_entry = tk.Entry(
        root,
        highlightthickness=0,
        relief=tk.FLAT,
        bg="#ffffff",
        fg="#000000",
        font=("yu gothic ui", 12, "bold"),
        insertbackground="#6b6a69",
    )
    username_entry.place(x=130, y=303, width=270)

    username_line = tk.Canvas(
        root, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0
    )
    username_line.place(x=100, y=329)

    username_icon = Image.open("images\\username_icon.png")
    photo = ImageTk.PhotoImage(username_icon)
    username_icon_label = tk.Label(root, image=photo, bg="#ffffff")
    username_icon_label.image = photo
    username_icon_label.place(x=100, y=303)

    password_label = tk.Label(
        root,
        text="Enter OTP",
        bg="#ffffff",
        fg="#000000",
        font=("yu gothic ui", 13, "bold"),
    )
    password_label.place(x=100, y=350)

    password_entry = tk.Entry(
        root,
        highlightthickness=0,
        relief=tk.FLAT,
        bg="#ffffff",
        fg="#000000",
        font=("yu gothic ui", 12, "bold"),
        insertbackground="#6b6a69",
    )
    vcmd = (root.register(validate_input), "%P")
    password_entry.config(validate="key", validatecommand=vcmd)
    password_entry.place(x=130, y=384, width=270)

    password_line = tk.Canvas(
        root, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0
    )
    password_line.place(x=100, y=410)

    password_icon = Image.open("images\\password_icon.png")
    photo = ImageTk.PhotoImage(password_icon)
    password_icon_label = tk.Label(root, image=photo, bg="#ffffff")
    password_icon_label.image = photo
    password_icon_label.place(x=100, y=384)

    lgn_button = Image.open("login1.png")
    photo = ImageTk.PhotoImage(lgn_button)
    lgn_button_label = tk.Label(root, image=photo, bg="#ffffff")
    lgn_button_label.image = photo
    lgn_button_label.place(x=100, y=430)
    login = tk.Button(
        lgn_button_label,
        text="LOGIN",
        font=("yu gothic ui", 12, "bold"),
        bd=0,
        bg="#2196f3",
        cursor="hand2",
        activebackground="#2196f3",
        fg="white",
        command=login_and_verify,
    )
    login.place(x=13, y=8, width=109)

    sendotp_button = Image.open("login1.png")
    photo1 = ImageTk.PhotoImage(sendotp_button)
    sendotp_button_label = tk.Label(root, image=photo, bg="#ffffff")
    sendotp_button_label.image = photo1
    sendotp_button_label.place(x=265, y=430)
    sendotp = tk.Button(
        sendotp_button_label,
        text="SEND OTP",
        font=("yu gothic ui", 12, "bold"),
        bd=0,
        bg="#2196f3",
        cursor="hand2",
        activebackground="#2196f3",
        fg="white",
        command=send_otp_button,
    )
    sendotp.place(x=13, y=8, width=109)

    def show_text(message, command):
        """
         Display a message in the text area. This is a wrapper around insert_text_with_typing_animation to allow typing animations
         
         @param message - The message to display.
         @param command - The command to use for typing animations ( s or f
        """
        # The command to be used for the background color
        if command == "s":
            bg = "#82ad8c"
        elif command == "f":
            bg = "#bf5252"
        else:
            bg = "#f0f4f9"
        output_box = tk.Text(
            root,
            height=1,
            bg=bg,
            fg="black",
            font=("Cascadia Code", 12),
            wrap="word",
            state="disabled",
        )
        output_box.place(x=100, y=height - 115, width=300)
        output_box.config(state=tk.NORMAL)
        output_box.delete("1.0", tk.END)
        insert_text_with_typing_animation(output_box, message)
        output_box.config(state=tk.DISABLED)

    def refresh():
        """
         Refresh the tkinter window to make it look like it was in the last
        """
        frame = tk.Frame(root, bg="white", borderwidth=0)
        frame.place(x=0, y=height - 117, height=30, width=width)

    root.mainloop()


# ============================================================================================
# ============================================================================================


def seats():
    """
     Manage seats and create / update window. This function is called when the user clicks on the " Manage Seats " button.
     
     
     @return A Tkinter widget to interact with the user
    """
    def retrieve_data():
        """
         Retrieve venue information from database and store in list for display in GUI
        """
        ref = db.reference("/seats")
        data = ref.get()
        venue_info_list.clear()
        # Add Venue information to the list of venues.
        for key, value in data.items():
            venue = key
            rows = value.get("row", "N/A")
            columns = value.get("column", "N/A")
            venue_info_list.append(f"Venue: {venue}\nRows: {rows}\nColumns: {columns}")

    root = tk.Tk()
    root.title("Manage Seats")
    root.overrideredirect(True)
    width = 800
    height = 675

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.wm_attributes("-topmost", 1)
    root.configure(bg="white")

    logo_img = tk.PhotoImage(file="logo.png")
    logo_img = logo_img.subsample(1)
    create_logo(root, width, height, logo_img)
    exit_button(root, width, height)

    lbl = tk.Label(
        root,
        text="SEATS:",
        width=21,
        anchor="w",
        height=1,
        fg="black",
        bg="white",
        font=("Sitka Text Semibold", 15, " bold "),
    )
    lbl.place(x=125 - 75, y=130 - 20)

    table_frame = tk.Frame(root)
    scroll_height = 265 + 130
    table_frame.place(x=0, y=170 - 20, width=width, height=scroll_height)

    canvas = tk.Canvas(table_frame)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    table_frame_inside_canvas = tk.Frame(canvas)
    canvas.create_window((0, 0), window=table_frame_inside_canvas, anchor="nw")
    ref = db.reference("/")
    data = ref.get()

    def create_rounded_rect(text):
        """
         Creates a rounded rectangle with the given text. It is used to show the progress of the image
         
         @param text - Text to show in the rectangle
         
         @return ImageTk. PhotoImage with the rounded rectangle
        """
        width = 100
        height = 100
        image = Image.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 12)
        text_color = (0, 0, 0)
        text_bbox = draw.textbbox((0, 0), text, font)
        x = (width - text_bbox[2] - text_bbox[0]) // 2
        y = (height - text_bbox[3] - text_bbox[1]) // 2
        draw.text((x, y), text, fill=text_color, font=font)
        photo_image = ImageTk.PhotoImage(image)
        return photo_image

    tick_button_image = tk.PhotoImage(file="tick.png")

    def add_section():
        """
         Adds a section to the program. It is used to enter information about the program and to provide a way to validate the user input.
         
         
         @return A tk. Frame containing the frame and the text
        """
        frame = tk.Frame(root, width=width, bg="white", borderwidth=0)
        frame.place(x=0, y=height - 128, height=60)
        lbl = tk.Label(
            root,
            text="Enter Venue:",
            anchor="w",
            height=1,
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        lbl.place(x=45, y=height - 126, width=150)
        txt = tk.Entry(root, bg="blue", fg="white", font=("Times New Roman", 15))
        txt.place(x=47, y=height - 100, width=150)

        def validate_numeric_input(P):
            """
             Validates the input to be a numeric. This is a helper function for validate_input ()
             
             @param P - The string to be validated
             
             @return True if P is valid False if not or if P is
            """
            # Return true if P is a digit or a digit.
            if P == "" or P.isdigit():
                return True
            else:
                return False

        validate_numeric_input_command = root.register(validate_numeric_input)

        lbl_rows = tk.Label(
            root,
            text="Rows:",
            anchor="w",
            height=1,
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        lbl_rows.place(x=150 + 20 + 45, y=height - 126, width=50)
        txt_rows = tk.Entry(root, bg="blue", fg="white", font=("Times New Roman", 15))
        txt_rows.config(
            validate="key", validatecommand=(validate_numeric_input_command, "%P")
        )
        txt_rows.place(x=170 + 47, y=height - 100, width=50)
        lbl_cols = tk.Label(
            root,
            text="Cols:",
            anchor="w",
            height=1,
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        lbl_cols.place(x=170 + 70 + 45, y=height - 126, width=50)
        txt_cols = tk.Entry(root, bg="blue", fg="white", font=("Times New Roman", 15))
        txt_cols.config(
            validate="key", validatecommand=(validate_numeric_input_command, "%P")
        )
        txt_cols.place(x=170 + 70 + 47, y=height - 100, width=50)

        def handle_add():
            """
             Adds venue to database. This function is called when user clicks add button.
             
             
             @return whether or not the operation was successful. If successful the data will be
            """
            new_seat_name = txt.get()
            new_seat_row = txt_rows.get()
            new_seat_column = txt_cols.get()
            # If the new_seat_row or new_seat_column is 0 show the text.
            if int(new_seat_row) == 0 or int(new_seat_column) == 0:
                show_text("Row or column cannot be 0.")
                refresh_data()
                return

            confirmation = f"Venue: {new_seat_name}\nRows: {new_seat_row}\nColumns: {new_seat_column}\n\nDo you want to add this venue?"
            response = messagebox.askyesno(
                "Confirmation", confirmation, default=messagebox.NO
            )

            # response response is true if successful
            if response:
                ref = db.reference("/seats")
                new_seat_data = {"row": new_seat_row, "column": new_seat_column}
                ref.update({new_seat_name: new_seat_data})
                show_text("Venue added successfully.")
                refresh_data()

        tick_button = tk.Button(
            root,
            image=tick_button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
            command=handle_add,
        )
        tick_button.place(x=170 + 70 + 10 + 47 + 50, y=height - 100)
        root.bind("<Return>", lambda event: handle_add())

    delete_button_image = tk.PhotoImage(file="delete.png")

    def edit_section(venue, rows, cols):
        """
         Edit a venue in Tkinter. This is a bit tricky because we don't have a way to tell the user if they want to edit an existing section or not.
         
         @param venue - The name of the venue being edited
         @param rows - The number of rows in the section
         @param cols - The number of columns in the section ( must be greater than 0 )
         
         @return A tk. Frame containing the edit form and the
        """
        frame = tk.Frame(root, width=width, bg="white", borderwidth=0)
        frame.place(x=0, y=height - 128, height=60)
        lbl = tk.Label(
            root,
            text="Venue:",
            anchor="w",
            height=1,
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        lbl.place(x=45, y=height - 126, width=150)
        txt = tk.Entry(root, bg="white", fg="black", font=("Times New Roman", 15))
        txt.insert(0, venue)
        txt.config(state="readonly")
        txt.place(x=47, y=height - 100, width=150)

        def validate_numeric_input(P):
            """
             Validates the input to be a numeric. This is a helper function for validate_input ()
             
             @param P - The string to be validated
             
             @return True if P is valid False if not or if P is
            """
            # Return true if P is a digit or a digit.
            if P == "" or P.isdigit():
                return True
            else:
                return False

        validate_numeric_input_command = root.register(validate_numeric_input)

        lbl_rows = tk.Label(
            root,
            text="Rows:",
            anchor="w",
            height=1,
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        lbl_rows.place(x=150 + 20 + 45, y=height - 126, width=50)
        txt_rows = tk.Entry(root, bg="blue", fg="white", font=("Times New Roman", 15))
        txt_rows.config(
            validate="key", validatecommand=(validate_numeric_input_command, "%P")
        )
        txt_rows.insert(0, rows)
        txt_rows.place(x=170 + 47, y=height - 100, width=50)
        lbl_cols = tk.Label(
            root,
            text="Cols:",
            anchor="w",
            height=1,
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        lbl_cols.place(x=170 + 70 + 45, y=height - 126, width=50)
        txt_cols = tk.Entry(root, bg="blue", fg="white", font=("Times New Roman", 15))
        txt_cols.config(
            validate="key", validatecommand=(validate_numeric_input_command, "%P")
        )
        txt_cols.insert(0, cols)
        txt_cols.place(x=170 + 70 + 47, y=height - 100, width=50)

        def handle_edit():
            """
             Edits the venue's position. This is called when the user presses the edit button
             
             
             @return whether or not the editing
            """
            new_row_no = txt_rows.get()
            new_col_no = txt_cols.get()
            # if new_row_no or new_col_no is 0 show text
            if int(new_row_no) == 0 or int(new_col_no) == 0:
                show_text("Row or column cannot be 0.")
                refresh_data()
                return

            # if new_row_no and new_col_no are different
            if (new_row_no != rows or new_col_no != cols) and not (
                new_row_no == rows and new_col_no == cols
            ):
                confirmation = f"Venue: {venue}\nRows: {rows}\nColumns: {cols}\n\nNew Rows: {new_row_no}\nNew Columns: {new_col_no}\n\nDo you want to proceed?"
                response = messagebox.askyesno(
                    "Confirmation", confirmation, default=messagebox.NO
                )

                # the new position of the venation
                if response:
                    ref = db.reference("/seats")
                    new_position = {"column": new_col_no, "row": new_row_no}
                    ref.child(f"{venue}").set(new_position)
                    show_text("Changes applied successfully.")
                    refresh_data()
                else:
                    show_text("No changes were made.")
            else:
                show_text("No changes were made.")

        def handle_delete():
            """
             Delete venue from database and refresh data if successfull Args : None
            """
            confirmation = f"Venue: {venue}\n\nDo you want to delete?"
            response = messagebox.askyesno(
                "Confirmation", confirmation, default=messagebox.NO
            )

            # Delete the Venue from the Venue
            if response:
                ref = db.reference("/seats")
                ref.child(f"{venue}").delete()
                show_text("Venue deleted successfully.")
                refresh_data()
            else:
                show_text("No changes made")

        tick_button = tk.Button(
            root,
            image=tick_button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
            command=handle_edit,
        )
        tick_button.place(x=170 + 70 + 10 + 47 + 50, y=height - 100)
        root.bind("<Return>", lambda event: handle_edit())

        delete_button = tk.Button(
            root,
            image=delete_button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
            command=handle_delete,
        )
        delete_button.place(x=375, y=height - 100)
        root.bind("<Delete>", lambda event: handle_delete())

    def extract_venue_info(data):
        """
         Extract venue information from JSON. This is a helper function to extract venue information from JSON data.
         
         @param data - The JSON data that will be used to extract information.
         
         @return A list of strings that will be printed to the console
        """
        venue_info = []
        # Add Venue information to the VenueInfo.
        for key, value in data.get("seats", {}).items():
            venue = key
            rows = value.get("row", "N/A")
            columns = value.get("column", "N/A")
            venue_info.append(f"Venue: {venue}\nRows: {rows}\nColumns: {columns}")
        return venue_info

    venue_info_list = extract_venue_info(data)
    i = 0
    j = 0
    m = 0
    # Create a button for each venue info
    for item in venue_info_list:
        x = i * 120 + 20
        # Move to the left of the screen
        if x > width - 120:
            j += 1
            i = 0
        x = i * 120 + 20
        y = j * 120 + 20
        image = create_rounded_rect(item)

        button = ttk.Button(
            table_frame_inside_canvas, image=image, style="Rounded.TButton"
        )
        button.config(command=lambda num=m: button_callback(num))
        button.image = image
        button.grid(row=j, column=i, padx=(10, 10), pady=(10, 10))
        m += 1
        i += 1

    def button_callback(num):
        """
         Callback for button press. Parses the venue info and calls edit_section to edit the section
         
         @param num - The number of the
        """
        input_string = venue_info_list[num]
        lines = input_string.split("\n")

        # Returns the number of rows rows and columns from the lines of the file.
        for line in lines:
            # Returns the number of rows rows and columns from the line.
            if line.startswith("Venue:"):
                venue = line.split(":")[1].strip()
            elif line.startswith("Rows:"):
                rows = int(line.split(":")[1].strip())
            elif line.startswith("Columns:"):
                columns = int(line.split(":")[1].strip())

        edit_section(venue, rows, columns)

    style = ttk.Style()
    style.configure("Rounded.TButton", borderwidth=0, relief="flat")
    style.configure(
        "RoundedW.TButton", borderwidth=0, relief="flat", background="white"
    )
    # Move to the left of the screen
    if x > width - 240:
        i = 0
        j += 1
    plus_button_image = tk.PhotoImage(file="seat_plus.png")
    plus_button = ttk.Button(
        table_frame_inside_canvas,
        image=plus_button_image,
        style="Rounded.TButton",
        command=add_section,
    )
    plus_button.image = plus_button_image
    plus_button.grid(row=j, column=i, padx=(10, 10), pady=(10, 10))

    def show_text(message):
        """
         Display a text box. This is a convenience function to make it easier to use it in a program's main loop
         
         @param message - The message to display
        """
        textbox(root, message, 410, height - 100, 345)

    def on_canvas_configure(event):
        """
         Called when the canvas is configured. This is a callback function and should be used to reconfigure the canvas to fit the table_frame_inside_canvas
         
         @param event - The event that triggered this
        """
        canvas.configure(scrollregion=canvas.bbox("all"))
        table_frame_inside_canvas.config(width=canvas.winfo_width())

    canvas.bind("<Configure>", on_canvas_configure)

    def handle_scroll(event):
        """
         Scroll the canvas vertically. This is called when the user scrolls a view.
         
         @param event - The event that triggered this function call. It's passed to the event handler
        """
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    canvas.bind_all("<MouseWheel>", handle_scroll)

    def handle_back():
        """
         Called when the user presses back. Destroys the window and calls two
        """
        root.destroy()
        two()

    back_button_image = tk.PhotoImage(file="back.png")
    create_back_button(root, handle_back, 7, 110, back_button_image)

    def refresh_data():
        """
         Refresh venue data from Tkinter and display it in the table
        """
        frame = tk.Frame(root, width=width, bg="white", borderwidth=0)
        frame.place(x=0, y=height - 128, height=60)

        # Destroy all widgets inside canvas.
        for widget in table_frame_inside_canvas.winfo_children():
            widget.destroy()

        venue_info_list.clear()

        retrieve_data()

        i = 0
        j = 0
        m = 0
        # Create a button for each venue info
        for item in venue_info_list:
            x = i * 120 + 20

            # Move to the left of the screen
            if x > width - 120:
                j += 1
                i = 0
            x = i * 120 + 20
            y = j * 120 + 20
            image = create_rounded_rect(item)

            button = ttk.Button(
                table_frame_inside_canvas, image=image, style="Rounded.TButton"
            )
            button.config(command=lambda num=m: button_callback(num))
            button.image = image
            button.grid(row=j, column=i, padx=(10, 10), pady=(10, 10))
            m += 1
            i += 1

        # Move to the left of the screen
        if x > width - 240:
            i = 0
            j += 1
        plus_button_image = tk.PhotoImage(file="seat_plus.png")
        plus_button = ttk.Button(
            table_frame_inside_canvas,
            image=plus_button_image,
            style="Rounded.TButton",
            command=add_section,
        )
        plus_button.image = plus_button_image
        plus_button.grid(row=j, column=i, padx=(10, 10), pady=(10, 10))

        canvas.configure(scrollregion=canvas.bbox("all"))
        table_frame_inside_canvas.config(width=canvas.winfo_width())

    refresh_button_image = tk.PhotoImage(file="refresh.png")
    refresh_button = ttk.Button(
        root, image=refresh_button_image, style="RoundedW.TButton", command=refresh_data
    )
    refresh_button.place(x=width - 70, y=height - 66)

    root.mainloop()


# ============================================================================================
# ============================================================================================


def department():
    """
     Create department selection window and return it as Tkinter widget. This widget is used to select a department
    """
    root = tk.Tk()
    root.title("Select Department")
    root.overrideredirect(True)
    width = 580
    height = 650
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg="white")

    logo_img = tk.PhotoImage(file="logo.png")
    logo_img = logo_img.subsample(1)
    create_logo(root, width, height, logo_img)
    exit_button(root, width, height)

    lbl = tk.Label(
        root,
        text="DEPARTMENTS:",
        width=21,
        anchor="w",
        height=1,
        fg="black",
        bg="white",
        font=("Sitka Text Semibold", 15, " bold "),
    )
    lbl.place(x=125 - 75, y=130 - 20)

    table_frame = tk.Frame(root, bg="white")
    scroll_height = 320
    table_frame.place(x=0, y=170 - 20, width=width, height=scroll_height)
    canvas = tk.Canvas(table_frame, bg="white")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    table_frame_inside_canvas = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=table_frame_inside_canvas, anchor="nw")

    def button_pressed(button_number, button_type):
        """
         Called when a button is pressed. Department or Edit buttons are handled by this function
         
         @param button_number - The number of the button that was pressed
         @param button_type - The type of button that was pressed
        """
        # destroy the tree and branches of the department
        if button_type == "Department":
            root.destroy()
            branches(department_names[button_number])
        elif button_type == "Edit":
            edit_section(department_names[button_number], button_number)

    def show_text(message):
        """
         Display a text box. This is a convenience function to call : func : ` pyglet. display. textbox `
         
         @param message - The message to display
        """
        textbox(root, message, 47, height - 115, 486)

    button_image = tk.PhotoImage(file="edit.png")
    i = 0
    # Create a button for the department.
    if len(department_names) == 0:
        color, fg = pick_color()
        txt = tk.Button(
            table_frame_inside_canvas,
            text="No department present.",
            anchor="w",
            width=38,
            height=1,
            bg=color,
            fg=fg,
            bd=1,
            font=("Times New Roman", 15),
        )
        txt.grid(row=i, column=0, padx=(50, 8), pady=5)

    # Generates a tk. Button for each department in the department_names.
    for department in department_names:
        color, fg = pick_color()
        txt = tk.Button(
            table_frame_inside_canvas,
            text=f" {department}",
            command=lambda num=i: button_pressed(num, "Department"),
            anchor="w",
            width=38,
            height=1,
            bg=color,
            fg=fg,
            bd=1,
            font=("Times New Roman", 15),
        )
        txt.grid(row=i, column=0, padx=(50, 8), pady=5)
        button = tk.Button(
            table_frame_inside_canvas,
            image=button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
        )
        button.config(command=lambda num=i: button_pressed(num, "Edit"))
        button.grid(row=i, column=1)
        i += 1

    def on_canvas_configure(event):
        """
         Called when the canvas is configured. This is a callback function and should be used to configure the canvas to fit the contents of the view.
         
         @param event - The event that triggered this function call. It is passed as an argument
        """
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_canvas_configure)

    def handle_scroll(event):
        """
         Scroll the canvas vertically. This is called when the user scrolls a view.
         
         @param event - The event that triggered this function call. It's passed to the event handler
        """
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    canvas.bind_all("<MouseWheel>", handle_scroll)

    tick_button_image = tk.PhotoImage(file="tick.png")
    delete_button_image = tk.PhotoImage(file="delete.png")

    def edit_section(department, num):
        """
         Edit section of department. This function is called when user presses enter in section of department.
         
         @param department - String of department name. E. g.
         @param num - Number of section to
        """
        frame = tk.Frame(root, width=width, height=100, bg="white", borderwidth=0)
        frame.place(x=0, y=470)
        lbl = tk.Label(
            root,
            text="Enter Department Name:",
            width=53,
            anchor="w",
            height=1,
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        lbl.place(x=45, y=height - 176)
        txt = tk.Entry(
            root, width=42, bg="blue", fg="white", font=("Times New Roman", 15)
        )
        txt.insert(0, department)
        txt.place(x=47, y=height - 150)

        def handle_edit():
            """
             Edits department's name in the database. Args : txt : Textbox containing name of new
            """
            new_department_name = txt.get()
            # This function will update the department list.
            if new_department_name != department:
                confirmation = f"Old Name: {department}\nNew Name: {new_department_name}\n\nDo you want to proceed?"
                response = messagebox.askyesno(
                    "Confirmation", confirmation, default=messagebox.NO
                )
                # update department_names department_names list department_names department_names num department_names department_names department_names department_names
                if response:
                    # update department_names department_names and update department_names list
                    if (
                        new_department_name != department
                        and new_department_name.lower()
                        not in (name.lower() for name in department_names)
                    ):
                        root_ref = db.reference("/departments")
                        # Delete the department from the database.
                        if department in root_ref.get():
                            old_department_data = root_ref.child(department).get()
                            root_ref.child(department).delete()
                            root_ref.update({new_department_name: old_department_data})
                        else:
                            print(
                                f"Department '{department}' not found in the database."
                            )
                        department_names[num] = new_department_name
                        show_text("Department Name Edited Successfully.")
                        refresh_department_list()
                    elif new_department_name.lower() in (
                        name.lower() for name in department_names
                    ):
                        show_text("Department already exist.")
                    else:
                        show_text("No changes made.")
            else:
                show_text("No changes made.")

        def handle_delete():
            """
             Delete department from database and refresh list of departments if successfull. Confirmation is shown in main
            """
            confirmation = f"Department Name: {department}\n\nDo you want to delete?"
            response = messagebox.askyesno(
                "Confirmation", confirmation, default=messagebox.NO
            )
            # delete department from the database
            if response:
                root_ref = db.reference("/departments")
                # Delete the department from the database.
                if department in root_ref.get():
                    department_ref = root_ref.child(department)
                    department_ref.delete()
                    show_text("Department deleted sucessfully.")
                    refresh_department_list()
                else:
                    show_text("Department not found in the database.")
            else:
                show_text("No changes made")

        tick_button = tk.Button(
            root,
            image=tick_button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
            command=handle_edit,
        )
        tick_button.place(x=480, y=height - 150)
        root.bind("<Return>", lambda event: handle_edit())

        delete_button = tk.Button(
            root,
            image=delete_button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
            command=handle_delete,
        )
        delete_button.place(x=513, y=height - 150)
        root.bind("<Delete>", lambda event: handle_delete())

    def add_section():
        """
         Add section to department list. This is used to add a new departments to the system.
         
         
         @return A Tkinter Frame containing the section that was
        """
        frame = tk.Frame(root, width=width, height=100, bg="white", borderwidth=0)
        frame.place(x=0, y=470)
        lbl = tk.Label(
            root,
            text="Enter Department Name:",
            width=53,
            anchor="w",
            height=1,
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        lbl.place(x=45, y=height - 176)
        txt = tk.Entry(
            root, width=42, bg="blue", fg="white", font=("Times New Roman", 15)
        )
        txt.place(x=47, y=height - 150)

        def handle_add():
            """
             Add department to database. This function is called when user presses add button.
             
             
             @return True if user confirms success False if user cancel
            """
            new_department_name = txt.get()
            new_department_data = {"branches": ""}
            # This function will confirm that the user has a new department name.
            if (
                new_department_name.strip() != ""
                and new_department_name.lower()
                not in (name.lower() for name in department_names)
            ):
                confirmation = f"Name: {new_department_name}\n\nDo you want to add?"
                response = messagebox.askyesno(
                    "Confirmation", confirmation, default=messagebox.NO
                )
            elif new_department_name.lower() in (
                name.lower() for name in department_names
            ):
                show_text("Department already exist.")
            else:
                show_text("Not a valid Department Name.")
                return
            # update department list if successful
            if response:
                root_ref = db.reference("/departments")
                # Update the root_ref with new_department_name and update the new_department_data
                if new_department_name not in root_ref.get():
                    root_ref.update({new_department_name: new_department_data})
                show_text("Department Added Successfully.")
                refresh_department_list()
            else:
                show_text("No changes made")

        tick_button = tk.Button(
            root,
            image=tick_button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
            command=handle_add,
        )
        tick_button.place(x=480, y=height - 150)
        root.bind("<Return>", lambda event: handle_add())

    def handle_back():
        """
         Called when the user presses back. Destroys the window and calls two
        """
        root.destroy()
        two()

    back_button_image = tk.PhotoImage(file="back.png")
    create_back_button(root, handle_back, 7, 110, back_button_image)

    style = ttk.Style()
    style.configure("Rounded.TButton", borderwidth=0, relief="flat", background="white")

    plus_button_image = tk.PhotoImage(file="pluss.png")
    plus_button = ttk.Button(
        root, image=plus_button_image, style="Rounded.TButton", command=add_section
    )
    plus_button.place(x=width - 70, y=height - 66)

    def refresh_department_list():
        """
         Refresh department list from Firebase. Args : None. None. Refreshes the list of departments
        """
        # Destroy all widgets inside canvas.
        for widget in table_frame_inside_canvas.winfo_children():
            widget.destroy()
        department_names.clear()
        root_ref = db.reference("/departments")
        try:
            root_ref = db.reference("/")
            departments_ref = root_ref.child("departments")
            data = departments_ref.get()
            # Add all department names to the list of departments_ref
            if data:
                # Add the names of all department names to the list of department names.
                for department in departments_ref.get():
                    department_names.append(department)
        except Exception as e:
            internet_connection()
            print("Error reading data from Firebase:", e)
        i = 0
        # Create a button for the department.
        if len(department_names) == 0:
            color, fg = pick_color()
            txt = tk.Button(
                table_frame_inside_canvas,
                text="No department present.",
                anchor="w",
                width=38,
                height=1,
                bg=color,
                fg=fg,
                bd=1,
                font=("Times New Roman", 15),
            )
            txt.grid(row=i, column=0, padx=(50, 8), pady=5)
        # Generates a tk. Button for each department in the department_names
        for department in department_names:
            color, fg = pick_color()
            txt = tk.Button(
                table_frame_inside_canvas,
                text=f" {department}",
                command=lambda num=i: button_pressed(num, "Department"),
                anchor="w",
                width=38,
                height=1,
                bg=color,
                fg=fg,
                bd=1,
                font=("Times New Roman", 15),
            )
            txt.grid(row=i, column=0, padx=(50, 8), pady=5)
            button = tk.Button(
                table_frame_inside_canvas,
                image=button_image,
                bd=0,
                highlightbackground="white",
                bg="white",
                highlightcolor="white",
            )
            button.config(command=lambda num=i: button_pressed(num, "Edit"))
            button.grid(row=i, column=1)
            i += 1
        frame = tk.Frame(root, width=width, height=100, bg="white", borderwidth=0)
        frame.place(x=0, y=470)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def add_many_return(x, y):
        """
         Add many departments to the list. This is a function to be called when user presses Return
         
         @param x - number of the department to add
         @param y - number of the department to add ( 0 = don't add
        """
        # Show the department s added and all departments already exist.
        if y == 0:
            show_text(f"{x} department(s) added.")
        elif x == 0:
            show_text(f"All department(s) already exist.")
        else:
            show_text(f"{x} department(s) added and {y} department(s) already exist.")
        refresh_department_list()

    def add_many_dept():
        """
         Add many departments to the database. This is a command that allows to add a department to the database and asks the user if he wants to do so.
         
         
         @return True if successful False otherwise. In case of error the user is prompted
        """
        def handle_many_add(text):
            """
             Add a department to the departments list. This is a batch add operation
             
             @param text - text of the command
            """
            new_department_name = text
            new_department_data = {"branches": ""}
            root_ref = db.reference("/departments")
            root_ref.update({new_department_name: new_department_data})
            department_names.clear()
            data = root_ref.get()
            # Add department names to the department names.
            if data:
                department_names.extend(list(data.keys()))

        def get_departments():
            """
             Get departments from user and add them to game. This is a function that handles the addition of departments to game.
             
             
             @return tuple of x y coordinates of new departments ( 0 - 3
            """
            departments = text_input.get("1.0", "end-1c").split("\n")
            departments = [dept.strip() for dept in departments if dept.strip()]
            # Show the departments text.
            if not departments:
                show_text("No departments entered.")
                return
            num_departments = len(departments)
            confirmation = f"Do you want to submit {num_departments} department(s)?\n\nCheck once before submitting."
            response = messagebox.askyesno(
                "Confirmation", confirmation, default=messagebox.NO
            )
            # Add a new department to the list of departments.
            if response:
                x, y = 0, 0
                # Add a department to the list of departments
                for department in departments:
                    # Add a department to the list of department names.
                    if department.lower() in (
                        name.lower() for name in department_names
                    ):
                        y += 1
                    else:
                        handle_many_add(department)
                        x += 1
                show_text("Done..Closing in 3..2..1")
                root1.destroy()
                return add_many_return(x, y)
            else:
                show_text("No departments entered.")

        def show_text(message):
            """
             Show text in output box. This is a convenience function for insert_text_with_typing_animation
             
             @param message - Text to be displayed
            """
            insert_text_with_typing_animation(output_box, message)

        root1 = tk.Tk()
        root1.title("Enter Departments")
        root1.wm_attributes("-topmost", 1)
        instructions = tk.Label(
            root1,
            text="Enter departments separated by line breaks:",
            font=("Times New Roman", 12),
        )
        instructions.pack(pady=5)
        text_input = tk.Text(root1, width=40, height=10, font=("Times New Roman", 12))
        text_input.pack(padx=20)
        output_box = tk.Text(
            root1,
            width=40,
            height=1,
            bg="grey",
            fg="white",
            font=("Times New Roman", 12),
            wrap="word",
            state="disabled",
        )
        output_box.pack(padx=20, pady=10)
        output_box.config(state=tk.NORMAL)
        output_box.delete("1.0", tk.END)
        output_box.config(state=tk.DISABLED)
        submit_button = ttk.Button(
            root1, text="Submit", style="Rounded.TButton", command=get_departments
        )
        submit_button.pack(pady=10)
        root1.mainloop()

    edit_button = tk.Button(
        root,
        text="ADD MANY DEPT.",
        width=15,
        height=1,
        bg=color,
        fg=fg,
        font=("Sitka Text Semibold", 15, "bold"),
        command=add_many_dept,
    )
    edit_button.place(x=width - 350, y=height - 65)

    refresh_button_image = tk.PhotoImage(file="refresh.png")
    refresh_button = ttk.Button(
        root,
        image=refresh_button_image,
        style="Rounded.TButton",
        command=refresh_department_list,
    )
    refresh_button.place(x=width - 140, y=height - 66)

    root.mainloop()


# ============================================================================================
# ============================================================================================


def branches(dept_name):
    """
     Create and return tree of branches. It is possible to select branch by department name
     
     @param dept_name - Name of department to select branches for
     
     @return Tk object with tree of branches ( list of branch
    """
    root = tk.Tk()
    root.title("Select Branches")
    root.overrideredirect(True)
    width = 580
    height = 650
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg="white")

    logo_img = tk.PhotoImage(file="logo.png")
    logo_img = logo_img.subsample(1)

    create_logo(root, width, height, logo_img)
    exit_button(root, width, height)

    lbl = tk.Label(
        root,
        text="BRANCHES:",
        width=21,
        anchor="w",
        height=1,
        fg="black",
        bg="white",
        font=("Sitka Text Semibold", 15, " bold "),
    )
    lbl.place(x=125 - 75, y=155 - 20)

    table_frame = tk.Frame(root, bg="white")
    scroll_height = 300
    table_frame.place(x=0, y=190 - 20, width=width, height=scroll_height)

    canvas = tk.Canvas(table_frame, bg="white")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    table_frame_inside_canvas = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=table_frame_inside_canvas, anchor="nw")

    courses_list = ["BE", "BTech", "ME", "MTech", "MCA", "MSc", "4+1", "PhD"]

    path = dept_name

    dept_button = ttk.Button(root, text=path, style="Rounded.TButton")
    dept_button.place(x=125 - 75, y=130 - 20)

    branch_names = []
    root_ref = db.reference("/")
    branch_ref = root_ref.child(f"departments/{path}/branches")

    # Add branch names to branch names.
    for branch in branch_ref.get():
        branch_names.append(branch)

    def pick_color():
        """
         Pick a color and color for use in an image. This is a helper function to make it easy to use as a context manager.
         
         
         @return tuple of color and foreground ( hex ) strings to
        """
        color = "#{:02x}{:02x}{:02x}".format(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )
        # Return black black or white depending on color
        if is_dark_color(color):
            fg = "white"
        else:
            fg = "black"
        return color, fg

    def button_pressed(button_number, button_type):
        """
         Called when a button is pressed. Depending on the type of button this will destroy the semester or edit the branch
         
         @param button_number - The number of the button that was pressed
         @param button_type - The type of the button ( Branch Edit
        """
        # This function is called when the button is clicked.
        if button_type == "Branch":
            root.destroy()
            semester(dept_name, branch_names[button_number])
        elif button_type == "Edit":
            try:
                code, branch = branch_names[button_number].split(" - ")
            except:
                code, branch = branch_names[button_number], ""
            edit_section(code, branch, button_number)

    def show_text(message):
        """
         Display a text box. This is a convenience function to call : func : ` pyglet. display. textbox `
         
         @param message - The message to display
        """
        textbox(root, message, 47, height - 115, 486)

    button_image = tk.PhotoImage(file="edit.png")
    # Generate a button for the current branch.
    if len(branch_names) == 0:
        color = "#{:02x}{:02x}{:02x}".format(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )
        # Return black black or white depending on color
        if is_dark_color(color):
            fg = "white"
        else:
            fg = "black"
        txt = tk.Button(
            table_frame_inside_canvas,
            text=f"No branch present.",
            anchor="w",
            width=38,
            height=1,
            bg=color,
            fg=fg,
            bd=1,
            font=("Times New Roman", 15),
        )
        txt.grid(row=0, column=0, padx=(50, 8), pady=10)
    i = 0
    # Generates a tk. Button with the branch and edit buttons.
    for branch in branch_names:
        color = "#{:02x}{:02x}{:02x}".format(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )
        # Return black black or white depending on color
        if is_dark_color(color):
            fg = "white"
        else:
            fg = "black"
        txt = tk.Button(
            table_frame_inside_canvas,
            text=f"{branch}",
            command=lambda num=i: button_pressed(num, "Branch"),
            anchor="w",
            width=38,
            height=1,
            bg=color,
            fg=fg,
            bd=1,
            font=("Times New Roman", 15),
        )
        txt.grid(row=i, column=0, padx=(50, 8), pady=10)

        button = tk.Button(
            table_frame_inside_canvas,
            image=button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
        )
        button.config(command=lambda num=i: button_pressed(num, "Edit"))
        button.grid(row=i, column=1)

        i += 1

    def on_canvas_configure(event):
        """
         Called when the canvas is configured. This is a callback function and should be used to configure the canvas to fit the contents of the view.
         
         @param event - The event that triggered this function call. It is passed as an argument
        """
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_canvas_configure)

    def handle_scroll(event):
        """
         Scroll the canvas vertically. This is called when the user scrolls a view.
         
         @param event - The event that triggered this function call. It's passed to the event handler
        """
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    canvas.bind_all("<MouseWheel>", handle_scroll)
    tick_button_image = tk.PhotoImage(file="tick.png")
    delete_button_image = tk.PhotoImage(file="delete.png")

    def edit_section(code, branch, num):
        """
         Edit a section in Courses. This is a function to allow the user to edit an existing section.
         
         @param code - The code of the section to edit. This must be unique for the course.
         @param branch - The branch name that will be used to edit the section.
         @param num - The number of the section to edit. This must be a non - negative integer
        """
        lbl = tk.Label(
            root,
            text="Enter Branch Name:",
            width=53,
            anchor="w",
            height=1,
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        lbl.place(x=45, y=height - 176)

        options = courses_list
        selected_option = tk.StringVar()
        dropdown = ttk.Combobox(
            root,
            width=5,
            height=1,
            textvariable=selected_option,
            values=options,
            state="readonly",
            font=("Times New Roman", 14),
        )
        dropdown.place(x=47, y=height - 150)
        selected_option.set(code)

        txt = tk.Entry(
            root, width=35, bg="blue", fg="white", font=("Times New Roman", 15)
        )
        txt.insert(0, branch)
        txt.place(x=120, y=height - 150)

        def handle_edit():
            """
             Edit branch and update database if needed. This is called when user presses edit
            """
            new_branch_name = f"{selected_option.get()} - {txt.get()}"
            # Set the branch name to the branch name.
            if branch == "":
                old_branch_name = code
            else:
                old_branch_name = f"{code} - {branch}"
            department_name = path

            # This function is called when the user clicks on the new branch name.
            if new_branch_name != old_branch_name:
                confirmation = f"Old Name: {old_branch_name}\nNew Name: {new_branch_name}\n\nDo you want to proceed?"
                response = messagebox.askyesno(
                    "Confirmation", confirmation, default=messagebox.NO
                )
                # update the list of branches and update the list of branches
                if response:
                    # Update the branch list.
                    if new_branch_name.lower() not in (
                        name.lower() for name in branch_names
                    ):
                        root_ref = db.reference("/")
                        # delete branch and branch data from the database
                        if department_name in root_ref.child("departments").get():
                            branch_ref = root_ref.child(
                                f"departments/{department_name}/branches"
                            )
                            # Delete branch from branch_ref and update branch_ref.
                            if old_branch_name in branch_ref.get():
                                branch_data = branch_ref.child(old_branch_name).get()
                                branch_ref.child(old_branch_name).delete()
                                branch_ref.update({new_branch_name: branch_data})
                                show_text(
                                    f"Branch '{old_branch_name}' edited to '{new_branch_name}' in '{department_name}'"
                                )
                            else:
                                show_text(
                                    f"Branch '{old_branch_name}' does not exist in '{department_name}'"
                                )
                        else:
                            show_text(
                                f"Department '{department_name}' not found in the database."
                            )

                        branch_names[num] = new_branch_name
                        show_text("Branch Name Edited Successfully.")
                        refresh_branch_list()
                    elif new_branch_name.lower() in (
                        name.lower() for name in branch_names
                    ):
                        show_text("Branch already exist.")
                    else:
                        show_text("No changes made.")
                else:
                    show_text("No changes made.")

        def handle_delete():
            """
             Delete branch from department if it exists. Otherwise show error message and ask
            """
            # This function will confirm that the branch is deleted.
            if branch == "":
                confirmation = f"Branch Name: {code}\n\nDo you want to delete?"
                branch_to_delete = f"{code}"
            else:
                branch_to_delete = f"{code} - {branch}"
                confirmation = (
                    f"Branch Name: {code} - {branch}\n\nDo you want to delete?"
                )
            response = messagebox.askyesno(
                "Confirmation", confirmation, default=messagebox.NO
            )
            department_name = path
            # if response is true show the branch list
            if response:
                root_ref = db.reference("/")
                # Delete all branches from the database.
                if department_name in root_ref.child("departments").get():
                    branch_ref = root_ref.child(
                        f"departments/{department_name}/branches"
                    )
                    # Delete the branch from the branch_to_delete list
                    if branch_to_delete in branch_ref.get():
                        branch_ref.child(branch_to_delete).delete()
                        show_text(
                            f"Branch '{branch_to_delete}' deleted successfully from '{department_name}'"
                        )
                        refresh_branch_list()
                    else:
                        show_text(
                            f"Branch '{branch_to_delete}' does not exist in '{department_name}'"
                        )
                else:
                    show_text(
                        f"Department '{department_name}' not found in the database."
                    )
            else:
                show_text("No changes made")

        tick_button = tk.Button(
            root,
            image=tick_button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
            command=handle_edit,
        )
        tick_button.place(x=480, y=height - 150)
        root.bind("<Return>", lambda event: handle_edit())

        # Delete the branch if there is only one branch
        if len(branch_names) > 1:
            delete_button = tk.Button(
                root,
                image=delete_button_image,
                bd=0,
                highlightbackground="white",
                bg="white",
                highlightcolor="white",
                command=handle_delete,
            )
            delete_button.place(x=513, y=height - 150)
            root.bind("<Delete>", lambda event: handle_delete())

    def add_section():
        """
         Add a section to the treeview. This is used to allow users to add courses to the treeview without having to know the name of the branch they want to add.
         
         
         @return A tuple containing the label the combobox and the entry
        """
        lbl = tk.Label(
            root,
            text="Enter Branch Name:",
            width=53,
            anchor="w",
            height=1,
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        lbl.place(x=45, y=height - 176)

        options = courses_list
        selected_option = tk.StringVar()
        dropdown = ttk.Combobox(
            root,
            width=5,
            height=1,
            textvariable=selected_option,
            values=options,
            state="readonly",
            font=("Times New Roman", 14),
        )
        dropdown.place(x=47, y=height - 150)

        txt = tk.Entry(
            root, width=35, bg="blue", fg="white", font=("Times New Roman", 15)
        )
        txt.place(x=120, y=height - 150)

        def handle_add():
            """
             Add branch to database. This function is called when user presses add button.
             
             
             @return None or raises exception on error ( branch already exists
            """
            selected_option = dropdown.get()
            branch_name = txt.get()
            new_branch_name = f"{selected_option} - {branch_name}"

            # If branch_name is empty or empty string it will be replaced by selected_option.
            if not branch_name.strip():
                new_branch_name = f"{selected_option}"

            # Show a branch already exists.
            if new_branch_name.lower() in (name.lower() for name in branch_names):
                show_text("Branch already exists.")
                return

            confirmation = f"Name: {new_branch_name}\n\nDo you want to add?"
            response = messagebox.askyesno(
                "Confirmation", confirmation, default=messagebox.NO
            )
            root_ref = db.reference("/")

            # If the branch is already present in the list of departments
            if response:
                # Add a new branch to the list of branches.
                if path in root_ref.child("departments").get():
                    # Add a new branch to the branch tree.
                    if (
                        new_branch_name
                        not in root_ref.child(f"departments/{path}/branches").get()
                    ):
                        root_ref.update(
                            {
                                f"departments/{path}/branches/{new_branch_name}": {
                                    "semesters": ""
                                }
                            }
                        )
                        show_text(f"Branch added successfully.")
                    else:
                        show_text(f"Branch already exists.")
                    refresh_branch_list()
                else:
                    show_text("No changes made.")

        tick_button = tk.Button(
            root,
            image=tick_button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
            command=handle_add,
        )
        tick_button.place(x=480, y=height - 150)
        root.bind("<Return>", lambda event: handle_add())

        frame = tk.Frame(root, width=24, height=24, bg="white", borderwidth=0)
        frame.place(x=513, y=height - 150)

    def handle_back():
        """
         Called when the user presses back. Destroys the root window and calls department
        """
        root.destroy()
        department()

    back_button_image = tk.PhotoImage(file="back.png")
    create_back_button(root, handle_back, 7, 110, back_button_image)

    style = ttk.Style()
    style.configure("Rounded.TButton", borderwidth=0, relief="flat", background="white")

    plus_button_image = tk.PhotoImage(file="pluss.png")
    plus_button = ttk.Button(
        root, image=plus_button_image, style="Rounded.TButton", command=add_section
    )
    plus_button.place(x=width - 70, y=height - 66)

    def refresh_branch_list():
        """
         Refresh the list of branches. This is done by reading the database and adding branches
        """
        # Destroy all widgets inside canvas.
        for widget in table_frame_inside_canvas.winfo_children():
            widget.destroy()
        branch_names.clear()
        root_ref = db.reference(f"/departments/{path}/branches")
        data = root_ref.get()
        # Add branch names to branch names.
        if data:
            # Add branch names to the list of branches.
            for branch in data:
                branch_names.append(branch)

        i = 0
        # Create a button for the current branch.
        if len(branch_names) == 0:
            color, fg = pick_color()
            txt = tk.Button(
                table_frame_inside_canvas,
                text="No branch present.",
                anchor="w",
                width=38,
                height=1,
                bg=color,
                fg=fg,
                bd=1,
                font=("Times New Roman", 15),
            )
            txt.grid(row=i, column=0, padx=(50, 8), pady=5)

        # Generates a tk. Button with the branch and edit buttons.
        for branch in branch_names:
            color, fg = pick_color()
            txt = tk.Button(
                table_frame_inside_canvas,
                text=f" {branch}",
                command=lambda num=i: button_pressed(num, "Branch"),
                anchor="w",
                width=38,
                height=1,
                bg=color,
                fg=fg,
                bd=1,
                font=("Times New Roman", 15),
            )
            txt.grid(row=i, column=0, padx=(50, 8), pady=5)

            button = tk.Button(
                table_frame_inside_canvas,
                image=button_image,
                bd=0,
                highlightbackground="white",
                bg="white",
                highlightcolor="white",
            )
            button.config(command=lambda num=i: button_pressed(num, "Edit"))
            button.grid(row=i, column=1)

            i += 1

        frame = tk.Frame(root, width=width, height=100, bg="white", borderwidth=0)
        frame.place(x=0, y=470)

        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    refresh_button_image = tk.PhotoImage(file="refresh.png")
    refresh_button = ttk.Button(
        root,
        image=refresh_button_image,
        style="Rounded.TButton",
        command=refresh_branch_list,
    )
    refresh_button.place(x=width - 140, y=height - 66)

    root.mainloop()


# ============================================================================================
# ============================================================================================


def semester(dept_name, branch_name):
    """
     Create semester selection dialog. It is possible to select a branch by name or by code
     
     @param dept_name - name of the department that will be used for selection
     @param branch_name - name of the branch that will be
    """
    root = tk.Tk()
    root.title("Select Semester")
    root.overrideredirect(True)

    width = 580
    height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    root.geometry(f"{width}x{height}+{x}+{y}")

    root.configure(bg="white")

    try:
        br_code, br_name = branch_name.split(" - ")
    except:
        br_code, br_name = branch_name, ""

    logo_img = tk.PhotoImage(file="logo.png")
    logo_img = logo_img.subsample(1)

    create_logo(root, width, height, logo_img)
    exit_button(root, width, height)

    lbl = tk.Label(
        root,
        text="SEMESTER:",
        width=21,
        anchor="w",
        height=1,
        fg="black",
        bg="white",
        font=("Sitka Text Semibold", 15, " bold "),
    )
    lbl.place(x=125 - 75, y=155 - 20)

    def handle_navigation(text):
        """
         Handle navigation to Dept. This is called when the user navigates to a Dept.
         
         @param text - The text that was entered by the user in the
        """
        # Destroy the tree and all branches
        if text == "Dept":
            root.destroy()
            branches(dept_name)

    dept_button = ttk.Button(
        root,
        text=dept_name,
        style="Rounded.TButton",
        command=lambda: handle_navigation("Dept"),
    )
    dept_button.place(x=125 - 75, y=130 - 20)

    dept_button.update()
    branch_button = ttk.Button(root, text=f"{branch_name}", style="Rounded.TButton")
    branch_button.place(x=125 - 75 + dept_button.winfo_width(), y=130 - 20)

    table_frame = tk.Frame(root, bg="white")
    scroll_height = 300
    table_frame.place(x=0, y=190 - 20, width=width, height=scroll_height)

    canvas = tk.Canvas(table_frame, bg="white")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    table_frame_inside_canvas = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=table_frame_inside_canvas, anchor="nw")

    def show_text(message):
        """
         Display a text box. This is a convenience function to call : func : ` pyglet. display. textbox `
         
         @param message - The message to display
        """
        textbox(root, message, 47, height - 115, 486)

    def button_pressed(button_number):
        """
         Called when button is pressed. Destroys subjects and the semester with the number of the button
         
         @param button_number - number of the button
        """
        root.destroy()
        subjects(dept_name, branch_name, f"Semester {button_number}")

    def create_sem(i, m):
        """
         Create semester and its contents permanently. This is a callback for when user wants to create a new semester.
         
         @param i - index of the new semester in the list
         @param m - name of the new semester to be created
        """
        def handle_del():
            """
             Delete semester and its contents permanently. This is a callback function for the delete_semester command
            """
            confirmation = (
                f"Do you want to delete Semester {m} and its contents permanently?"
            )
            response = messagebox.askyesno(
                "Confirmation", confirmation, default=messagebox.NO
            )
            # Delete the semester from the database.
            if response:
                semester_to_delete = f"Semester {m}"

                root_ref = db.reference("/")

                # Delete all semesters and semesters in the database.
                if dept_name in root_ref.child("departments").get():
                    # Delete all semesters and semesters in the department.
                    if (
                        branch_name
                        in root_ref.child(f"departments/{dept_name}/branches").get()
                    ):
                        semesters = root_ref.child(
                            f"departments/{dept_name}/branches/{branch_name}/semesters"
                        ).get()
                        # Delete the semester from the list of semesters.
                        if semester_to_delete in semesters:
                            root_ref.child(
                                f"departments/{dept_name}/branches/{branch_name}/semesters"
                            ).child(semester_to_delete).delete()
                            show_text(f"Semester {m} has been deleted successfully.")
                            refresh_sem_list()
                        else:
                            print(
                                f"Semester '{semester_to_delete}' not found in '{branch_name}'"
                            )
                    else:
                        print(f"Branch '{branch_name}' not found in '{dept_name}'")
                else:
                    print(f"Department '{dept_name}' not found in the database.")

            else:
                show_text(f"Deletion cancelled.")

        if i % 2 == 0:
            color = "#{:02x}{:02x}{:02x}".format(
                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            )
            if is_dark_color(color):
                fg = "white"
            else:
                fg = "black"
            txt = tk.Button(
                table_frame_inside_canvas,
                text=f"Semester {i+1}",
                anchor="w",
                command=lambda num=i + 1: button_pressed(num),
                width=16,
                height=1,
                bg=color,
                fg=fg,
                bd=1,
                font=("Times New Roman", 15),
            )
            txt.grid(row=i // 2, column=0, padx=(50, 8), pady=10)
            if (i + 1 == m) and (i != 0):
                button = tk.Button(
                    table_frame_inside_canvas,
                    image=del_button_image,
                    bd=0,
                    highlightbackground="white",
                    bg="white",
                    highlightcolor="white",
                    command=handle_del,
                )
                button.config()
                button.grid(row=i // 2, column=1)
        else:
            color = "#{:02x}{:02x}{:02x}".format(
                random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            )
            if is_dark_color(color):
                fg = "white"
            else:
                fg = "black"
            txt = tk.Button(
                table_frame_inside_canvas,
                text=f"Semester {i+1}",
                command=lambda num=i + 1: button_pressed(num),
                anchor="w",
                width=16,
                height=1,
                bg=color,
                fg=fg,
                bd=1,
                font=("Times New Roman", 15),
            )
            txt.grid(row=i // 2, column=2, padx=(50, 8), pady=10)

            if (i + 1 == m) and (i != 0):
                button = tk.Button(
                    table_frame_inside_canvas,
                    image=del_button_image,
                    bd=0,
                    highlightbackground="white",
                    bg="white",
                    highlightcolor="white",
                    command=handle_del,
                )
                button.config()
                button.grid(row=i // 2, column=3)

        root.bind("<Delete>", lambda event: handle_del())

    del_button_image = tk.PhotoImage(file="delete.png")

    def check_sem():
        """
         Check semester in department branch and return number of semesters.
         
         
         @return number of semester in department branch and 0 if
        """
        root_ref = db.reference("/")
        semesters = root_ref.child(
            f"departments/{dept_name}/branches/{branch_name}/semesters"
        ).get()
        # Returns the number of semesters in the list.
        if semesters:
            num_semesters = len(semesters)
            return num_semesters
        return 0

    no_of_sem = check_sem()

    # Create a new semester if no_of_sem 0.
    if no_of_sem == 0:
        num_semesters = 4 if br_code == ("ME" or "MCA" or "MTech") else 8
        # Create a new sem for each sem
        for i in range(num_semesters):
            create_sem(i, num_semesters)
        semesters_dict = {
            f"Semester {i}": {"subjects": ""} for i in range(1, num_semesters + 1)
        }
        root_ref = db.reference("/")
        root_ref.update(
            {
                f"departments/{dept_name}/branches/{branch_name}/semesters": semesters_dict
            }
        )
    else:
        # Create a new sem for each of the no_of_sem.
        for i in range(no_of_sem):
            create_sem(i, no_of_sem)

    def handle_add():
        """
         Add semester to database if it doesn't exist. Args : None
        """
        semester_name = f"Semester {check_sem()+1}"
        root_ref = db.reference("/")
        semesters = root_ref.child(
            f"departments/{dept_name}/branches/{branch_name}/semesters"
        ).get()
        # Add a new semester to the list of semesters
        if semester_name not in semesters:
            root_ref.update(
                {
                    f"departments/{dept_name}/branches/{branch_name}/semesters/{semester_name}": ""
                }
            )
            show_text(f"{semester_name} added successfully.")
            refresh_sem_list()

    def on_canvas_configure(event):
        """
         Called when the canvas is configured. This is a callback function and should be used to configure the canvas to fit the contents of the view.
         
         @param event - The event that triggered this function call. It is passed as an argument
        """
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_canvas_configure)

    def handle_scroll(event):
        """
         Scroll the canvas vertically. This is called when the user scrolls a view.
         
         @param event - The event that triggered this function call. It's passed to the event handler
        """
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    canvas.bind_all("<MouseWheel>", handle_scroll)

    def handle_back():
        """
         Delete branch and all sub - branches. This is called when the user presses back
        """
        root.destroy()
        branches(dept_name)

    back_button_image = tk.PhotoImage(file="back.png")
    create_back_button(root, handle_back, 7, 110, back_button_image)

    style = ttk.Style()
    style.configure("Rounded.TButton", borderwidth=0, relief="flat", background="white")

    plus_button_image = tk.PhotoImage(file="pluss.png")
    plus_button = ttk.Button(
        root, image=plus_button_image, style="Rounded.TButton", command=handle_add
    )
    plus_button.place(x=width - 70, y=height - 66)

    def refresh_sem_list():
        """
         Refresh semesters list and store in root_ref. Args : None
        """
        # Destroy all widgets inside canvas.
        for widget in table_frame_inside_canvas.winfo_children():
            widget.destroy()
        no_of_sem = check_sem()

        # Create a new semester if no_of_sem 0.
        if no_of_sem == 0:
            num_semesters = 4 if br_code == "ME" else 8
            # Create a new sem for each sem
            for i in range(num_semesters):
                create_sem(i, num_semesters)
            semesters_dict = {f"Semester {i}": "" for i in range(1, num_semesters + 1)}
            root_ref.update(
                {
                    f"departments/{dept_name}/branches/{branch_name}/semesters": semesters_dict
                }
            )
        else:
            # Create a new sem for each of the no_of_sem.
            for i in range(no_of_sem):
                create_sem(i, no_of_sem)

        # Create a new sem for each of the no_of_sem.
        for i in range(no_of_sem):
            create_sem(i, no_of_sem)

        frame = tk.Frame(root, width=width, height=50, bg="white", borderwidth=0)
        frame.place(x=0, y=470)

    refresh_button_image = tk.PhotoImage(file="refresh.png")
    refresh_button = ttk.Button(
        root,
        image=refresh_button_image,
        style="Rounded.TButton",
        command=refresh_sem_list,
    )
    refresh_button.place(x=width - 140, y=height - 66)

    root.lift()
    root.mainloop()


# ============================================================================================
# ============================================================================================


def subjects(dept_name, branch_name, sem_name):
    """
     Display a dialog to select subjects. It is possible to select a subject by branch name or by department code
     
     @param dept_name - name of departure or branch
     @param branch_name - branch name or branch code - name
     @param sem_name - semitranspritic name of
    """
    root = tk.Tk()
    root.title("Select Subjects")
    root.overrideredirect(True)
    width = 580
    height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg="white")

    def button_pressed(button_number, action):
        """
         Called when a button is pressed. This is a callback function to be registered with : func : ` button_pressed `
         
         @param button_number - The index of the button that was pressed
         @param action - The action that was pressed ( edit or delete
        """
        # Edit or edit section. If action is Edit then edit section.
        if action == "Edit":
            edit_section(subject_names[button_number], button_number)
        else:
            pass

    try:
        br_code, br_name = branch_name.split(" - ")
    except:
        br_code, br_name = branch_name, ""

    subject_names = []
    root_ref = db.reference("/")
    subject_ref = root_ref.child(
        f"departments/{dept_name}/branches/{branch_name}/semesters/{sem_name}/subjects"
    )

    try:
        student_ref = db.reference(
            f"/departments/{dept_name}/branches/{branch_name}/semesters/{sem_name}/students"
        )
        students = student_ref.get()
        student_count = len(students)
    except:
        student_count = 0

    try:
        # Update subject_ref with student count if students are 0.
        for subject, stud_count in subject_ref.get().items():
            # Update subject_ref. update subject_ref if students count is 0
            if (not isinstance(stud_count, int)) or (stud_count == 0):
                subject_ref.update({subject: student_count})
    except:
        pass

    # Add subjects to subject_names list
    for subject in subject_ref.get():
        subject_names.append(subject)

    logo_img = tk.PhotoImage(file="logo.png")
    logo_img = logo_img.subsample(1)
    create_logo(root, width, height, logo_img)
    exit_button(root, width, height)

    lbl = tk.Label(
        root,
        text="SUBJECTS:",
        width=21,
        anchor="w",
        height=1,
        fg="black",
        bg="white",
        font=("Sitka Text Semibold", 15, " bold "),
    )
    lbl.place(x=125 - 75, y=155 - 20)

    def handle_navigation(text):
        """
         Handle navigation to the tree. This is called when the user navigates to one of the buttons
         
         @param text - The text that was
        """
        # Destroy the tree and all branches
        if text == "Dept":
            root.destroy()
            branches(dept_name)
        # Destroy the root node if text is Branch
        if text == "Branch":
            root.destroy()
            semester(dept_name, branch_name)

    dept_button = ttk.Button(
        root,
        text=dept_name,
        style="Rounded.TButton",
        command=lambda: handle_navigation("Dept"),
    )
    dept_button.place(x=125 - 75, y=130 - 20)
    dept_button.update()

    branch_button = ttk.Button(
        root,
        text=f"{branch_name}",
        style="Rounded.TButton",
        command=lambda: handle_navigation("Branch"),
    )
    branch_button.place(x=125 - 75 + dept_button.winfo_width(), y=130 - 20)
    branch_button.update()

    sem_button = ttk.Button(root, text=f"{sem_name}", style="Rounded.TButton")
    sem_button.place(
        x=125 - 75 + dept_button.winfo_width() + branch_button.winfo_width(), y=130 - 20
    )

    table_frame = tk.Frame(root, bg="white")
    scroll_height = 300
    table_frame.place(x=0, y=190 - 20, width=width, height=scroll_height)
    canvas = tk.Canvas(table_frame, bg="white")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    table_frame_inside_canvas = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=table_frame_inside_canvas, anchor="nw")

    def show_text(message):
        """
         Display a text box. This is a convenience function to call : func : ` pyglet. display. textbox `
         
         @param message - The message to display
        """
        textbox(root, message, 47, height - 165, 486)

    button_image = tk.PhotoImage(file="edit.png")

    i = 0
    # Add a button to the table.
    if len(subject_names) == 0:
        color, fg = pick_color()
        txt = tk.Button(
            table_frame_inside_canvas,
            text=f"No subject added.",
            anchor="w",
            width=40,
            height=1,
            bg=color,
            fg=fg,
            bd=1,
            font=("Times New Roman", 15),
        )
        txt.grid(row=0, column=0, padx=(50, 8), pady=10)
    # Generates a tk. Button with the subject names.
    for subject in subject_names:
        color, fg = pick_color()
        txt = tk.Button(
            table_frame_inside_canvas,
            text=f"{subject}",
            anchor="w",
            width=46,
            height=1,
            bg=color,
            fg=fg,
            bd=1,
            font=("Times New Roman", 12),
        )
        txt.grid(row=i, column=0, padx=(50, 8), pady=5)
        button = tk.Button(
            table_frame_inside_canvas,
            image=button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
        )
        button.config(command=lambda num=i: button_pressed(num, "Edit"))
        button.grid(row=i, column=1)
        i += 1

    def on_canvas_configure(event):
        """
         Called when the canvas is configured. This is a callback function and should be used to configure the canvas to fit the contents of the view.
         
         @param event - The event that triggered this function call. It is passed as an argument
        """
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_canvas_configure)

    def handle_scroll(event):
        """
         Scroll the canvas vertically. This is called when the user scrolls a view.
         
         @param event - The event that triggered this function call. It's passed to the event handler
        """
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    canvas.bind_all("<MouseWheel>", handle_scroll)

    tick_button_image = tk.PhotoImage(file="tick.png")
    delete_button_image = tk.PhotoImage(file="delete.png")

    def edit_section(subject, num):
        """
         Edit section in Tkinter. This is a function to edit a section
         
         @param subject - The name of the subject
         @param num - The number of the section to edit ( 0 -
        """
        frame = tk.Frame(root, width=width, height=100, bg="white", borderwidth=0)
        frame.place(x=0, y=470)
        lbl = tk.Label(
            root,
            text="Enter Subject Name:",
            width=53,
            anchor="w",
            height=1,
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        lbl.place(x=45, y=height - 226)
        txt = tk.Entry(
            root, width=42, bg="blue", fg="white", font=("Times New Roman", 15)
        )
        txt.insert(0, subject)
        txt.place(x=47, y=height - 200)

        def handle_edit():
            """
             Edits subject in database and returns True if subject is new. Otherwise returns
            """
            new_subject_name = txt.get()
            # This function will confirm that the subject name is different from the new name.
            if new_subject_name != subject:
                confirmation = f"Old Name: {subject}\nNew Name: {new_subject_name}\n\nDo you want to proceed?"
                response = messagebox.askyesno(
                    "Confirmation", confirmation, default=messagebox.NO
                )
                # if subject_names. get subject_names. get subject_name. lower
                if response:
                    # This function will remove the subject from the subject_names list and update the subject list.
                    if new_subject_name.lower() not in (
                        name.lower() for name in subject_names
                    ):
                        root_ref = db.reference("/")
                        subject_ref = root_ref.child(
                            f"departments/{dept_name}/branches/{branch_name}/semesters/{sem_name}/subjects"
                        )
                        # This function will delete the subject from the subject_ref and set the subject to the old one.
                        if subject in subject_ref.get():
                            old_subject_data = root_ref.child(
                                f"departments/{dept_name}/branches/{branch_name}/semesters/{sem_name}/subjects/{subject}"
                            ).get()
                            root_ref.child(
                                f"departments/{dept_name}/branches/{branch_name}/semesters/{sem_name}/subjects/{subject}"
                            ).delete()
                            root_ref.child(
                                f"departments/{dept_name}/branches/{branch_name}/semesters/{sem_name}/subjects/{new_subject_name}"
                            ).set(old_subject_data)
                        else:
                            print(f"Subject '{subject}' not found in the database.")
                        subject_names[num] = new_subject_name
                        show_text("Subject Name Edited Successfully.")
                        refresh_subject_list()
                    else:
                        show_text("Subject with the new name already exists.")
                else:
                    show_text("No changes made.")
            else:
                show_text("No changes made.")

        def handle_delete():
            """
             Delete subject from database and refresh subject list if successfull. This function is called when user presses delete button
            """
            confirmation = f"Subject Name: {subject}\n\nDo you want to delete?"
            response = messagebox.askyesno(
                "Confirmation", confirmation, default=messagebox.NO
            )
            # delete subject from the subject list
            if response:
                root_ref = db.reference(
                    f"departments/{dept_name}/branches/{branch_name}/semesters/{sem_name}/subjects"
                )
                # Delete the subject from the subject list.
                if subject in root_ref.get():
                    subject_ref = root_ref.child(subject)
                    subject_ref.delete()
                    show_text("Subject deleted successfully.")
                    refresh_subject_list()
                else:
                    show_text("Subject not found in the database.")
            else:
                show_text("No changes made.")

        tick_button = tk.Button(
            root,
            image=tick_button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
            command=handle_edit,
        )
        tick_button.place(x=480, y=height - 200)
        root.bind("<Return>", lambda event: handle_edit())

        delete_button = tk.Button(
            root,
            image=delete_button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
            command=handle_delete,
        )
        delete_button.place(x=513, y=height - 200)
        root.bind("<Delete>", lambda event: handle_delete())

    def add_section():
        """
         Add section to the subject list. This is used to add a new subject to the user's profile.
         
         
         @return A frame containing the subject name in a text field
        """
        frame = tk.Frame(root, width=width, height=100, bg="white", borderwidth=0)
        frame.place(x=0, y=470)
        lbl = tk.Label(
            root,
            text="Enter Subject Name:",
            width=53,
            anchor="w",
            height=1,
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        lbl.place(x=45, y=height - 226)
        txt = tk.Entry(
            root, width=42, bg="blue", fg="white", font=("Times New Roman", 15)
        )
        txt.place(x=47, y=height - 200)

        def handle_add():
            """
             Adds a new subject to the database. This is a function that handles the addition of new subjects and returns the new subject name
             
             
             @return A string containing the new subject
            """
            new_subject_name = txt.get()
            line = new_subject_name.strip()
            # This function takes a line of text and returns a new string that can be used to create a new subject name.
            if " - " in line:
                code, name = line.split(" - ", 1)
                new_subject_name = f"{code.strip()} - {name.strip()}"
            elif "- " in line:
                code, name = line.split("- ", 1)
                new_subject_name = f"{code.strip()} - {name.strip()}"
            elif "-" in line:
                code, name = line.split("-", 1)
                new_subject_name = f"{code.strip()} - {name.strip()}"
            elif " " in line:
                code, name = line.split(" ", 1)
                new_subject_name = f"{code.strip()} - {name.strip()}"
            elif line:
                code, name = "NULL", line
                new_subject_name = f"{code.strip()} - {name.strip()}"
            # Confirm the user has to add a new subject.
            if new_subject_name.strip() != "" and new_subject_name.lower() not in (
                name.lower() for name in subject_names
            ):
                confirmation = f"Name: {new_subject_name}\n\nDo you want to add?"
                response = messagebox.askyesno(
                    "Confirmation", confirmation, default=messagebox.NO
                )
            elif new_subject_name.lower() in (name.lower() for name in subject_names):
                show_text("Subject already exists.")
            else:
                show_text("Not a valid Subject Name.")
                return
            # if response is True show subject added successfully.
            if response:
                root_ref = db.reference(
                    f"departments/{dept_name}/branches/{branch_name}/semesters/{sem_name}/subjects"
                )
                # This method is used to get the count of students in the student s list of students.
                if new_subject_name not in root_ref.get():
                    try:
                        student_ref = db.reference(
                            f"/departments/{dept_name}/branches/{branch_name}/semesters/{sem_name}/students"
                        )
                        students = student_ref.get()
                        student_count = len(students)
                    except:
                        student_count = 0
                    root_ref.child(new_subject_name).set(student_count)
                show_text("Subject Added Successfully.")
                refresh_subject_list()
            else:
                show_text("No changes made")

        tick_button = tk.Button(
            root,
            image=tick_button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
            command=handle_add,
        )
        tick_button.place(x=480, y=height - 200)
        root.bind("<Return>", lambda event: handle_add())

    def handle_back():
        """
         Delete semester on back of dept. This is called when user presses back
        """
        root.destroy()
        semester(dept_name, branch_name)

    back_button_image = tk.PhotoImage(file="back.png")
    create_back_button(root, handle_back, 7, 110, back_button_image)

    style = ttk.Style()
    style.configure("Rounded.TButton", borderwidth=0, relief="flat", background="white")

    plus_button_image = tk.PhotoImage(file="pluss.png")
    plus_button = ttk.Button(
        root, image=plus_button_image, style="Rounded.TButton", command=add_section
    )
    plus_button.place(x=width - 70, y=height - 66)

    def refresh_subject_list():
        for widget in table_frame_inside_canvas.winfo_children():
            widget.destroy()
        subject_names.clear()

        root_ref = db.reference(
            f"departments/{dept_name}/branches/{branch_name}/semesters/{sem_name}/subjects"
        )

        try:
            data = root_ref.get()
            if data:
                for subject in data:
                    subject_names.append(subject)
        except Exception as e:
            internet_connection()
            print("Error reading data from Firebase:", e)

        i = 0
        if len(subject_names) == 0:
            color, fg = pick_color()
            txt = tk.Button(
                table_frame_inside_canvas,
                text="No subjects present.",
                anchor="w",
                width=38,
                height=1,
                bg=color,
                fg=fg,
                bd=1,
                font=("Times New Roman", 15),
            )
            txt.grid(row=i, column=0, padx=(50, 8), pady=5)

        # Generates a tk. Button for each subject in subject_names.
        for subject in subject_names:
            color, fg = pick_color()
            txt = tk.Button(
                table_frame_inside_canvas,
                text=f" {subject}",
                command=lambda num=i: button_pressed(num, "Subject"),
                anchor="w",
                width=46,
                height=1,
                bg=color,
                fg=fg,
                bd=1,
                font=("Times New Roman", 12),
            )
            txt.grid(row=i, column=0, padx=(50, 8), pady=5)

            button = tk.Button(
                table_frame_inside_canvas,
                image=button_image,
                bd=0,
                highlightbackground="white",
                bg="white",
                highlightcolor="white",
            )
            button.config(command=lambda num=i: button_pressed(num, "Edit"))
            button.grid(row=i, column=1)
            i += 1
        frame = tk.Frame(root, width=width, height=100, bg="white", borderwidth=0)
        frame.place(x=0, y=470)

        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def add_many_return(x, y):
        """
         Add many subjects to subject list. This function is used for adding many subjects to subject list
         
         @param x - index of subject to add
         @param y - index of subject to add ( 0 = all
        """
        # Show a text message if all subjects already exist.
        if y == 0:
            show_text(f"{x} subject(s) added.")
        elif x == 0:
            show_text(f"All subject(s) already exist.")
        else:
            show_text(f"{x} subject(s) added and {y} subject(s) already exist.")
        refresh_subject_list()

    def add_many_dept():
        """
         Add subjects to the Firebase Realtime Database. This is a list of department names that can be added to the branch and semester
         
         
         @return A Deferred that fires when the user clicks the add button
        """
        def handle_many_add(text):
            """
             Add a subject to Firebase Realtime Database. This is a batch add operation that will be executed in a single thread
             
             @param text - The subject's
            """
            new_subject_name = text

            # Add the subject to the Firebase Realtime Database
            root_ref = db.reference(
                f"departments/{dept_name}/branches/{branch_name}/semesters/{sem_name}/subjects"
            )
            try:
                student_ref = db.reference(
                    f"/departments/{dept_name}/branches/{branch_name}/semesters/{sem_name}/students"
                )
                students = student_ref.get()
                student_count = len(students)
            except:
                student_count = 0
            root_ref.child(new_subject_name).set(student_count)

            # Refresh the subject names from the database
            subject_names.clear()
            data = root_ref.get()
            # Add subject names to subject names.
            if data:
                subject_names.extend(list(data.keys()))

        def get_subjects():
            """
             Get subjects from the text widget and return them as a list of strings.
             
             
             @return List of subject codes and names in ISO 639
            """
            # Read text from the input widget
            subjects_input = text_input.get("1.0", "end-1c")

            # Split the input into lines and process each line
            subjects = []
            # This function will parse the subjects_input and add subjects to the subjects list.
            for line in subjects_input.split("\n"):
                line = line.strip()  # Remove leading and trailing whitespace

                # Check if there is a space and a valid subject name
                # Add a subject to the list of subjects.
                if " " in line:
                    code, name = line.split(" ", 1)
                    subject = f"{code.strip()} - {name.strip()}"
                    subjects.append(subject)
                elif " - " in line:
                    code, name = line.split(" - ", 1)
                    subject = f"{code.strip()} - {name.strip()}"
                    subjects.append(subject)
                elif "- " in line:
                    code, name = line.split("- ", 1)
                    subject = f"{code.strip()} - {name.strip()}"
                    subjects.append(subject)
                elif "-" in line:
                    code, name = line.split("-", 1)
                    subject = f"{code.strip()} - {name.strip()}"
                    subjects.append(subject)
                elif (
                    line
                ):  # If no space or dash found, assume it's the subject name itself
                    subjects.append(line)

            # Show the subjects text.
            if not subjects:
                show_text("No subjects entered.")
                return

            # Count the number of departments entered
            num_subjects = len(subjects)

            confirmation = f"Do you want to submit {num_subjects} subject(s)?\n\nCheck once before submitting."
            response = messagebox.askyesno(
                "Confirmation", confirmation, default=messagebox.NO
            )

            # Handle the response of the request.
            if response:
                added_count = 0
                existing_count = 0

                # Add subjects to the list of subjects.
                for subject in subjects:
                    # Add a new subject to the list of subjects.
                    if subject.lower() in (name.lower() for name in subject_names):
                        existing_count += 1
                    else:
                        handle_many_add(subject)
                        added_count += 1

                show_text("Done..Closing in 3..2..1")
                root1.destroy()
                add_many_return(added_count, existing_count)

            else:
                show_text("No subjects entered.")

        def show_text(message):
            """
             Show text in output box. This is a convenience function for insert_text_with_typing_animation
             
             @param message - Text to be displayed
            """
            insert_text_with_typing_animation(output_box, message)

        root1 = tk.Tk()
        root1.title("Enter Subjects")
        root1.wm_attributes("-topmost", 1)

        # Create and pack a label with instructions
        instructions = tk.Label(
            root1,
            text="Enter subjects separated by line breaks:\nEx. UTA017 COMPUTER or UTA017 - COMPUTER",
            font=("Times New Roman", 12),
        )
        instructions.pack(pady=5)

        text_input = tk.Text(root1, width=60, height=10, font=("Times New Roman", 12))
        text_input.pack(padx=20)

        output_box = tk.Text(
            root1,
            width=60,
            height=1,
            bg="grey",
            fg="white",
            font=("Times New Roman", 12),
            wrap="word",
            state="disabled",
        )
        output_box.pack(padx=20, pady=10)
        output_box.config(state=tk.NORMAL)
        output_box.delete("1.0", tk.END)
        output_box.config(state=tk.DISABLED)

        submit_button = ttk.Button(
            root1, text="Submit", style="Rounded.TButton", command=get_subjects
        )
        submit_button.pack(pady=10)

        root1.mainloop()

    edit_button = ttk.Button(
        root, text="ADD MANY SUBJECT", style="Rounded.TButton", command=add_many_dept
    )
    edit_button.place(x=290, y=height - 115, width=215, height=35)

    def add_stud():
        """
         Add student to StudentSS. This is a wrapper for studentss
        """
        root.destroy()
        studentss(dept_name, branch_name, sem_name)

    # Add an exit button in the bottom left corner
    add_stud_button = ttk.Button(
        root, text="ADD STUDENT LIST", style="Rounded.TButton", command=add_stud
    )
    add_stud_button.place(x=125 - 75, y=height - 115, width=215, height=35)

    refresh_button_image = tk.PhotoImage(file="refresh.png")
    refresh_button = ttk.Button(
        root,
        image=refresh_button_image,
        style="Rounded.TButton",
        command=refresh_subject_list,
    )
    refresh_button.place(x=width - 140, y=height - 66)
    root.mainloop()


# ============================================================================================
# ============================================================================================


def studentss(dept_name, branch_name, sem_name):
    """
     Upload Students to Solaris. It is used to upload student list and semantically all students in a branch
     
     @param dept_name - Name of the department where the student list is stored
     @param branch_name - Branch name to be uploaded. If branch does not exist it will be created
     @param sem_name - Semantically unique name of the
    """
    root = tk.Tk()
    root.title("Upload Students")
    root.overrideredirect(True)

    width = 580
    height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))

    root.geometry(f"{width}x{height}+{x}+{y}")

    root.configure(bg="white")

    try:
        br_code, br_name = branch_name.split(" - ")
    except:
        br_code, br_name = branch_name, ""

    logo_img = tk.PhotoImage(file="logo.png")
    logo_img = logo_img.subsample(1)

    create_logo(root, width, height, logo_img)
    exit_button(root, width, height)

    lbl = tk.Label(
        root,
        text="STUDENT LIST:",
        width=21,
        anchor="w",
        height=1,
        fg="black",
        bg="white",
        font=("Sitka Text Semibold", 15, " bold "),
    )
    lbl.place(x=125 - 75, y=155 - 20)

    def handle_navigation(text):
        """
         Handle navigation to the tree. This is called when the user navigates to a page that has been created by : func : ` create_navigation `
         
         @param text - The text of the
        """
        # Destroy the tree and all branches
        if text == "Dept":
            root.destroy()
            branches(dept_name)
        # Destroy the root node if text is Branch
        if text == "Branch":
            root.destroy()
            semester(dept_name, branch_name)
        # Destroys the root node and all subjects.
        if text == "Sem":
            root.destroy()
            subjects(dept_name, branch_name, sem_name)

    dept_button = ttk.Button(
        root,
        text=dept_name,
        style="Rounded.TButton",
        command=lambda: handle_navigation("Dept"),
    )
    dept_button.place(x=125 - 75, y=130 - 20)

    dept_button.update()
    branch_button = ttk.Button(
        root,
        text=f"{br_code} - {br_name}",
        style="Rounded.TButton",
        command=lambda: handle_navigation("Branch"),
    )
    branch_button.place(x=125 - 75 + dept_button.winfo_width(), y=130 - 20)

    branch_button.update()
    sem_button = ttk.Button(
        root,
        text=f"{sem_name}",
        style="Rounded.TButton",
        command=lambda: handle_navigation("Sem"),
    )
    sem_button.place(
        x=125 - 75 + dept_button.winfo_width() + branch_button.winfo_width(), y=130 - 20
    )

    sem_button.update()

    def show_text(message):
        """
         Display a text box. This is a convenience function to call : func : ` pyglet. display. textbox `
         
         @param message - The message to display
        """
        textbox(root, message, 47, height - 115, 486)

    def add_student_lists():
        """
         Add students to the Student list. This is done by reading the file from the user
        """
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        # Add students to the list of students in the file.
        if file_path:
            df = pd.read_excel(file_path)
            # Add students to the list of students in the dataframe.
            if "Roll No." in df.columns and "Name" in df.columns:
                show_text(f"Adding students. It may take a while.")
                students_ref = db.reference(
                    f"departments/{dept_name}/branches/{branch_name}/semesters/{sem_name}/students"
                )
                students_ref.delete()
                students = df[["Roll No.", "Name"]].to_dict(orient="records")

                def add_students_thread(student_chunk):
                    """
                     Add students to the database. This is a thread and should be called in a while
                     
                     @param student_chunk - list of dicts each with a roll
                    """
                    students_ref = db.reference(
                        f"departments/{dept_name}/branches/{branch_name}/semesters/{sem_name}/students"
                    )
                    # Set the student s roll no to the student s name.
                    for student in student_chunk:
                        roll_no = str(student.get("Roll No."))
                        name = student.get("Name")
                        # Set the student record s name
                        if roll_no and name:
                            students_ref.child(roll_no).set(name)
                        else:
                            print(
                                f"Skipping invalid student record: Roll No = {roll_no}, Name = {name}"
                            )

                chunk_size = 10
                chunks = [
                    students[i : i + chunk_size]
                    for i in range(0, len(students), chunk_size)
                ]

                threads = []
                # Add students threads to the list of threads.
                for chunk in chunks:
                    thread = threading.Thread(target=add_students_thread, args=(chunk,))
                    thread.start()
                    threads.append(thread)

                # join all threads in the list
                for thread in threads:
                    thread.join()

                show_text(f"Student list has been added.")
            else:
                show_text(
                    "The Excel file does not have the expected columns (Roll No. and Name)."
                )

    color, fg = pick_color()

    add_student_button = tk.Button(
        root,
        text="ADD STUDENT LISTS",
        command=add_student_lists,
        anchor="center",
        width=43,
        height=2,
        bg=color,
        fg=fg,
        bd=1,
        font=("Times New Roman", 15),
    )
    add_student_button.place(x=47, y=190)

    def handle_back():
        """
         Delete subjects on back of department. This is called when the user clicks the back button
        """
        root.destroy()
        subjects(dept_name, branch_name, sem_name)

    back_button_image = tk.PhotoImage(file="back.png")
    create_back_button(root, handle_back, 7, 110, back_button_image)

    style = ttk.Style()
    style.configure("Rounded.TButton", borderwidth=0, relief="flat", background="white")

    root.mainloop()


# ============================================================================================
# ============================================================================================

departments = []


def dates(tried_earlier):
    """
     Edit dates from Firebase. It is called when you click on the date button
     
     @param tried_earlier - True if you tried to edit dates earlier than
    """
    # Get the data from Firebase
    if tried_earlier:
        try:
            root_ref = db.reference("/dates")
            data = root_ref.get()
            keys = list(data.keys())
            # Add days to the names of the days in the data.
            if data:
                # Add days to the list of days names
                for days in keys:
                    days_names.append(days)
        except Exception as e:
            print("Error reading data from Firebase:", e)

    root = tk.Tk()
    root.title("Edit Dates")
    root.overrideredirect(True)
    width = 580
    height = 650
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")
    x_cord = 75
    y_cord = 20
    root.configure(bg="white")
    logo_img = tk.PhotoImage(file="logo.png")
    logo_img = logo_img.subsample(1)
    create_logo(root, width, height, logo_img)
    exit_button(root, width, height)
    lbl = tk.Label(
        root,
        text="EDIT DATES:",
        width=21,
        anchor="w",
        height=1,
        fg="black",
        bg="white",
        font=("Sitka Text Semibold", 15, " bold "),
    )
    lbl.place(x=125 - x_cord, y=130 - y_cord)
    table_frame = tk.Frame(root, bg="white")
    scroll_height = 320
    table_frame.place(x=0, y=170 - y_cord, width=width, height=scroll_height)
    canvas = tk.Canvas(table_frame, bg="white")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    table_frame_inside_canvas = tk.Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=table_frame_inside_canvas, anchor="nw")

    def show_text(message):
        """
         Display a text box. This is a convenience function to call : func : ` pyglet. display. textbox `
         
         @param message - The message to display
        """
        textbox(root, message, 47, height - 115, 460)

    def button_pressed(button_number, button_type):
        """
         Called when a button is pressed. This is a function to be implemented by subclasses
         
         @param button_number - the number of the button that was pressed
         @param button_type - the type of the button ( Edit etc
        """
        # Edit or edit section. If button_type is Edit then edit section is shown in the edit section.
        if button_type == "Edit":
            edit_section(days_names[button_number], button_number)

    button_image = tk.PhotoImage(file="edit.png")
    i = 0

    # Generates a tk. Button object with the days names.
    for days in days_names:
        # Generates a tk. Button object for the i th button.
        if i % 2 == 0:
            color, fg = pick_color()
            txt = tk.Button(
                table_frame_inside_canvas,
                text=f"{days}",
                anchor="w",
                command=lambda num=i + 1: button_pressed(num),
                width=16,
                height=1,
                bg=color,
                fg=fg,
                bd=1,
                font=("Times New Roman", 15),
            )
            txt.grid(row=i // 2, column=0, padx=(50, 8), pady=10)
            button = tk.Button(
                table_frame_inside_canvas,
                image=button_image,
                bd=0,
                highlightbackground="white",
                bg="white",
                highlightcolor="white",
            )
            button.config(command=lambda num=i: button_pressed(num, "Edit"))
            button.grid(row=i // 2, column=1)
        else:
            color, fg = pick_color()
            txt = tk.Button(
                table_frame_inside_canvas,
                text=f"{days}",
                command=lambda num=i + 1: button_pressed(num),
                anchor="w",
                width=16,
                height=1,
                bg=color,
                fg=fg,
                bd=1,
                font=("Times New Roman", 15),
            )
            txt.grid(row=i // 2, column=2, padx=(50, 8), pady=10)
            button = tk.Button(
                table_frame_inside_canvas,
                image=button_image,
                bd=0,
                highlightbackground="white",
                bg="white",
                highlightcolor="white",
            )
            button.config(command=lambda num=i: button_pressed(num, "Edit"))
            button.grid(row=i // 2, column=3)
        i += 1

    def on_canvas_configure(event):
        """
         Called when the canvas is configured. This is a callback function and should be used to configure the canvas to fit the contents of the view.
         
         @param event - The event that triggered this function call. It is passed as an argument
        """
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_canvas_configure)

    def handle_scroll(event):
        """
         Scroll the canvas vertically. This is called when the user scrolls a view.
         
         @param event - The event that triggered this function call. It's passed to the event handler
        """
        canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")

    canvas.bind_all("<MouseWheel>", handle_scroll)

    tick_button_image = tk.PhotoImage(file="tick.png")

    def edit_section(days, num):
        """
         Display a Tkinter frame to edit a section. It is used in the Sitka editor and for the day and year of the day.
         
         @param days - Number of days in the section. This should be a positive integer.
         @param num - Number of days in the section. This should be a positive integer.
         
         @return A Tkinter frame containing the day and year
        """
        frame = tk.Frame(root, width=width, height=100, bg="white", borderwidth=0)
        frame.place(x=0, y=470)
        lbl = tk.Label(
            root,
            text="(DD/MM/YYYY):",
            anchor="w",
            height=1,
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        lbl.place(x=45, y=height - 176, width=180)
        dd = tk.Entry(root, bg="blue", fg="white", font=("Times New Roman", 15))
        dd.place(x=47, y=height - 150, width=30)
        hyf = tk.Label(
            root,
            text="-",
            anchor="w",
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        hyf.place(x=63 + 15, y=height - 154, width=10)
        mm = tk.Entry(root, bg="blue", fg="white", font=("Times New Roman", 15))
        mm.place(x=74 + 15, y=height - 150, width=30)
        hyf = tk.Label(
            root,
            text="-",
            anchor="w",
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        hyf.place(x=90 + 30, y=height - 154, width=10)
        yyyy = tk.Entry(root, bg="blue", fg="white", font=("Times New Roman", 15))
        yyyy.place(x=101 + 30, y=height - 150, width=60)
        lbl1 = tk.Label(
            root,
            text="(HH:MM)",
            anchor="w",
            height=1,
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        lbl1.place(x=150 + 60, y=height - 176, width=90)
        hh = tk.Entry(root, bg="blue", fg="white", font=("Times New Roman", 15))
        hh.place(x=155 + 60, y=height - 150, width=30)
        col = tk.Label(
            root,
            text=":",
            anchor="w",
            fg="black",
            bg="white",
            font=("Sitka Text Semibold", 12, "bold"),
        )
        col.place(x=186 + 60, y=height - 154, width=10)
        m = tk.Entry(root, bg="blue", fg="white", font=("Times New Roman", 15))
        m.place(x=197 + 60, y=height - 150, width=30)

        def handle_edit():
            """
             Edit the date and time. This will update the database to reflect the changes
             
             
             @return True if everything went
            """
            # Check the date and time.
            if not (
                1 <= int(dd.get()) <= 31
                and 1 <= int(mm.get()) <= 12
                and 2023 <= int(yyyy.get()) <= 2099
                and 0 <= int(hh.get()) <= 23
                and 0 <= int(m.get()) <= 59
            ):
                show_text("Invalid input! Please check the date and time.")
                return
            new_day_name = f"{dd.get().zfill(2)}-{mm.get().zfill(2)}-{yyyy.get()} {hh.get().zfill(2)}:{m.get().zfill(2)}"
            root_ref = db.reference("/dates")
            # Delete the days from the root_ref.
            if days in root_ref.get():
                old_day_data = root_ref.child(days).get()
                root_ref.child(days).delete()
                root_ref.update({new_day_name: old_day_data})
            days_names[num] = new_day_name
            show_text("Date Edited Successfully.")
            refresh()

        tick_button = tk.Button(
            root,
            image=tick_button_image,
            bd=0,
            highlightbackground="white",
            bg="white",
            highlightcolor="white",
        )
        tick_button.place(x=295, y=height - 150)
        root.bind("<Return>", lambda event: handle_edit())

    def refresh():
        """
         Refresh the table and display the days in the table. Called every time the user changes
        """
        frame = tk.Frame(root, width=width, height=100, bg="white", borderwidth=0)
        frame.place(x=0, y=470)
        global days_names
        try:
            root_ref = db.reference("/dates")
            data = root_ref.get()
            keys = list(data.keys())
            days_names = keys
            # This function will create the table_frame_inside_canvas. winfo_children widget. destroy
            if data:
                # Destroy all widgets inside canvas.
                for widget in table_frame_inside_canvas.winfo_children():
                    widget.destroy()
                i = 0
                # Generates a tk. Button object with the days names.
                for days in days_names:
                    # Generates a tk. Button object for the i th button.
                    if i % 2 == 0:
                        color, fg = pick_color()
                        txt = tk.Button(
                            table_frame_inside_canvas,
                            text=f"{days}",
                            anchor="w",
                            command=lambda num=i + 1: button_pressed(num),
                            width=16,
                            height=1,
                            bg=color,
                            fg=fg,
                            bd=1,
                            font=("Times New Roman", 15),
                        )
                        txt.grid(row=i // 2, column=0, padx=(50, 8), pady=10)
                        button = tk.Button(
                            table_frame_inside_canvas,
                            image=button_image,
                            bd=0,
                            highlightbackground="white",
                            bg="white",
                            highlightcolor="white",
                        )
                        button.config(command=lambda num=i: button_pressed(num, "Edit"))
                        button.grid(row=i // 2, column=1)
                    else:
                        color, fg = pick_color()
                        txt = tk.Button(
                            table_frame_inside_canvas,
                            text=f"{days}",
                            command=lambda num=i + 1: button_pressed(num),
                            anchor="w",
                            width=16,
                            height=1,
                            bg=color,
                            fg=fg,
                            bd=1,
                            font=("Times New Roman", 15),
                        )
                        txt.grid(row=i // 2, column=2, padx=(50, 8), pady=10)
                        button = tk.Button(
                            table_frame_inside_canvas,
                            image=button_image,
                            bd=0,
                            highlightbackground="white",
                            bg="white",
                            highlightcolor="white",
                        )
                        button.config(command=lambda num=i: button_pressed(num, "Edit"))
                        button.grid(row=i // 2, column=3)
                    i += 1
        except Exception as e:
            print("Error refreshing data from Firebase in refresh:", e)

    def handle_back():
        """
         Called when the user presses back. Destroys the window and calls two
        """
        root.destroy()
        two()

    back_button_image = tk.PhotoImage(file="back.png")
    back_button = ttk.Button(
        root, image=back_button_image, style="Rounded.TButton", command=handle_back
    )
    back_button.place(x=82 - x_cord, y=130 - y_cord)
    style = ttk.Style()
    style.configure("Rounded.TButton", borderwidth=0, relief="flat", background="white")
    refresh_button_image = tk.PhotoImage(file="refresh.png")
    refresh_button = ttk.Button(
        root, image=refresh_button_image, style="Rounded.TButton", command=refresh
    )
    refresh_button.place(x=width - 80, y=height - 66)

    publish_button = tk.Button(
        root,
        text="PUBLISH DATESHEET",
        width=20,
        height=1,
        bg=color,
        fg=fg,
        font=("Sitka Text Semibold", 15, "bold"),
        command=lambda: root.destroy() or publish(tried_earlier),
    )
    publish_button.place(x=width - 350, y=height - 65)

    root.mainloop()


# ============================================================================================
# ============================================================================================



def get_departments_and_branches():
    root_ref = db.reference("/")
    departments_ref = root_ref.child("departments")
    departments = []

    # Add all the departments to the list of departments
    data = departments_ref.get()
    if data:
        departments = list(data.keys())

    return departments

def get_subjects_and_students(department, branch, semester):
    ref = db.reference(f"/departments/{department}/branches/{branch}/semesters/{semester}")
    try:
        subjects = ref.child("subjects").get()
        return subjects
    except Exception as e:
        print(f"Error fetching data for {department},{branch},{semester}:{e}")
        return {}

def create_logo_pdf(pdf_canvas):
    logo_path = "logo.png"
    pdf_canvas.drawInlineImage(logo_path, 0, 730, width=178, height=94)

def create_header(pdf_canvas):
    pdf_canvas.drawString(200, 780, "THAPAR INSTITUTE OF ENGINEERING & TECHNOLOGY, PATIALA")
    pdf_canvas.drawString(256, 760, "(Deemed to be University) Patiala 147004 Punjab")
    pdf_canvas.drawString(
        0,
        730,
        "____________________________________________________________________________________________",
    )

def create_date_sheet_header(pdf_canvas):
    page_width, _ = A4
    text = "Date Sheet"
    text_width = pdf_canvas.stringWidth(text, "Helvetica", 12)
    x_centered = (page_width - text_width) / 2
    pdf_canvas.drawString(x_centered, 710, text)
    pdf_canvas.drawString(
        0,
        705,
        "____________________________________________________________________________________________",
    )

def generate_pdf(pdf_filename, data, subject_list):
    pdf_canvas = canvas.Canvas(pdf_filename)
    create_logo_pdf(pdf_canvas)
    create_header(pdf_canvas)
    create_date_sheet_header(pdf_canvas)

    y_position = 700
    max_y_position = 50

    pdf_canvas.setFont("Helvetica", 12)

    for day, shifts in data.items():
        y_position -= 50
        pdf_canvas.drawString(40, y_position, f"\n {day}:")
        y_position -= 15

        for subjects in shifts:
            for sub in subjects:
                target_subject = sub
                matching_subjects = [
                    subject
                    for subject in subject_list
                    if subject.startswith(target_subject)
                ]

                try:
                    pdf_canvas.drawString(
                        120, y_position, matching_subjects[0].split(" ")[0]
                    )
                    pdf_canvas.drawString(
                        180, y_position, matching_subjects[0].split(" - ", 1)[1]
                    )
                    y_position -= 15

                    if y_position < max_y_position:
                        pdf_canvas.showPage()
                        y_position = 700

                except:
                    pdf_canvas.drawString(120, y_position, str(matching_subjects))
                    y_position -= 15

    pdf_canvas.save()

def publish(tried_earlier):
    root = tk.Tk()
    root.title("Edit Dates")
    root.overrideredirect(True)
    width = 600
    height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg="white")

    # create_logo = tk.PhotoImage(file="logo.png").subsample(1)
    
    
    def show_text(message):
        """
         Display a text box. This is a convenience function to make it easier to use it in a program's main loop
         
         @param message - The message to display
        """
        textbox(root, message, 40, height - 100, 520)
    
    lbl1 = tk.Label(
        root,
        text=f"Don't close this window.",
        anchor="center",
        fg="black",
        bg="white",
        font=("Arial", 12),
    )
    lbl1.place(x=185, y=height - 30)
    lbl1.update()
    lbl1.place(x=(width - lbl1.winfo_width()) // 2, y=height - 25)

    lbl2 = tk.Label(
        root,
        text=f"Downloading Datesheet:",
        anchor="center",
        fg="black",
        bg="white",
        font=("Arial", 15),
    )
    lbl2.place(x=38, y=height - 150)

    show_text("This can take few seconds. Please be patient.")

    # If tried_earlier is true then we try to find all the students in the departments and all the students in the departments.
    if tried_earlier:
        departments = get_departments_and_branches()

        for department in departments:
            branches = []

            branch_ref = root_ref.child(f"departments/{department}/branches")

            for branch1 in branch_ref.get():
                branches.append(branch1)

            for branch in branches:
                try:
                    semesters = []
                    semester_ref = root_ref.child(
                        f"departments/{department}/branches/{branch}/semesters"
                    )
                    for semester1 in semester_ref.get():
                        semesters.append(semester1)
                except:
                    pass

                for semester in semesters:
                    subjects = get_subjects_and_students(department, branch, semester)
                    try:
                        if subjects is not None:
                            for subject, student_count in subjects.items():
                                if subject not in subject_list:
                                    subject_list.append(subject)
                    except:
                        pass
    show_text("Download it.")

    pdf_filename = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")]
    )

    if not pdf_filename:
        return

    root_ref = db.reference("/dates")
    data = root_ref.get()
    generate_pdf(pdf_filename, data, subject_list)

    show_text("Datesheet downloaded successfully.")
    time.sleep(1)
    root.destroy()
    root.mainloop()



if internet:
    one()
