import os
import psycopg2
import hashlib
from datetime import datetime
# date.today()

connection = psycopg2.connect(
    host = "localhost",
    database = "project",
    user = os.environ['DB_USERNAME'],
    password = os.environ['DB_PASSWORD']
)
cursor = connection.cursor()
global session
global post_ID
global salt
salt = b'\x0e\xf2H\xb7\x8ca\x88\x82\xe9\x08\t\xbe\x1e\x95x:\xd0\xe2~\xe7\xb8\xdfpw\xb9\xe6E\x9b\rx\xc1h'




def login():
    global session

    print("Logging In!")

    username = input("Enter your username: \n")
    password = input("Enter your password: \n")

    cursor.execute("SELECT Password FROM Users WHERE Username = %s", [username])
    exists = cursor.fetchone()


    # print("Exists: ", exists)
    
    if exists:
        salted_password = password.encode('utf-8') + salt
        hashed_password = str(hashlib.sha256(salted_password).hexdigest())
        
        # CHANGE HASH_PASS
        if hashed_password == exists[0]:
            # print("You're in!")
                session = username
                print("login session: ", session)
                main()
        elif password == exists[0]:
            session = username
            print("login session: ", session)
            main()
        else: 
            print("Error in login process. Try Again.")
            return False
    else:
        print("Error in login process. Try Again.")
        return False



def register():

    print("Registering your account!")

    badges = ["1. Mercedes-AMG Petronas Formula One Team: MC", "2. Red Bull Racing Honda: RB", "3. Scuderia Ferrari Mission Winnow: FR",
    "4. Alpine F1 Team: AP", "5. McLaren Racing: MC", "6. Scuderia AlphaTauri Honda: AT", "7. Aston Martin Cognizant Formula One Team: AM",
    "8. Alfa Romeo Racing ORLEN: AR", "9. Haas F1 Team: HA", "10. Williams Racing: WI"]

    valid_team_inputs = ["1","2","3","4","5","6","7","8","9"]

    while True:
        name = input("Enter your name: \n")
        if 30 < len(name) < 1:
            print("Name is invalid. Try again")
        else:
            break

    email = input("Enter your email: ")

    while True:
        username = input("Please enter a username (Between 3-10 characters): \n")
        if  10 < len(username) < 3:
            print("Username is invalid, Try again")
            continue
        # check if in database 
        cursor.execute("SELECT Username FROM Users WHERE Username = %s", [username]) 
        exists = cursor.fetchone()
        if exists:
            print("username is already in use")
            continue
        break

    while True: 
        password = input("Enter your password (Between 8-16 characters): \n")
        if 16 < len(password) < 8:
            print("Password is invalid, Try again")
        else:
            password2 = input("Confirm your password (Between 8-16 characters): \n")
            if 16 < len(password) < 8 or password != password2:
                print("Password does not match, Try again")
            else:
        
                # salt = os.urandom(32) # Generate a random salt
                salted_password = password.encode('utf-8') + salt
                hashed_password = str(hashlib.sha256(salted_password).hexdigest())
                # generate random salt, encode with utf-8, hash with sha256, commit
                # salt password later 
                break
                
    
    
    while True:

        print("Please select a badge from the list below by entering the relating number: ")

        for team in badges:
            print(team)

        team = input()
        if team in valid_team_inputs:
            break
    if team == "1":
        badge = "MC"
    elif team == "2":
        badge = "RB"
    elif team == "3":
        badge = "FR"
    elif team == "4":
        badge = "AP"
    elif team == "5":
        badge = "MC"
    elif team == "6":
        badge = "AT"
    elif team == "7":
        badge = "AM"
    elif team == "8":
        badge = "AR"
    elif team == "9":
        badge = "HA"
    elif team == "10":
        badge = "WI"


    today = datetime.today()

    # push into database
    cursor.execute("INSERT INTO Users (Username,Email,Password, Name, Badge, DateCreated) VALUES (%s, %s, %s, %s, %s, %s)", (username, email, hashed_password, name, badge, today))
    connection.commit()
    connection.commit()



