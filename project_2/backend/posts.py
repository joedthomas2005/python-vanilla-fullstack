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

db = sqlite3.connect('blogapp.db')
cursor = db.cursor()

def search(query, limit):
    
    queryTerms = urllib.parse.unquote(query).split(" ")
    SQLquery = "SELECT id, title, path FROM posts WHERE title LIKE "

    for i in range(len(queryTerms)):

        if i == len(queryTerms) - 1:
            SQLquery += f"\"%{queryTerms[i]}%\" "
        else:
            SQLquery += f"\"%{queryTerms[i]}%\" OR title LIKE "

    SQLquery += f"OR id=\"{query}\" ORDER BY id DESC LIMIT {limit}"

    print("SQL query: " + SQLquery)
    cursor.execute(SQLquery)

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
    query = f"SELECT id, title, path FROM posts WHERE id = {id}"
    
    cursor.execute(query)

    for record in cursor:
        return record
    

def getRecentPosts(number: int) -> list:
    query = f"SELECT * FROM posts ORDER BY id DESC LIMIT {number}"

    cursor.execute(query)

    return [record for record in cursor]

def getRecent(property, number):

    query = f"SELECT {property} FROM posts ORDER BY id DESC LIMIT {number}"
    cursor.execute(query)
    
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
