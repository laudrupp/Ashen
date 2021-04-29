import mysql.connector
import random
import sys



#help funktio
def helpfunction():
    print("Commands to get you going in the game:")
    print("- 'map' to take a look at the map.")
    print("- 'move' or 'go' to move around the map.")
    print("- 'north', 'east', 'south' and 'west' are the directions you can go to.")
    print("- 'information' to get background information on a character.")
    print("- 'speak' or 'talk' to speak to a character.")
    print("- 'search' or 'investigate' to see if there's any items nearby.")
    print("- 'inventory' or 'items' to see the items you have in your inventory.")
    print("- 'quit' to quit the game.")
    return


#mappi funktio
def mapfunction():
    print("                         |-------------|")
    print("                         |   Church    |")
    print("                         |-------------|")
    print("                              | R |")
    print("                              | o |")
    print("                              | a |")
    print("                              | d |")
    print("|------------|           |-------------|           |------------|")
    print("|  Hospital  |--R-o-a-d--|    Mitre    |--R-o-a-d--|   River    |")
    print("|            |-----------|   Square    |-----------|            |")
    print("|------------|           |-------------|           |------------|")
    print("                              | R |")
    print("                              | o |")
    print("                              | a |")
    print("                              | d |")
    print("                         |-------------|")
    print("                         |    Tavern   |")
    print("                         |-------------|")


#show location funktio
def show_location(loc):
    cur = db.cursor()
    sql = "SELECT Description FROM area WHERE AreaID='" + str(loc) + "'"
    cur.execute(sql)
    for row in cur:
        print("")
        print (row[0])
    return


#show character funktio
def show_character(loc):
    cur = db.cursor()
    sql = "SELECT DISTINCT characters.Name, characters.Description FROM characters JOIN area WHERE characters.AreaID = (SELECT area.AreaID FROM area WHERE area.AreaID='" + str(loc) + "')"
    #print (sql)
    cur.execute(sql)
    if cur.rowcount>=1:
        for row in cur.fetchall():
            print (row[0],'is',row[1])
    else:
        print("You need to be near a suspect to get his/her background information.")
    return 


#intro
def intro():
    cur = db.cursor()
    sql = "select begining from intro;"
    cur.execute(sql)
    if cur.rowcount==2:
        for row in cur.fetchall():
            print (row[0])
    print("")
    print("Dr. Gobelin: “Good morning! Nice to meet you detective Dupont. We have quite a curious case on our hands. I have examined the body and I’m certain that Camille Roget didn’t die naturally. She was murdered. I need you to interrogate three suspects I have in mind and find some evidence to support our case.”")
    print("")
    print("Paul Dupont: “Understood. How do we proceed after that?”")
    print("")
    print("Dr. Gobelin: “After you’ve gotten enough information from the suspects and found some evidence, come talk to me at the Harvey Street Clinic. I’ll be heading back to the clinic now. Good luck on cracking the case!”")
    print("")
    murderer = str(input('Here are the names of the three suspects: Annie Chapman, Thomas Audley and Charles Warren. Which one of the names piques your interest initially? '))
    choice = 0
    while choice < 1:
        if murderer == "Annie" or murderer == "Annie Chapman" :
            cur = db.cursor()
            sql = 'update characters set guilty = 1 where characters.Name = "Thomas Audley";'
            #print(sql)
            cur.execute(sql)
            sql2 = 'update items set items.AreaID = "41" where items.Name = "Hammer";'
            #print(sql2)
            cur.execute(sql2)
            num = random.randint(46,49)
            sql3 = 'update items set items.AreaID ="' + str(num) + '" where items.Name = "Ring";'
            cur.execute(sql3)
            #print(sql3)
            choice = choice + 1
        elif murderer == "Thomas" or murderer == "Thomas Audley":
            cur = db.cursor()
            sql = 'update characters set guilty = 1 where characters.Name = "Charles Warren";'
            cur.execute(sql)
            #print(sql)
            sql2 = 'update items set items.AreaID = "41" where items.Name = "Wooden club";'
            cur.execute(sql2)
            #print(sql2)
            num = random.randint(46,49)
            sql3 = 'update items set items.AreaID ="' + str(num) +'" where items.Name = "Piece of fabric";'
            cur.execute(sql3)
            #print(sql3)
            choice = choice + 1
        elif murderer == "Charles" or murderer == "Charles Warren":
            cur = db.cursor()
            sql = 'update characters set guilty = 1 where characters.Name = "Annie Chapman";'
            cur.execute(sql)
            #print(sql)
            sql2 = 'update items set items.AreaID = "41" where items.Name = "Knife";'
            cur.execute(sql2)
            #print(sql2)
            num = random.randint(46,49)
            sql3 = 'update items set items.AreaID ="' + str(num) +'" where items.Name = "Pendant";'
            cur.execute(sql3)
            #print(sql3)
            choice = choice + 1
        else:
            print("Unknown command")
            choice = choice + 0
            murderer = str(input('Give new answer:'))
    print("")
    print("Alright, let the investigation begin!")
    print("")
    cur = db.cursor()
    sql = """SELECT area.Description FROM area WHERE area.AreaID = 41"""
    cur.execute(sql)
    for row in cur:
        print(row[0])
    return


