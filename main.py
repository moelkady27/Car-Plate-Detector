import cv2
import arabic_reshaper
from bidi.algorithm import get_display
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import ImageFont, ImageDraw, Image, ImageTk
import easyocr


# load the image and resize it
def select_image():  # function to select an image
    file_path = filedialog.askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    frame = cv2.imread(file_path)  # read the image
    image = cv2.resize(frame, (800, 600))  # resize the image
    original_image = image  # save the original image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert the image to gray scale
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # blur the image
    edged = cv2.Canny(blur, 10, 200)  # detect edges

    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]  # sort contours from big to small
    approx = []  # list of approximations of the contours
    for c in contours:  # loop over the contours
        peri = cv2.arcLength(c, True)  # calculate the perimeter of the contour
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)  # approximate the contour
        if len(approx) == 4:  # if the contour has 4 vertices then it is the number plate
            n_plate_cnt = approx  # save the contour of the number plate
            break  # break from the loop
    if len(approx) != 4:  # if the contour of the number plate is not found
        return  # return from the function
    if n_plate_cnt.any():  # if the contour of the number plate is found
        (x, y, w, h) = cv2.boundingRect(n_plate_cnt)  # get the coordinates of the number plate
        license_plate = gray[y:y + h, x:x + w]  # crop the number plate from the gray image
        reader = easyocr.Reader(['ar'], gpu=False, verbose=False)  # initialize the reader
        detection = reader.readtext(license_plate)  # read the text from the number plate
    else:  # if the contour of the number plate is not found
        detection = []  # if the contour of the number plate is not found

    if len(detection) == 0:  # if the text is not found
        text = "Impossible to read the text from the license plate"  # set the text to be displayed
        cv2.putText(image, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 3)  # put the text on the image
        # Update text box with the result (text)
        text_box.delete(0, tk.END)  # delete the previous text
        text_box.insert(0, text)  # insert the new text

        # Convert images to PhotoImage objects
        original_image = cv2.resize(frame, (400, 300))  # resize the image
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)  # convert the image to RGB
        original_image = Image.fromarray(original_image)  # convert the image to PIL format
        photo_1 = ImageTk.PhotoImage(original_image)  # convert the image to PhotoImage format

        image = cv2.resize(image, (400, 300))  # resize the image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # convert the image to RGB
        image = Image.fromarray(image)  # convert the image to PIL format
        photo_2 = ImageTk.PhotoImage(image)  # convert the image to PhotoImage format

        plate = cv2.imread("p.jpg")  # read the image
        plate = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)  # convert the image to RGB
        plate = Image.fromarray(plate)  # convert the image to PIL format
        photo_3 = ImageTk.PhotoImage(plate)  # convert the image to PhotoImage format

        # Update image labels in the GUI
        label1.configure(image=photo_1)  # update the image label
        label1.image = photo_1  # keep a reference

        label2.configure(image=photo_2)  # update the image label
        label2.image = photo_2  # keep a reference

        label3.configure(image=photo_3)  # update the image label
        label3.image = photo_3  # keep a reference
    else:  # if the text is found
        cv2.drawContours(image, [n_plate_cnt], -1, (0, 255, 0), 3)  # draw the contour of the number plate

        fontPath = "arial.ttf"  # path to the font
        font = ImageFont.truetype(fontPath, 40)  # load the font
        img_pil = Image.fromarray(image)  # convert the image to PIL format
        text = f"{detection[0][1]}"  # get the text to be displayed
        reshaped_text = arabic_reshaper.reshape(text)  # reshape the text
        bidi_text = get_display(reshaped_text)  # get the text in the correct format
        draw = ImageDraw.Draw(img_pil)  # initialize the drawing context
        draw.text((x, y - 42), bidi_text, font=font, fill=(0, 255, 0))  # draw the text on the image
        image = np.array(img_pil)  # convert the image to numpy array

        outText = detection[0][1]  # get the text to be displayed
        arabic_nums = "٠١٢٣٤٥٦٧٨٩"  # arabic numbers
        result_characters = ""  # the characters of the text
        result_numbers = ""  # the numbers of the text
        if outText:  # if the text is not empty
            for i in range(len(outText)):  # loop over the text
                if outText[i] in arabic_nums:  # if the character is a number
                    result_characters = outText[:i]  # get the characters of the text
                    result_numbers = outText[i:]  # get the numbers of the text
                    break  # break from the loop
        temp = [x for x in result_characters if (x != " ")]  # remove the spaces from the characters
        temp2 = [x for x in result_numbers if (x != " ")]  # remove the spaces from the numbers
        result_characters = " ".join(temp)  # join the characters
        result_numbers = " ".join(temp2)  # join the numbers
        result = result_characters + " " + result_numbers  # join the characters and the numbers
        print(result)  # print the result

        # Update text box with the result
        text_box.delete(0, tk.END)  # delete the previous text
        text_box.insert(0, outText)  # insert the new text

        # Convert images to PhotoImage objects
        original_image = cv2.resize(frame, (400, 300))  # resize the image
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)  # convert the image to RGB
        original_image = Image.fromarray(original_image)  # convert the image to PIL format
        photo_1 = ImageTk.PhotoImage(original_image)  # convert the image to PhotoImage format

        image = cv2.resize(image, (400, 300))  # resize the image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # convert the image to RGB
        image = Image.fromarray(image)  # convert the image to PIL format
        photo_2 = ImageTk.PhotoImage(image)  # convert the image to PhotoImage format

        plate = cv2.cvtColor(license_plate, cv2.COLOR_BGR2RGB)  # convert the image to RGB
        plate = Image.fromarray(plate)  # convert the image to PIL format
        photo_3 = ImageTk.PhotoImage(plate)  # convert the image to PhotoImage format

        # Update image labels in the GUI
        label1.configure(image=photo_1)  # update the image label
        label1.image = photo_1  # keep a reference

        label2.configure(image=photo_2)  # update the image label
        label2.image = photo_2  # keep a reference

        label3.configure(image=photo_3)  # update the image label
        label3.image = photo_3  # keep a reference

    x = 1000
    y = 500
    text = f'{detection[0][1]}'  # get the text to be displayed
    reversed_text = text[::-1]  # Reverse the text
    reversed_numbers = "".join(reversed([c for c in reversed_text if c.isdigit()]))  # Reverse the numbers
    size = len(reversed_text)  # get the size of the text

    for c in range(size):  # loop over the characters
        lab = Label(root, bg="red", fg="white", width="2", height="2", font=("Arial", 14))  # create a label
        if reversed_text[c] != " ":  # if the character is not a space
            if reversed_text[c].isdigit():  # if the character is a number
                lab["text"] = reversed_numbers[0]  # get the number
                reversed_numbers = reversed_numbers[1:]  # remove the number from the list
            else:  # if the character is not a number
                lab["text"] = reversed_text[c]  # get the character
            lab.place(x=x - 100, y=y)  # place the label
            x += 30  # increment x
            if x >= 1300:  # if x is greater than 1300
                x = 410  # reset x
                y += 100  # increment y


