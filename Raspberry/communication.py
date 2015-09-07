import sqlite3
import sys
import webbrowser
import serial
import time

connection = sqlite3.connect("../cocktail/db.sqlite3")
cursor = connection.cursor()
#ser = serial.Serial('/dev/cocktailuino', 9600)


###  Select Mix Steps from DB ###
cursor.execute("SELECT * FROM cocktaildb_mixstep WHERE cocktail_id = " + sys.argv[1]) 
print("fetchall:")
result = cursor.fetchall() 
for r in result:
    print r
    step = r[1]
    jar = r[2]
    amount = r[3]
    cocktail_id = r[4]
    ingredient = r[5]
    action = r[6]
    msg = ""
    #webbrowser.open('http://127.0.0.1:8000/cocktail/' + str(cocktail_id) + '/' + str(step) +'/')
    if (jar == 0 and action == 0):
    	msg = '5        ' # take glass
    elif (jar == 1 and action == 0):
    	msg = '6        ' # take shaker
    elif (jar == 0 and action == 1):
    	msg = '7        ' # fill shaker in glass
    elif (action == 2):
    	msg = '8        ' # skake
    elif (action == 3):
    	msg = '9        ' # mix
    elif (action == 4):
    	msg = '1        ' # finish
    elif (ingredient >= 10 and amount < 10):
    	msg ='3  ' + str(ingredient) + ' ' + str(amount) + '  '
    elif(ingredient >= 10 and amount >= 10 and amount < 100):  
    	msg = '3  ' + str(ingredient) + ' ' + str(amount) + ' ' 
    elif(ingredient >= 10 and amount >= 100): 
        msg = '3  ' + str(ingredient) + ' ' + str(amount) 
    elif (ingredient < 10 and amount < 10):
    	msg = '3  ' + str(ingredient) + '  ' + str(amount) + '  '
    elif(ingredient < 10 and amount >= 10 and amount < 100):  
    	msg = '3  ' + str(ingredient) + '  ' + str(amount) + ' '
    elif(ingredient < 10 and amount >= 100):  
    	msg = '3  ' + str(ingredient) + '  ' + str(amount)
    else:
    	print('Error')
    print (msg) 
    #ser.write(msg) 
    #while not ser.inWaiting():
    #    time.sleep(0.001)
    #    a = ser.readline()
    #    print (a)
    #    if (a == 'Error'):

    #time.sleep(10)

    
#ser.write('2  2  123')
#time.sleep(5)
#ser.write('1  2  123')
#time.sleep(5)
#ser.write('4  0  123')
#while ser.inWaiting():
#	a = ser.readline()
#	print (a)