def post():
   
    valid_blog = ["commentary", "funny", "rant"]
    valid_driver = ["Lewis Hamilton", "Max Verstappen", "Sergio Perez", "Fernando Alonso", "Carlos Sainz", "Lance Stroll", "George Russell", "Lando Norris", "Nico Hulkenburg", "Charles leclerc", "Valtteri Bottas", "Esteban Ocon", "Oscar Piastri", "Pierre Gasly", "Zhou Guanyu", "Yuki Tsunoda", "Kevin Magnussen", "Alexander Albon", "Logan Sargeant", "Nyck De Vries"]
    valid_team = ["Ferrari", "Mercedes", "Mclaren", "Aston Martin", "Alpha Tauri", "Alfa Romeo", "Haas", "Williams", "Alpine", "Red Bull"]
    valid_race = ["Bahrain", "Australia", "Miami"]
    global post_ID
    global session 

    print("session check: ", session)

    timestamp = datetime.now()

    text = input("Enter your blog text (Under 2000 Characters): ")
    if len(text) > 2000:
        print(text)
        print(f"too long over by {len(text) - 2000} characters")
        while True:
            text = input("Re-Enter your blog text (Under 2000 Characters): ")
            if 2000 < len(text): 
                continue
            break

    tag = ''

    while True:

        print("Would you like to add a tag?")
        print("1. Yes")
        print("2. No")

        val = input()
        if val == "1":
            print("Choose from the following options: ")
            print("Would you like to tag based on ")
            print(" 1. Blog Type \n 2. Driver Name \n 3. Team Name \n 4. Race Name")
            choice = input()

            if choice == "1":
                print("Choose from the following options: ")
                print(" 1. Commentary \n 2. Funny \n 3.Rant ")
                tag = input()
                if tag in valid_blog:
                    break
            elif choice == "2":
                print("Choose from the following options: ")
                print(" 1. Lewis Hamilton \n 2. Max Verstappen \n 3. Sergio Perez \n 4. Fernando Alonso \n 5. Carlos Sainz \n 6. Lance Stroll\n 7. George Russell \n 8. Lando Norris \n 9. Hulkenburg \n 10. Charles Leclerc \n 11. Valtteri Bottas \n 12. Esteban Ocon \n 13. Oscar Piastri \n 14. Pierre Gasly \n 15. Zhou Guanyu \n 16. Yuki Tsunoda \n 17. Kevin Magnussen \n 18. Alexander Albon \n 19. Logan Sargeant \n 20. Nyck De Vries ")
                tag = input()
                if tag in valid_driver:
                    break
            elif choice == "3":
                print("Choose from the following options: ")
                print(" 1. Ferrari \n 2. Mercedes \n 3. Mclaren \n 4. Aston Martin \n 5. Alpha Tauri \n 6. Alfa Romeo \n 7. Haas \n 8. Williams \n 9. Alpine \n 10. Red Bull ")
                tag = input()
                if tag in valid_team:
                    break
            elif choice == "4":
                print("Choose from the following options: ")
                print(" 1. Bahrain \n 2. Australia \n 3.Miami ")
                tag = input()
                if tag in valid_blog:
                    break
        elif val == "2":
            break



    
    cursor.execute("INSERT INTO Posts (Text, Tags, Author, PostCreated) VALUES (%s, %s, %s,%s)", (text, tag, session, timestamp))
    connection.commit()

    print("Post Created Successfully!")
    main()
    


