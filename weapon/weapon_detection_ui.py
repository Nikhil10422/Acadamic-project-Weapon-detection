import cv2
import numpy as np
import os
import smtplib
import imghdr
from email.message import EmailMessage
from tkinter import *
from tkinter.ttk import *
import mysql.connector

import tkinter as tk
from tkinter import PhotoImage
from PIL import Image




net = cv2.dnn.readNet("yolov3_training_2000.weights", "yolov3_testing.cfg")
classes = ["Weapon"]


layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

def send_email():
    print("sending email")
    Sender_Email = "nn7899042587@gmail.com"
    Reciever_Email = "mpchetan@gmail.com"
    Password = 'qtkslefgswrlswja'

    newMessage = EmailMessage()
    newMessage['Subject'] = "Alert"
    newMessage['From'] = Sender_Email
    newMessage['To'] = Reciever_Email
    newMessage.set_content('weapon detected')

    with open('face_recognition/weapon.jpg', 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name[7:]

    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email, Password)
        smtp.send_message(newMessage)
    print("email sent")


def run():
    cap = cv2.VideoCapture(0)
    while True:
        _, img = cap.read()
        height, width, channels = img.shape

        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        print(indexes)
        if indexes == 0: 
            print("weapon detected in frame")
            cv2.imwrite("face_recognition/weapon.jpg",img)
            # send_email()
            # os.system('python face_recognition/recognize_faces_image.py'+' --image face_recognition/weapon.jpg')
            os.system('python face_recognition/test.py'+' --image face_recognition/weapon.jpg')
            # break
            
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 3, color, 3)

        cv2.imshow("Images", img)
        key = cv2.waitKey(1)
        if key == 102:
            cv2.imwrite("face_recognition/weapon.jpg",img)
            os.system('python face_recognition/test.py'+' --image face_recognition/weapon.jpg')

        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def fetchvaluesaadhar(Aadhar):
    global status_label,name_label_search,email_label_search,phone_label,address_label,history_label,case1_label,additional_number_label
    mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="",
		database="weapon"
	)
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM user WHERE Aadhar=" + "'" + Aadhar + "'")

    myresult = mycursor.fetchall()

    row_count = mycursor.rowcount
    if row_count == 0:
        print("Person not registered")
        status_label.config(text="Person not registered")
    else:
        for row in myresult:
           
           
            Name = row[1]
            Aadhar = row[2]
            Mobile= row[3]
            Address=row[4]
            History=row[5]
            case1=row[6]
            Additional_number=row[7]
			
        print("Name: ", Name)
        print("Aadhar: ", Aadhar)
        print("Mobile: ", Mobile)
        print("Address:",Address)
        print("History:",History)
        print("case1:",case1)
        print("Additional_number:",Additional_number)
        name_label_search.config(text="Name: "+Name)
        phone_label.config(text="Mobile:"+Mobile)
        address_label.config(text="Address:"+Address)
        history_label.config(text="History:"+History)
        case1_label.config(text="case1:"+case1)
        additional_number_label.config(text="Additional_number:"+Additional_number)


        
        #aahdar_label.config(text="Aadhar:"+Aadhar)
        
        path = "dataset/train/"+Name+"/0.jpg"
        cv2.imshow('image', cv2.imread(path))
        cv2.waitKey(5000)
        cv2.destroyWindow('image')
		

    mydb.close()

def search():


    #any updation or changes in search window


    global aadhar_search,search_win,name_label_search,email_label_search,phone_label,address_label,history_label,case1_label,additional_number_label
    a = aadhar_search.get()
    search_win.withdraw()
    search_details = Toplevel(root)
    search_details.title("Search")
    search_details.geometry('1920x1080')
    name_label_search = Label(search_details, text='Name', font=('calibre', 10, 'bold'))
    name_label_search.place(x=10,y=10)
    phone_label = Label(search_details, text='Phone', font=('calibre', 10, 'bold'))
    phone_label.place(x=10,y=50)
    aadhar_label_search = Label(search_details, text='Aadhar Number', font=('calibre', 10, 'bold'))
    aadhar_label_search.place(x=10,y=100)
    address_label=Label(search_details, text='Address', font=('calibre', 10, 'bold'))
    address_label.place(x=10,y=150)
    history_label=Label(search_details, text='History', font=('calibre', 10, 'bold'))
    history_label.place(x=10,y=200)
    case1_label=Label(search_details, text='case1', font=('calibre', 10, 'bold'))
    case1_label.place(x=10,y=250)
    additional_number_label=Label(search_details, text='Additional_number', font=('calibre', 10, 'bold'))
    additional_number_label.place(x=10,y=300)

    fetchvaluesaadhar(a)
    
def search_widget():
    global aadhar_search,search_win
    aadhar_search = StringVar()
    root.withdraw()
    search_win = Toplevel(root)
    search_win.geometry('1920x1080')
    search_win.title("Search")
    Entry(search_win, textvariable=aadhar_search, font=('calibre', 10, 'normal')).place(x=80,y=10)
    Button(search_win, text="Search", command=search).place(x=50,y=50)




def convert_image(input_path, output_path):
    jpeg_image = Image.open(input_path)
    jpeg_image = jpeg_image.resize((1920, 1080), Image.ANTIALIAS)
    jpeg_image.save(output_path, "GIF")



root = Tk()

root.geometry("1920x1080")
#root.configure(bg="sky blue")

 # Convert the JPEG image to GIF format using PIL
convert_image("4.jpg", "background.gif")  # Replace with your image path

    # Load the background image
bg_image = PhotoImage(file="background.gif")  # Use the converted GIF image

    # Create a label to display the background image
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)  # Cover the entire window

label = Label(root, text="Real Time Weapon detection with facial recognition system",font=('calabre',20,'bold'))

label.place(x=370, y=5)

btn = Button(root, text="Run", command=run)
btn.place(x=600, y=230)

Button(root, text="Search", command=search_widget).place(x=800,y=230)


mainloop()