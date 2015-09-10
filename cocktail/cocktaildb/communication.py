import sqlite3
import sys
import webbrowser
import serial
import time
#import os
#import django

#if __name__ == '__main__':  
#    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cocktaildb.settings')

#    django.setup()

connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()
ser = serial.Serial('/dev/cocktailuino', 9600)


###  Select Mix Steps from DB ###
cursor.execute("SELECT * FROM cocktaildb_mixstep WHERE cocktail_id = " + sys.argv[1]) 
result = cursor.fetchall() 
ser.write('0        ')
time.sleep(5)
### For each Mix Step ###
for r in result:
    print r
    step = r[1]
    jar = r[2]
    amount = r[3]
    cocktail_id = r[4]
    ingredient = r[5]
    action = r[6]
    msg = ""
    ### open current step in browser ###
    webbrowser.open('http://127.0.0.1:8000/cocktail/' + str(cocktail_id) + '/' + str(step) +'/')
    ### write corresponding message ###
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
    elif (ingredient == 13 and amount < 10):
        msg = '10 13 ' + str(amount) + '  '
    elif (ingredient == 13 and amount >= 10):
        msg = '10 13 ' + str(amount) + ' '
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
   
    ### send message to arduino ###
     

    ### wait for right answer ###
    answ = ""
    while not msg in answ:
        print ("Pi: '{0}'".format(msg)) 
        ser.write(msg)
        while not ser.inWaiting():
            time.sleep(0.001)
        ### read answer of arduino
        answ = ser.readline()
        print ("Arduino: '{0}'".format(answ))
    #while  ser.inWaiting():
    #    print (ser.readline())
    if (ingredient > 0 and ingredient < 13):
        print ("weight")
        answ = ""
        while not "READY" in answ:
            while not ser.inWaiting():
                time.sleep(0.001)
            ### read answer of arduino
            answ = ser.readline()
            print ("Arduino: '{0}'".format(answ))
            time.sleep(5)
            #ser.write(msg)
    else:
        time.sleep(5) ## TODO wait for arduino to continue
        