def feed():
    global session
    flag1 = False
    flag2 = False
    flag3 = False

    print("Do you want to filter your feed? ")
    print(" 1. Yes \n 2. No \n")
    val = input()
    if val == "1":
        
        print("These are the available filters: ")
        print(" 1. Author \n 2. Tags \n 3. Likes")
        print("How many filters would you like to use? (1-3)")
        count = int(input())
    
        for i in range(count):

            print("Select your filter: ")
            print(" 1. Author \n 2. Tags \n 3. Likes")
            choice = input()

            if choice == "1":
                # Author 
                print("Enter the user name: ")
                author = input()
                flag1 = True

            elif choice == "2":

                flag2 = True

                print("Choose one of the categories below: ")
                print("Type 1: Blog Type")
                print("Type 2: Driver Name")
                print("Type 3: Grid Teams")
                print("Type 4: Race Name")
                category = input()

                if category == "1":
                    print("Choose one of the tags below: ")
                    print(" 1. Commentary \n 2. Funny \n 3. Rant ")
                    num = input()
                    if num == "1":
                        tag = "Commentary"
                    elif num == "2":
                        tag = "Funny"
                    elif num == "3":
                        tag = "Rant"

                elif category == "2":
                    print("Choose one of the tags below: ")
                    print(" 1. Lewis Hamilton \n 2. Max Verstappen \n 3. Sergio Perez \n 4. Fernando Alonso \n 5. Carlos Sainz ")
                    print(" 6. Lance Stroll \n 7. George Russell \n 8. Lando Norris \n 9. Nico Hulkenburg \n 10. Charles Leclerc ")
                    print(" 11. Valtteri Bottas \n 12. Esteban Ocon \n 13. Oscar Piastri \n 14. Pierre Gasly \n 15. Zhou Guanyu ")
                    print(" 16. Yuki Tsunoda \n 17. Kevin Magnussen \n 18. Alexander Albon \n 19. Logan Sargeant \n 20. Nyck De Vries ")
                    num = input()
                    if num == "1":
                        tag = "Lewis Hamilton"
                    elif num == "2":
                        tag = "Max Verstappen"
                    elif num == "3":
                        tag = "Sergio Perez"
                    elif num == "4":
                        tag = "Fernando Alonso"
                    elif num == "5":
                        tag = "Carlos Sainz"
                    elif num == "6":
                        tag = "Lance Stroll"
                    elif num == "7":
                        tag = "George Russell"
                    elif num == "8":
                        tag = "Lando Norris"
                    elif num == "9":
                        tag = "Nico Hulkenburg"
                    elif num == "10":
                        tag = "Charles Leclerc"
                    elif num == "11":
                        tag = "Valtteri Bottas"
                    elif num == "12":
                        tag = "Esteban Ocon"
                    elif num == "13":
                        tag = "Oscar Piastri"
                    elif num == "14":
                        tag = "Pierre Gasly"
                    elif num == "15":
                        tag = "Zhou Guanyu"
                    elif num == "16":
                        tag = "Yuki Tsunoda"
                    elif num == "17":
                        tag = "Kevin Magnussen"
                    elif num == "18":
                        tag = "Alexander Albon"
                    elif num == "19":
                        tag = "Logan Sargeant"
                    elif num == "20":
                        tag = "Nyck De Vries"
                    
                elif category == "3":
                    print("Choose one of the tags below: ")
                    print(" 1. Ferrari \n 2. Mercedes \n 3. Mclaren \n 4. Aston Martin \n 5. Alpha Tauri \n 6. Alfa Romeo \n 7. Haas \n 8. Williams \n 9. Alpine \n 10. Red Bull ")
                    num = input()
                    if num == "1":
                        tag = "Ferrari"
                    elif num == "2":
                        tag = "Mercedes"
                    elif num == "3":
                        tag = "Mclaren"
                    elif num == "4":
                        tag = "Aston Martin"
                    elif num == "5":
                        tag = "Alpha Tauri"
                    elif num == "6":
                        tag = "Alfa Romeo"
                    elif num == "7":
                        tag = "Haas"
                    elif num == "8":
                        tag = "Williams"
                    elif num == "9":
                        tag = "Alpine"
                    elif num == "10":
                        tag = "Red Bull"

                elif category == "4":
                    print("Choose one of the tags below: ")
                    print(" 1. Bahrain \n 2. Australia \n 3. Miami ")
                    num = input()
                    if num == "1":
                        tag = "Bahrain"
                    elif num == "2":
                        tag = "Australia"
                    elif num == "3":
                        tag = "Miami"
            elif choice == "3":
                flag3 = True
                print("Enter the minimum like count: ")
                likes = int(input())

        if flag1 and not flag2 and not flag3:
            # author only   
            cursor.execute("SELECT * FROM Posts WHERE Author = %s", (author,))
            posts = cursor.fetchall()
           

        elif flag2 and not flag1 and not flag3:
            # only tag
            cursor.execute("SELECT * FROM Posts WHERE Tags = %s", (tag,))
            posts = cursor.fetchall()

        elif flag3 and not flag1 and not flag2:
            # only likes
            print("here")
            cursor.execute("SELECT * FROM Posts WHERE Likes >= %s", (likes,))
            posts = cursor.fetchall()
            print(posts)

        elif flag1 and flag2 and not flag3:
            # author and tag
            cursor.execute("SELECT * FROM Posts WHERE Author = %s AND Tags = %s", (author, tag))
            posts = cursor.fetchall()
        
        elif flag1 and flag3 and not flag2:
            # author and likes
            cursor.execute("SELECT * FROM Posts WHERE Author = %s AND  Likes >= %s", (author, likes))
            posts = cursor.fetchall()

        elif flag2 and flag3 and not flag1:
            # tag and likes
            cursor.execute("SELECT * FROM Posts WHERE Tags = %s AND Likes >= %s", (tag, likes))
            posts = cursor.fetchall()

        elif flag1 and flag2 and flag3:
            # author, tag, likes
            cursor.execute("SELECT * FROM Posts WHERE Author = %s AND Tags = %s AND Likes >= %s", (author, tag, likes))
            posts = cursor.fetchall()

    elif val == "2":
        cursor.execute("SELECT * FROM Users JOIN Posts ON Users.Username = Posts.Author JOIN followers ON Users.Username = followers.User2 WHERE followers.User1 = %s", [session])
        posts = cursor.fetchall()

    if not posts:
        print("There are no posts available with the appplied filter(s)")
        main()

    i = len(posts) - 1
    # print("post: ", len(posts))
    while True:

        print("\n")
        print("User: ", posts[i][4])
        print(posts[i][2])
        print("Likes: ", posts[i][1])
        print("Tags: ", posts[i][3])
        print("Date Posted: ", posts[i][5])

        print("Select from the following: ")
        print("1. See Previous \n 2. See Next \n 3. Like \n 4. Go Back")
        val = input()

        if val == "1":
            if i != len(posts) - 1:
                i += 1
        elif val == "2":
            if i != 0:
                i -= 1
        elif val == "3":
            likes = int(posts[i][2])
            likes += 1
            likes = str(likes)
            print("Likes: ", likes)

            PID = posts[i][3]
            cursor.execute("UPDATE Posts SET Likes = %s WHERE PID = %s", (likes, PID))
            connection.commit()  

        elif val == "4":
            main()