#check dialog funktio
def check_dialog():
    cur = db.cursor()
    sql = "SELECT Used FROM dialog WHERE Used = 'TRUU'"
    cur.execute(sql)
    if cur.rowcount>=6:
        dialog2(loc)
    #print(sql)
    return


#dialog 1st round funktio
def dialog1(loc):
    cur = db.cursor()
    sql1 = """SELECT DISTINCT dialog.Questions, dialog.Answers
           FROM dialog, characters WHERE dialog.CharacterID = 
           (SELECT characters.CharacterID
           FROM characters WHERE characters.AreaID = """+ str(loc) +"""
           AND dialog.LineID BETWEEN 50 AND 57
           AND dialog.Used = 'FALSE'
           AND characters.Guilty = dialog.Guilty)"""
    #print (sql1)
    cur.execute(sql1)
    if cur.rowcount>=1:
        for row in cur.fetchall():
            print (row[0])
            print("")
            print (row[1])
    else:
        print("...")
    
    sql2 = """UPDATE dialog
           SET dialog.Used = 'TRUU'
           WHERE dialog.CharacterID = 
           (SELECT characters.CharacterID
           FROM characters WHERE characters.AreaID = """+ str(loc) +"""
           AND dialog.LineID BETWEEN 50 AND 57)"""
    cur.execute(sql2)
    return


#dialog 2nd round funktio
def dialog2(loc):
    cur = db.cursor()
    sql = """SELECT DISTINCT dialog.Questions, dialog.Answers, dialog.Used
             FROM dialog, characters WHERE dialog.CharacterID = 
             (SELECT characters.CharacterID
             FROM characters WHERE characters.AreaID = """+ str(loc) +"""
             AND dialog.LineID BETWEEN 60 AND 67
             AND dialog.Used = 'FALSE'
             AND characters.Guilty = dialog.Guilty)"""
    cur.execute(sql)
    if cur.rowcount>=1:
        for row in cur.fetchall():
            print (row[0])
            print("")
            print (row[1])
    sql2 = """UPDATE dialog
              SET dialog.Used = 'TRUU'
              WHERE dialog.CharacterID = 
              (SELECT characters.CharacterID
              FROM characters WHERE characters.AreaID = """+ str(loc) +"""
              AND dialog.LineID BETWEEN 60 AND 67)"""
    cur.execute(sql2)
    #print (sql)
    return


#gobelin talk funktio
def gobelin_talk():
    gobelin_outro()
    cur = db.cursor()
    sql = """SELECT DISTINCT dialog.Questions, dialog.Answers
             FROM dialog, characters WHERE dialog.CharacterID =
             (SELECT characters.CharacterID FROM characters WHERE characters.AreaID = """+ str(loc) +"""
             AND dialog.LineID = 70)"""
    cur.execute(sql)
    if cur.rowcount>=1:
        for row in cur.fetchall():
            print("")
            print (row[0])
    else:
        return


#gobelin outro funktio
def gobelin_outro():
    cur = db.cursor()
    sql = "SELECT Used FROM dialog WHERE Used = 'TRUU'"
    cur.execute(sql)
    #print(sql)
    if cur.rowcount<12:
        for row in cur.fetchall():
            return
    else:
        cur = db.cursor()
        sql = """SELECT name FROM items WHERE items.PlayerID = 1"""
        cur.execute(sql)
        #print(sql)
        if cur.rowcount<2:
            for row in cur.fetchall():
                return
        else:
            if loc == 45:
                outro()
            else:
                return
    


