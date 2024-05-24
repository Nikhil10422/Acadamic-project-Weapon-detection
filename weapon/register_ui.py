from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import cv2
import face_recognition
import time
import os
from imutils import paths
import argparse
import pickle
import mysql.connector


import tkinter as tk
from tkinter import PhotoImage
from PIL import Image


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=False,
	help="path to input directory of faces + images",default="face_recognition/dataset")
ap.add_argument("-e", "--encodings", required=False,default="face_recognition/encodings.pickle",
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="weapon"
)

def insertvalues():
    global name_entry,  aadhar_entry, mobile_entry, address_entry, history_entry,case1_entry,additional_number_entry

    mycursor = mydb.cursor()

    sql = "INSERT INTO user (Name, Aadhar, Mobile, Address, History,case1,Additional_number) VALUES " \
          "(%s, %s, %s,%s,%s,%s,%s) "
    val = (name_entry, str(aadhar_entry), str(mobile_entry), address_entry, str(history_entry),str(case1_entry),str(additional_number_entry))
    mycursor.execute(sql, val)

    mydb.commit()
    row_count = mycursor.rowcount
    if row_count == 0:
        print("Error values not inserted/Already registered")
    else:
        print("User Registered successfully")
    mycursor.close()

def submit():
    global name_entry,aadhar_entry, mobile_entry,address_entry,history_entry,case1_entry,additional_number_entry
    obama_image = face_recognition.load_image_file("test.png")
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    known_face_encodings = [
        obama_face_encoding
    ]
    known_face_names = [
        "Test"
    ]

    face_locations = []
    face_encodings = []
    face_names = []
    name_entry = name_a.get()
    aadhar_entry = aadhar.get()
    mobile_entry = mobile.get() 
    address_entry = address.get()
    history_entry = history.get()
    case1_entry=case1.get()
    additional_number_entry=additional_number.get()
    

    if(len(name_entry) == 0 or len(aadhar_entry) == 0 or len(mobile_entry) == 0 or len(history_entry)==0 or len(case1_entry)==0 or len(additional_number_entry)==0):
        messagebox.showerror("Error", "Please fill all the fields")
        return
    
    if(len(aadhar_entry)!=12):
        messagebox.showerror("Error", "Invalid aadhar")
        return

    if(len(mobile_entry)!=10):
        messagebox.showerror("Error", "Invalid mobile number")
        return
    
    if(len(additional_number_entry)!=10):
        messagebox.showerror("Error", "Invalid additional mobile number")
        return
        
    else:
        print(name_entry)
        video_capture = cv2.VideoCapture(0)

        path = ("face_recognition/dataset/" + name_entry)
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)

        process_this_frame = True
        font = cv2.FONT_HERSHEY_DUPLEX

        while True:
            code = cv2.waitKey(10)
            ret, frame = video_capture.read()

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            rgb_small_frame = small_frame[:, :, ::-1]

            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    names = "Face detected"

                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

                    face_names.append(names)

            process_this_frame = not process_this_frame
            cv2.putText(frame, "Press S to save", (10,40), font, 1, (255, 255, 255), 2)

            if code == ord('s'):
                for i in range(10):
                    print("saving ", i)
                    cv2.imwrite(path + "\\" + str(i) + ".jpg", frame)
                    time.sleep(0.5)
                insertvalues()
                break

                
            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 1)

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            cv2.imshow('Video', frame)

            if code == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

def train():  
    print("[INFO] quantifying faces...")
    imagePaths = list(paths.list_images(args["dataset"]))

    knownEncodings = []
    knownNames = []

    for (i, imagePath) in enumerate(imagePaths):
        print("[INFO] processing image {}/{}".format(i + 1,
            len(imagePaths)))
        name = imagePath.split(os.path.sep)[-2]

        image = cv2.imread(imagePath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        boxes = face_recognition.face_locations(rgb,
            model=args["detection_method"])

        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)

    print("[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}
    f = open(args["encodings"], "wb")
    f.write(pickle.dumps(data))
    f.close()

def convert_image(input_path, output_path):
    jpeg_image = Image.open(input_path)
    jpeg_image = jpeg_image.resize((1920, 1080), Image.ANTIALIAS)
    jpeg_image.save(output_path, "GIF")

root = Tk()
root.geometry("1920x1080")
root.configure(bg="gray")

 # Convert the JPEG image to GIF format using PIL
convert_image("4.jpg", "background.gif")  # Replace with your image path

    # Load the background image
bg_image = PhotoImage(file="background.gif")  # Use the converted GIF image

    # Create a label to display the background image
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)  # Cover the entire window



name_a = StringVar()
aadhar = StringVar()
mobile = StringVar()
address= StringVar()
history= StringVar()
case1=StringVar()
additional_number=StringVar()


label = Label(root,text="Real time weapon detection with criminal face identification",font=('calabre',20,'bold'))
label.place(x=270,y=5)

name_label = Label(root, text='Name', font=('calibre', 10, 'bold')).place(x=550, y=70, anchor="center")
name_entry = Entry(root, textvariable=name_a, font=('calibre', 10, 'normal')).place(x=650, y=70, anchor="center")

Label(root, text='Aadhar', font=('calibre', 10, 'bold')).place(x=550, y=110, anchor="center")
Entry(root, textvariable=aadhar, font=('calibre', 10, 'normal')).place(x=650, y=110, anchor="center")

Label(root, text='Mobile', font=('calibre', 10, 'bold')).place(x=550, y=150, anchor="center")
Entry(root, textvariable=mobile, font=('calibre', 10, 'normal')).place(x=650, y=150, anchor="center")

Label(root, text='Address', font=('calibre', 10, 'bold')).place(x=545, y=190, anchor="center")
Entry(root, textvariable=address, font=('calibre', 10, 'normal')).place(x=650, y=190, anchor="center")

Label(root, text='History', font=('calibre', 10, 'bold')).place(x=550, y=230, anchor="center")
Entry(root, textvariable=history, font=('calibre', 10, 'normal')).place(x=650, y=230, anchor="center")


Label(root, text='Case', font=('calibre', 10, 'bold')).place(x=555, y=270, anchor="center")
Entry(root, textvariable=case1, font=('calibre', 10, 'normal')).place(x=650, y=270, anchor="center")

Label(root, text='Additional number', font=('calibre', 10, 'bold')).place(x=510, y=310, anchor="center")
Entry(root, textvariable=additional_number, font=('calibre', 10, 'normal')).place(x=650, y=310, anchor="center")


btn = Button(root,text="Register",command=submit)
btn.place(x=570,y=363,anchor="center")

Button(root,text="Train",command=train).place(x=650,y=350)

mainloop()