def remove(user1, user2):
    cursor.execute("DELETE FROM followers where User1 = %s AND User2 = %s", (user1, user2))
    connection.commit()
def add(user1, user2):
    cursor.execute("INSERT INTO followers (User1, User2) VALUES (%s, %s)", (user1, user2))
    connection.commit()  


def followers():
    # getting follower count 

    cursor.execute("SELECT COUNT(User1) FROM followers WHERE User2 = %s", (session, ))
    num_followers = cursor.fetchall()
    print(f"You have {num_followers[0][0]} followers ")
    
    print("What would you like to do?")
    print("1. See Followers")
    print("2. Search Followers")
    print("3. Remove a Follower")
    selection = input()

    if selection == "1":

        cursor.execute("SELECT User1 FROM followers WHERE User2 = %s", (session, ))
        results = cursor.fetchall()

        for result in results:
            print(result[0])
    
    elif selection == "2":
        search = input("please enter the follower you are searching for")
        # cursor.execute(f"SELECT User1 FROM followers WHERE User2 = %s; AND User1 LIKE '{search}%';", session)
        cursor.execute("SELECT User1 FROM followers WHERE User2 = %s AND User1 LIKE %s", (session, f"{search}%"))

        friends = cursor.fetchall()
        print("Here are the results:")
        for elem in friends:
            print(elem[0]) #printing all the matching friends

    elif selection == "3":
        select = input("which friend would you like to remove?")
        remove(select, session)



def following():

    # getting number of people following
    cursor.execute("SELECT COUNT(User2) FROM followers WHERE User1 = %s", (session, ))
    num_following = cursor.fetchall()
    print(f"You are following {num_following[0][0]} people ")
    
    #same as followers but user1 and user2 are flipped in all the queries to get the inverse relationship
    print("What would you like to do?")
    print("1. See Following")
    print("2. Search Following")
    print("3. Unfollow")
    print("4. Follow a User")
    selection = input()

    if selection == "1":
        cursor.execute("SELECT User2 FROM Followers WHERE User1 = %s", (session, ))
        results = cursor.fetchall()

        for result in results:
            print(result[0])

    elif selection == "2":
        search = input("please enter who you are searching for")
        # cursor.execute(f"SELECT User2 FROM followers WHERE User1 = %s; AND User1 LIKE '{search}%';", session)
        cursor.execute("SELECT User2 FROM followers WHERE User1 = %s AND User2 LIKE %s", (session, f"{search}%"))

        follows = cursor.fetchall()
        print("Here are the results:")
        for elem in follows:
            print(elem[0]) #printing all the matching friends

    elif selection == "3":
        select = input("who would you like to unfollow?")
        remove(session, select)

    elif selection == "4":
        select = input("who would you like to follow?")
        add(session, select)