#outro
def outro():
    cur = db.cursor()
    sql = """UPDATE dialog SET dialog.LineID = 71 WHERE dialog.LineID = 70"""
    cur.execute(sql)
    print("")
    answer = str(input("""Martin Gobelin: "I see you have gathered compelling evidence and interrogated all the suspects thoroughly. Are we thinking of the same suspect here? Who do you think the murderer is? Annie Chapman, Thomas Audley or Charles Warren?" """))
    choice = 0
    while choice < 1:
        if answer == "Annie" or answer == "Annie Chapman" :
            cur = db.cursor()
            sql = """SELECT characters.CharacterID, characters.Guilty FROM characters WHERE characters.CharacterID = 21 AND characters.Guilty = 1"""
            cur.execute(sql)
            if cur.rowcount>=1:
                for row in cur.fetchall():
                    print("")
                    print("""Martin Gobelin: "That is spot on my friend! She seems very suspicious to me. We need to get her arrested immediately!" """)
            else:
                print("")
                print("""Martin Gobelin: "That is completely wrong! Why would you even suggest an innocent girl like her would commit a murder? You are not qualified as a detective!" """)
            choice = choice + 1
        elif answer == "Thomas" or answer == "Thomas Audley":
            cur = db.cursor()
            sql = """SELECT characters.CharacterID, characters.Guilty FROM characters WHERE characters.CharacterID = 23 AND characters.Guilty = 1"""
            cur.execute(sql)
            if cur.rowcount>=1:
                for row in cur.fetchall():
                    print("")
                    print("""Martin Gobelin: "That is spot on my friend! He seems very suspicious to me. We need to get him arrested immediately!" """)
            else:
                print("")
                print("""Martin Gobelin: "That is completely wrong! Why would you even suggest an innocent man like him would commit a murder? You are not qualified as a detective!" """)
            choice = choice + 1
        elif answer == "Charles" or answer == "Charles Warren":
            cur = db.cursor()
            sql = """SELECT characters.CharacterID, characters.Guilty FROM characters WHERE characters.CharacterID = 22 AND characters.Guilty = 1"""
            cur.execute(sql)
            if cur.rowcount>=1:
                for row in cur.fetchall():
                    print("")
                    print("""Martin Gobelin: "That is spot on my friend! He seems very suspicious to me. We need to get him arrested immediately!" """)
            else:
                print("")
                print("""Martin Gobelin: "That is completely wrong! Why would you even suggest an innocent man like him would commit a murder? You are not qualified as a detective!" """)
            choice = choice + 1
            
        else:
            print("Excuse me?")
            choice = choice + 0
            answer = str(input('? '))
    print("")
    print("You finished the game. Hooray!")
    print("")
    print("This game was made by Joni Kokko and Lauri Järvisalo. Thank you for playing!")
    sys.exit(0)   


#move funktio
def move(loc, newloc):
        cur = db.cursor()
        sql = "SELECT AreaID FROM movement WHERE ToId='" + str(newloc) + "' AND FromId='" + str(loc) + "'"
        #print (sql)
        cur.execute(sql)
        if cur.rowcount>=1:
            for row in cur.fetchall():
                destination = newloc
        else:
            destination = loc; # movement not possible
        return destination


#search and pick evidence
def investigate():
    cur = db.cursor()
    sql = 'select distinct items.Name, items.Description from items join area where items.AreaID ="' + str(loc) +'"'
    #print(sql)
    cur.execute(sql)
    if cur.rowcount >= 1:
        for row in cur.fetchall():
            #print (row[0], '-', row[1])
            print ('You found', row[1])
            sql2 = "update items set items.PlayerID = 1 where items.AreaID ='" + str(loc) + "'"
            #print(sql2)
            cur.execute(sql2)
            sql3 = "update items set items.AreaID = null where items.AreaID ='" + str(loc) + "'"
            #print(sql3)
            cur.execute(sql3)
            print("")
            print("You picked up the evidence.")
    else:
        print("")
        print("There's no items to be found here.")
    return


#carried items
def inventory():
    cur = db.cursor()
    sql = 'SELECT name, description FROM items WHERE items.PlayerID = 1;'
    cur.execute(sql)
    if cur.rowcount >= 1:
        for row in cur.fetchall():
            print (row[0], '-', row[1])
    else:
        print('You dont have any items.')
    return


db = mysql.connector.connect(host="localhost",
                             user="dbuser08",
                             passwd="dbpass",
                             db="ashen08",
                             buffered=True)


#start of the game
loc = 41
action = ""

intro()

#main loop
while action!="quit" and loc!=99:
    print("")
    input_string=input("What do you want to do? ").split()
    if len(input_string)>=1:
        action = input_string[0].lower()
    else:
        action = ""
    if len(input_string)>=2:
        target = input_string[len(input_string)-1].lower()
    else:
        target = ""
    #print("Parsed action: " + action)
    #print("Parsed target: " + target)
    print("")


    #move
    if action == 'move' or action == 'go':
        destination = input("Where would you like to go? ")
        cur = db.cursor()
        sql = "SELECT movement.ToId FROM movement WHERE direction='" + str(destination) + "' AND FromId='" + str(loc) + "'"
        cur.execute(sql)
        if cur.rowcount>=1:
            for row in cur.fetchall():
                landing = row[0]
                #print(row[0])
        else:
            landing = loc
            print("")
        
        newloc = move(loc,landing)
        if loc == newloc:
            print("You can't go there.");
        else:
            loc = newloc
            show_location(loc)
        #print("You are in " + str(loc))


    #show character details
    if action=="information":
        show_character(loc)


    #talk to a character
    if action=="speak" or action=="talk":
        check_dialog()
        dialog1(loc)
        gobelin_talk()


    #search/investigate
    if action == 'search' or action == 'investigate':
        investigate()


    #inventory
    if action == 'inventory' or action == 'items':
        inventory()


    #help
    if action=="help":
        helpfunction()


    #map
    if action=="map":
        mapfunction()
