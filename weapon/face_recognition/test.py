
import face_recognition
import argparse
import pickle
import cv2
import sys
import os
import mysql.connector
import smtplib
import imghdr
from email.message import EmailMessage

ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", default="face_recognition/encodings.pickle",
                help="path to serialized db of facial encodings")
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
                help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())





def send_email(Name,a,m):

    Sender_Email = "nn7899042587@gmail.com"
    Reciever_Email = 'kisharukishu@gmail.com'
    Password = 'qtkslefgswrlswja'

    newMessage = EmailMessage()
    newMessage['Subject'] = "Alert"
    newMessage['From'] = Sender_Email
    newMessage['To'] = Reciever_Email
    newMessage.set_content('weapon detected\nName'+Name+"\nAadhar:"+a+"\nMobile:"+m)

    with open('face_recognition/weapon.jpg', 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name[7:]

    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email, Password)
        smtp.send_message(newMessage)


def fetchvalues(Name):
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="",
		database="weapon"
	)
	#print("recieved name"+name)
	mycursor = mydb.cursor()

	mycursor.execute("SELECT * FROM user WHERE Name=" + "'" + Name + "'")

	myresult = mycursor.fetchall()

	row_count = mycursor.rowcount
	# print("number of affected rows: {}".format(row_count))
	if row_count == 0:
		print("Person not registered")
	else:
		for row in myresult:
			Name = row[1]
			Aadhar = row[2]
			Mobile = row[3]
			
		print("Name: ", Name)
		print("Aadhar: ", Aadhar)
		print("Mobile: ", Mobile)
		send_email(Name,Aadhar,Mobile)
		
		

	mydb.close()

print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

image = cv2.imread(args["image"])
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


print("[INFO] recognizing faces...")
boxes = face_recognition.face_locations(rgb,
                                        model=args["detection_method"],number_of_times_to_upsample=2)
encodings = face_recognition.face_encodings(rgb, boxes,num_jitters=5)

names = []
name = "Unknown"

for encoding in encodings:
    matches = face_recognition.compare_faces(data["encodings"],
                                             encoding,tolerance=0.3)


    if True in matches:
        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
        counts = {}


        for i in matchedIdxs:
            name = data["names"][i]
            counts[name] = counts.get(name, 0) + 1

        name = max(counts, key=counts.get)
    
    
    names.append(name)
    print(name)
    
    fetchvalues(name)
    # send_email(name)

for ((top, right, bottom, left), name) in zip(boxes, names):
	cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
	y = top - 15 if top - 15 > 15 else top + 15
	cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
		0.75, (0, 255, 0), 2)
print(names)
cv2.imshow("Image", image)

cv2.waitKey(0)
sys.exit()
