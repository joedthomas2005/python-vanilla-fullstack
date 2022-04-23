#import mysql.connector
import sqlite3
import urllib.parse
# credFile = open("sqlcreds.creds", "r")
# fileData = credFile.readlines()
# credFile.close()
# user = fileData[0].strip("\n")
# password = fileData[1].strip("\n")

# db = mysql.connector.connect(
#     host = "localhost",
#     user = user,
#     password = password,
#     database = "blogapp"
# )

# cursor = db.cursor()
sqliteDB = 'blogapp.db'

db = sqlite3.connect(sqliteDB)
cursor = db.cursor()

def search(query, limit):
    
    queryTerms = urllib.parse.unquote(query).split(" ")
    for i in range(len(queryTerms)):
        queryTerms[i] = f"%{queryTerms[i]}%"
    
    SQLquery = "SELECT id, title, path FROM posts WHERE title LIKE "

    for i in range(len(queryTerms)):

        if i == len(queryTerms) - 1:
            SQLquery += "? "
        else:
            SQLquery += f"? OR title LIKE "

    SQLquery += f"OR id=? ORDER BY id DESC LIMIT ?"

    print("SQL query: " + SQLquery)
    print("Parameters: ", queryTerms + [query] + [limit])
    cursor.execute(SQLquery, queryTerms + [query] + [limit])

    results = [result for result in cursor]
    return results

def readPostById(id):
    
    path = getPath(id)
    return readPost(path)

def readPost(path):
    try:
        post = open(path, "r")
    except:
        return ""
    data = post.read()
    post.close()
    return data

def getPostRecord(id):
    query = "SELECT id, title, path FROM posts WHERE id = ?"
    
    cursor.execute(query, (id))

    for record in cursor:
        return record
    

def getRecentPosts(number: int) -> list:
    query = "SELECT * FROM posts ORDER BY id DESC LIMIT ?"

    cursor.execute(query, (number,))

    return [record for record in cursor]

def getRecent(property, number = 1):

    query = f"SELECT {property} FROM posts ORDER BY id DESC LIMIT ?"
    cursor.execute(query, (number,))
    
    return [record for record in cursor]

def getPath(id):
    if(getPostRecord(id)):
        return getPostRecord(id)[2]
    return ""

def getTitle(id):
    if(getPostRecord(id)):
        return getPostRecord(id)[1]
    return ""

def getPostData(id):

    return readPost(getPath(id))

for post in getRecentPosts(10):
    print(post)

def createPost(title, body):
    recentEntries = getRecent("id")
    if(len(recentEntries) > 0):
        postID = int(getRecent("id")[0][0]) + 1
    else:
        postID = 1
        
    print("ID: ", postID)
    print("TITLE: ", title)
    path = f"posts/{postID}.txt"
    print("PATH: ", path)
    print("BODY: ", body)
    file = open(path, 'w')
    file.write(body)
    file.close()

    cursor.execute("INSERT INTO posts (id, title, path) VALUES (?, ?, ?)", (postID, title, path))
    db.commit()

