'''
File: qrReader.py
Description: The contents of this file are used to create an object tracking system using QR codes and a camera.
Created by: Bobby R. Stephens III & Nucleotide Network
Institution: Newton College and Career Academy
Date Created: 11/06/2023
'''

from pyzbar.pyzbar import decode
from picamera2 import Picamera2, Preview
from libcamera import controls
from libcamera import Transform
import threading
from gtts import gTTS
from tempfile import NamedTemporaryFile
from playsound import playsound
import pyttsx3 as tts
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from time import sleep
from gpiozero import Button

# Button Setup
buttonA = Button(22)
buttonB = Button(23)
buttonC = Button(24)


# Lists for each room

l_kitchenTable = []
l_bookShelf = []
l_bedRoomNightStand = []
l_bedRoomCloset = []
l_diningRoomTable = []

loc_list = ['l_kitchenTable',
            'l_bookShelf',
            'l_bedRoomNightStand',
            'l_bedRoomCloset',
            'l_diningRoomTable']
obj_list = []

picam2 = Picamera2()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous}) #enable continuous autofocus
barcodes = []
picam2.start()
cap = picam2.capture_array("main") #capture video from main camera in the form of an array

def qrReader():
    while True:
        cap = picam2.capture_array("main")
        barcodes = decode(cap) #decode the data from the array
        for b in barcodes:
            dec = b.data.decode('utf-8') #decodes the qr code from bytes to string
            if dec:
                if dec in loc_list:
                    temp_location_name = str(dec)
                    temp_location = eval(dec)
                    print("Temporary Location Stored: " + temp_location_name)
                elif (dec not in loc_list):
                    if dec not in obj_list:
                        obj_list.append(dec)
                    try:
                        if dec not in temp_location:
                            # if not in the temp location, remove from any other location
                            for i in loc_list:
                                if dec in eval(i):
                                    eval(i).remove(dec)
                                    print("Removed from " + i)
                            # add to temp location
                            temp_location.append(dec)
                            # print out the object and the name of the location it was added to
                            print(dec + "Added to " + temp_location_name)
                    except Exception as e:
                        pass
                        print(e)
                         #print("Object List: ")
                    # print(obj_list)

def speak(txt, lang='en'):
    try:
        gTTS(text=txt, lang=lang).write_to_fp(voice := NamedTemporaryFile())
        playsound(voice.name)
        voice.close()
    except Exception as e:
        print(e)
        engine = tts.init(driverName="espeak")
        engine.say(txt)
        engine.runAndWait()
        engine.stop()

def selection():
    selected_index = 0

    while True:
        # get the selected string
        if obj_list:
            

            # get the user input
            sleep(.15)

            # if the user enters 'a', move the selection to the left
            if buttonA.value == 1:
                selected_index = (selected_index - 1) % len(obj_list)
                selected_string = obj_list[selected_index]
                print(f"Selected: {selected_string[2:]}")
                speak(f"Selected: {selected_string[2:]}")
                

            # if the user enters 'd', move the selection to the right
            if buttonC.value == 1:
                selected_index = (selected_index + 1) % len(obj_list)
                selected_string = obj_list[selected_index]
                print(f"Selected: {selected_string[2:]}")
                speak(f"Selected: {selected_string[2:]}")

            # if the user presses enter, find the location of the selected item
            if buttonB.value == 1:
                # find the list the selected string is in
                for location in loc_list:
                    if selected_string in eval(location):
                        print(f"{selected_string[2:]} is at the {location[2:]}")
                        speak(f"{selected_string[2:]} is at the {location[2:]}")
                        break                   

def databaseSend():
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate(
        '/home/Hyperlapse/piZero-Smartglass/projectsmartglass-aee0e-firebase-adminsdk-vmdds-842cf32920.json')

    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://projectsmartglass-aee0e-default-rtdb.firebaseio.com/'
    })

    # As an admin, the app has access to read and write all data, regradless of Security Rules
    ref = db.reference('/')
    while True:
        # for every object in the list, update the database wtih the object and the location
        if obj_list:
            for i in obj_list:
                # find the location of the object
                for location in loc_list:
                    if i in eval(location):
                        ref.update({
                            i[2:]: location[2:]
                        })

                        break
        else:
            print("HOLDING ON DATA")
            sleep(2)

if __name__ == '__main__':

    qrReaderThread = threading.Thread(target=qrReader)
    qrReaderThread.start()

    selectionThread = threading.Thread(target=selection)
    selectionThread.start()

    databaseSendThread = threading.Thread(target=databaseSend)
    databaseSendThread.start()
    
    speak("Hello, All Systems Operational")
    print("Hello, All Systems Operational")
    
    databaseSendThread.join()
    qrReaderThread.join()
    selectionThread.join()
