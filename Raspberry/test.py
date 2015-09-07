import sqlite3
import sys
import webbrowser
import serial
import time

connection = sqlite3.connect("../cocktail/db.sqlite3")

cursor = connection.cursor()

#cursor.execute("SELECT * FROM cocktaildb_cocktail") 
#print("fetchall:")
#result = cursor.fetchall() 
#for r in result:
#    print(r)

#for eachArg in sys.argv:  
#	print eachArg 
cursor.execute("SELECT * FROM cocktaildb_mixstep WHERE cocktail_id = " + sys.argv[1]) 
print("fetchall:")
result2 = cursor.fetchall() 
for r2 in result2:
    print(r2[1])

#webbrowser.open('http://127.0.0.1:8000/cocktail/' + sys.argv[1] + '/1/')

ser = serial.Serial('/dev/cocktailuino', 9600)
ser.write('2  2  123')
time.sleep(2)
ser.write('1  2  123')
while not ser.inWaiting():
	time.sleep(0.001)
a = ser.readline()
print (a)	
time.sleep(5)
ser.write('4  0  123')
time.sleep(0.2)
while not ser.inWaiting():
	time.sleep(0.001)
a = ser.readline()
print (a)