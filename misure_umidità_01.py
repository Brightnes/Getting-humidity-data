"""
AstroPi o RaspberryPi con Sense Hat.
Per 24 ore di funzionamento, registra l'umidità ad ogni minuto e crea un file csv.
Mentre registra i valori di umidità relativa sul display c'è u quadrato verde,
Quando il programma ha finito, sul display compare un quadrato rosso.
Il programma può essere terminato premendo ctrl e c

"""


from sense_hat import SenseHat
from datetime import datetime, timedelta
from time import sleep
import random
import os
import csv
time_total = timedelta(hours=24)
termination=1
pause_time = 1

#A seguire, alcune definizioni di colori
b = (0,0,0)
v = (0,255,0)
r = (255,0,0)

# A seguire un'immagine da presentare a display che indica lo stato attivo
working = [
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,v,v,b,b,b,
    b,b,b,v,v,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b]

# A seguire, un'immagine da presentare a display che indica lo stato di fine attività
finished = [
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,r,r,b,b,b,
    b,b,b,r,r,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b,
    b,b,b,b,b,b,b,b]



dir_path = os.path.dirname(os.path.realpath(__file__))

# Connect to the Sense Hat
sh = SenseHat()

def create_csv_file(data_file):
    """
    Create a new CSV file and add the header row
    """
    with open(data_file, 'w') as f:
        writer = csv.writer(f)
        header = ("Date/time", "Humidity percent")
        writer.writerow(header)

def add_csv_data(data_file, data):
    """
    Add a row of data to the data_file CSV
    """
    with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# A seguire, una funzione che manda a display il segnale di stato attivo.
# La funzione accetta due variabili: la figura da visualizzare (pic)
# e la pausa (wait) tra una visualizzazione e la successiva.
def ok_working(pic, wait):
    for a in range(59):
        sh.set_pixels(pic)
        sleep(wait/2)
        sh.clear()
        sleep(wait/2)

sh.show_message("started")
# initialise the CSV file
data_file = dir_path + "/humidity.csv"
create_csv_file(data_file)
# store the start time
start_time = datetime.now()
# store the current time
# (these will be almost the same at the start)
now_time = datetime.now()

"""
sh.set_pixel(3,3,0,255,0)
sh.set_pixel(3,4,0,255,0)
sh.set_pixel(4,3,0,255,0)
sh.set_pixel(4,4,0,255,0)
"""

while now_time-start_time <= time_total:
    try:
        humidity_value = round(sh.get_humidity(),2)
        data = (datetime.now(), humidity_value)
        add_csv_data(data_file, data)
        ok_working(working, pause_time)
        now_time=datetime.now()
    except:
        termination=0
        break
if termination==1:
    print("Program finished")
elif termination==0:
    print("Program interrupted")
"""
sh.set_pixel(3,3,255,0,0)
sh.set_pixel(3,4,255,0,0)
sh.set_pixel(4,3,255,0,0)
sh.set_pixel(4,4,255,0,0)
"""
sh.set_pixels(finished)