# Create the GUI window
root = tk.Tk()  # create the root window
root.title("License Plate Recognition")  # set the title of the window

# Create a label to display the selected image
image_label = tk.Label(root)  # create a label
image_label.pack()  # pack the label

# Create a label to display the recognition result
message_label = tk.Label(root)  # create a label
message_label.pack()  # pack the label

# Create a button to select an image file
select_button = tk.Button(root, text="Select Image", command=select_image)  # create a button
select_button.pack()  # pack the button

frame1 = tk.Frame(root)  # create a new frame
frame1.pack(side=tk.LEFT, padx=10, pady=10)  # pack the frame

frame2 = tk.Frame(root)  # create a new frame
frame2.pack(side=tk.LEFT, padx=10, pady=10)  # pack the frame

frame3 = tk.Frame(root)  # create a new frame
frame3.pack(side=tk.LEFT, padx=10, pady=10)  # pack the frame
# Create a new frame for the text box
frame4 = tk.Frame(root)  # create a new frame
frame4.pack(side=tk.TOP, pady=10)  # pack the frame

text_box = tk.Entry(frame4, font=('Arial', 16), width=30)  # create a text box
text_box.pack(side=tk.LEFT, padx=10)  # pack the text box

# Create the initial ImageTk.PhotoImage objects for display
photo1 = ImageTk.PhotoImage(Image.new('RGB', (400, 300)))  # create a new image
photo2 = ImageTk.PhotoImage(Image.new('RGB', (400, 300)))  # create a new image
photo3 = ImageTk.PhotoImage(Image.new('RGB', (100, 70)))  # create a new image

# Create the image labels inside the frames
label1 = tk.Label(frame1, image=photo1)  # create a label
label1.pack()  # pack the label

label2 = tk.Label(frame2, image=photo2)  # create a label
label2.pack()  # pack the label

label3 = tk.Label(frame3, image=photo3)  # create a label
label3.pack()  # pack the label

# Run the GUI
root.mainloop()  # run the main loop