def profile_change():
    
    global session

    valid_inputs = ["1","2", "3", "4", "5"]

    badges = ["1. Mercedes-AMG Petronas Formula One Team: MC", "2. Red Bull Racing Honda: RB", "3. Scuderia Ferrari Mission Winnow: FR",
    "4. Alpine F1 Team: AP", "5. McLaren Racing: MC", "6. Scuderia AlphaTauri Honda: AT", "7. Aston Martin Cognizant Formula One Team: AM",
    "8. Alfa Romeo Racing ORLEN: AR", "9. Haas F1 Team: HA", "10. Williams Racing: WI"]

    valid_team_inputs = ["1","2","3","4","5","6","7","8","9", "10"]
    
    

    while True:
    
        print("Which area would you like to change? Please enter the corresponding number")
        print("1. Name")
        print("2. Username")
        print("3. email")
        print("4. Team")
        print("5. Done making changes")

        choice = input()

        while choice not in valid_inputs:
            choice = input("Please enter a valid input: ")
    
        if choice == "1":
            new_name = input("Please enter your new name ")
            cursor.execute("UPDATE Users SET Name = %s WHERE Username = %s", (new_name, session))
            connection.commit()
            continue
        if choice == "2":
            new_username = input("Please enter your new username ")
            cursor.execute("UPDATE Users SET Username = %s WHERE Username = %s", (new_username, session))
            connection.commit()
            session = new_username
            continue
        if choice == "3":
            new_email = input("Please enter your new email ")
            cursor.execute("UPDATE Users SET Email = %s WHERE Username = %s", (new_email, session))
            connection.commit()
            continue
       
        if choice == "4":
            
            while True:
                print("Please select a badge from the list below by entering the relating number: ")

                for team in badges:
                    print(team)
        
                team = input()
                if team in valid_team_inputs:
                    break    
            
            if team == "1":
                badge = "MC"
            elif team == "2":
                badge = "RB"
            elif team == "3":
                badge = "FR"
            elif team == "4":
                badge = "AP"
            elif team == "5":
                badge = "MC"
            elif team == "6":
                badge = "AT"
            elif team == "7":
                badge = "AM"
            elif team == "8":
                bagde = "AR"
            elif team == "9":
                badge = "HA"
            elif team == "10":
                badge = "WI"
            cursor.execute("UPDATE Users SET Badge = %s WHERE Username = %s", (badge, session))
            connection.commit()
            continue
       
        if choice == "5":
            break
    main()    
    

def profile():
    
    valid_inputs = ["1","2"]
    arg = (session, )
    cursor.execute("SELECT Username,Email, Name, Badge FROM Users WHERE Username = %s", arg )

    userInfo = cursor.fetchall()

    username = userInfo[0][0]
    email = userInfo[0][1]
    Name = userInfo[0][2]
    badge = userInfo[0][3]

    print("Name: ",Name)
    print("Username: ", username)
    print("Email ", email)
    print("Team: ", badge)
    
    print("Would you like to make changes to your profile: ")
    print("1. Yes")
    print("2. No")

    choice = input()

    while choice not in valid_inputs:
        choice = input("Please enter a valid input: ")

    if choice == "1":
        profile_change()
    
    main()
    
def logout():
    global session 
    session = ""

    home()




def home():
    print("Welcome to Bormula 0! ")
    print("Select one of the following: \n 1: Login \n 2: Register")
    selection = input()

    if selection == "1":
        # Login 
        print("This is the login page")
        valid = False
        while valid == False:
            valid = login()
        main()

    elif selection == "2":
        # Register 
        print("This is the register function")
        register()
        valid = False
        while not valid:
            valid = login()


home()