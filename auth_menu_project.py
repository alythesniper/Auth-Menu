import sqlite3, os, time, math

def sqlite_setup_close(action, connection1=sqlite3.connect("student_scores.db")):
    """Sets up and closes sqlite.
    action: 1 for setup, 2 for commit & close, 3 for commit. Returns cursor, connection if called in setup mode"""
    if action == 1:
        connection = sqlite3.connect("student_scores.db")
        cursor = connection.cursor()
        # create scores table if it does not allready exit
        newTableCmd = """CREATE TABLE IF NOT EXISTS scores(
        student_name TEXT, 
        score INTEGER,
        set_number INTEGER)
        """
        cursor.execute(newTableCmd)
        return cursor, connection
    elif action == 2:
        connection1.commit()
        connection1.close()

    elif action == 3:
        connection1.commit()


def insert_recall_scores(list, cursor, action=1):
    """Inserts or recalls scores. List: list to parse. Cursor: sqlite cursor.
    Action: 1 for setup, 2 for recall"""
    if action == 1:
        for value in list:
            name = value[1]
            score = value[0]
            cursor.execute("INSERT INTO scores(student_name, score, set_number) VALUES(?, ?, ?)", (name, score, 1))
    if action == 2:
        cursor.execute("SELECT * FROM scores")
        for obj in cursor.fetchall():
            list.append(obj)
        return list


def validate_inputs(input):
    if input > 10 or input < 0:
        return False
    else:
        return True


cursor, connection = sqlite_setup_close(1)

print("Welcome To Student Score Calculator!")
while True:
    try:
        choice = int(input("""Please Choose An Option From Below:\n
-------------------------------
1. Enter Scores                
2. Search And Calculate Scores 
3. Exit
-------------------------------
    
Enter Choice Here: """))
    except ValueError:
         continue

    if choice == 1:
        scores = [] 
        average = 0
        print("Enter Your Student's Scores Here. Press Ctrl+C To Get Calculations\n\n")
        while True:
            try:
                try:
                    name = input("Enter Students Name: ")
                    score = int(input("Enter The Students Score: "))
                except ValueError:
                    continue
                
                if validate_inputs(score):
                    scores.append([score, name])
            except KeyboardInterrupt:
                for score in scores:
                    average += score[0]
                print(f"\nThe Average Score Is: {average/len(scores)}")
                print(f"{min(scores)[1]} Has The Lowest Score With: {min(scores)[0]}")
                print(f"{max(scores)[1]} Has The Highest Score With: {max(scores)[0]}")
                insert_recall_scores(scores, cursor)
                time.sleep(3.5)
                os.system("cls")
                break 

    if choice == 2:

        os.system("cls")
        scores = [] 
        found = False
        choice_1 = int(input("""\nPlease Choose A Function: 
1. Name Search
2. Score Search 

Enter Choice: """))
        os.system("cls")
        
        if choice_1 == 1:
            name = input("Enter Name: ")
            #extract student scores & names, place in array
            scores = insert_recall_scores(scores, cursor, 2)
            #search list using linear search
            for obj in scores:
                if obj[0] == name:
                    print(f"{obj[0]} has a score of {obj[1]}")
                    found = True

            if found == False:
                print("Student Not Found, Please Enter/Re-Enter Score.")
            time.sleep(3.5)
            os.system("cls")

            
        if choice_1 == 2:
            search_term = int(input("Enter Score To Find: "))
            scores = insert_recall_scores(scores, cursor, 2)
            changed = True

            #bubble sort
            while True:
                if changed == False:
                    break
                changed = False
                for i in range(0, len(scores)-1):
                    if scores[i] > scores[i+1]:
                        temp_small_int = scores[i+1]
                        temp_big_int = scores[i]
                        scores[i] = temp_small_int
                        scores[i+1] = temp_big_int
                        changed = True

            #binary search
            midpoint = 0
            low = 0
            high = len(scores)-1
            count = 0

            while True:
                #prevents ifninite loop if item not found
                count +=1
                if count > len(scores):
                    print("Student Not Found, Please Enter/Re-Enter Score.")
                    time.sleep(3.5)
                    os.system("cls")
                    break
                midpoint = math.floor((high + low) / 2)
                if scores[midpoint][1] == search_term:
                    print(f"{scores[midpoint][0]} has a score of {scores[midpoint][1]} ")
                    time.sleep(3.5)
                    os.system("cls")
                    break
                else:
                    if scores[midpoint][1] > search_term:
                        high = midpoint - 1 
                        
                    elif scores[midpoint][1] < search_term:
                        low = midpoint + 1 



    if choice == 3:
        #print exiting message
        for i in range(0,4):
            os.system("cls")
            print(f"Exiting{i * '.'}")
            time.sleep(0.5)

        os.system("cls")
        break

 

#safely close database
sqlite_setup_close(2, connection)
