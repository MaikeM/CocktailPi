import sqlite3
import sys
import webbrowser
import serial
import time

connection = sqlite3.connect("../db.sqlite3")
cursor = connection.cursor()
ser = serial.Serial('/dev/cocktailuino', 9600)
while (True):
    ###  Select Mix Steps from DB ###
    msg = ""
    result = None
    while (not result):
        cursor.execute("SELECT * FROM cocktaildb_order WHERE done = 0 ORDER BY date;") 
        result = cursor.fetchall()
        time.sleep(1)
    current_order = result[0]
    print(current_order)
    cocktail_id = current_order[4]
    step = current_order[1]
    if (step == 0):
        time.sleep(5)
        msg = '11 30000 '

        # msg = "1 "
        # answ = ""
        # while not msg in answ:
        #     print ("Pi: '{0}'".format(msg)) 
        #     ser.write(msg)
        #     while not ser.inWaiting():
        #         time.sleep(0.001)
        #     ### read answer of arduino
        #     answ = ser.readline()
        #     print ("Arduino: '{0}'".format(answ))
        # ### Wait for User Input to start ###
        # while (not "TOUCHED" in answ) or (not "NO_INPUT"):
        #     while not ser.inWaiting():
        #         time.sleep(0.001)
        #     ### read answer of arduino ###
        #     answ = ser.readline()
        #     print ("Arduino: '{0}'".format(answ))
        #     time.sleep(5)
        # if ("NO_INPUT" in answ):
        #     cursor.execute("DELETE FROM cocktaildb_order WHERE id = " + str(current_order) + ";")
    else:
        cursor.execute("SELECT * FROM cocktaildb_mixstep WHERE cocktail_id = " + str(cocktail_id) + " AND step = " + str(step) + ";") 
        step_result = cursor.fetchall() 
        ### For each Mix Step ###
        for r in step_result:
            print r
            step = r[1]
            jar = r[2]
            amount = r[3]
            cocktail_id = r[4]
            ingredient = r[5]
            action = r[6]
            msg = ""
            ### open current step in browser ###
            webbrowser.open('http://127.0.0.1:8000/cocktail/')
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
            elif (ingredient == 13 and amount < 10): # ICE
                msg = '10    ' + str(amount) + '     '
            elif (ingredient == 13 and amount >= 10): # ICE
                msg = '10 ' + str(amount) + '    '
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

            ### Delete amount of ingredient from db ###
            if (ingredient > 0 and ingredient < 13):
                cursor.execute("SELECT amount FROM cocktaildb_ingredient WHERE id = "+ str(ingredient) + ";")
                result2 = cursor.fetchall()
                for r in result2:
                    old_amount = r[0]
                new_amount = old_amount-amount
                print ("Old: " + str(old_amount) + ", ingredient_id: " + str(ingredient) + ", new: " + str(new_amount))
                cursor.execute("UPDATE cocktaildb_ingredient SET amount =" + str(new_amount) + " WHERE id =" + str(ingredient) + ";")
                connection.commit()

    ### send message to arduino & wait for right answer ###
    answ = ""

    while not msg in answ:
        print ("Pi: '{0}'".format(msg)) 
        ser.write(msg)
        while not ser.inWaiting():
            time.sleep(0.001)
        ### read answer of arduino
        answ = ser.readline()
        print ("Arduino: '{0}'".format(answ))
    print ("weight")
    answ = ""
    loop = True
    while (loop):
        while not ser.inWaiting():
            time.sleep(0.001)
        ### read answer of arduino
        answ = ser.readline()
        print ("Arduino: '{0}'".format(answ))
        if ("READY" in answ):
            loop = False
            cursor.execute("SELECT * FROM cocktaildb_mixstep WHERE cocktail_id = " + str(cocktail_id) + " AND step = " + str(step+1) + ";") 
            order_result = cursor.fetchall() 
            if (order_result):
                cursor.execute("UPDATE cocktaildb_order SET step =" + str(step+1) + " WHERE id =" + str(current_order[0]) + ";")
                connection.commit()
            else:
                cursor.execute("UPDATE cocktaildb_order SET done = 1 WHERE id = " + str(current_order) + ";")
                connection.commit
        elif ("TOUCHED" in answ):
            loop = False
            cursor.execute("UPDATE cocktaildb_order SET step = " + str(step+1) + " WHERE id =" + str(current_order[0]) + ";")
            connection.commit()
        elif ("NO_INPUT" in answ):
            cursor.execute("DELETE FROM cocktaildb_order WHERE id = " + str(current_order[0]) + ";")
            connection.commit
            loop = False
    print("loop break")
