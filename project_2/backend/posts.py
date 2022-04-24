import sqlite3
import urllib.parse
import os

SQLITEDB = 'blogapp.db'

db = sqlite3.connect(SQLITEDB)
cursor = db.cursor()

def search(query: str, limit: int) -> list:
    
    queryTerms = urllib.parse.unquote(query).split(" ")
    
    queryTerms = [f"%{queryTerm}%" for queryTerm in queryTerms]
    
    SQLquery = "SELECT id, title, path FROM posts WHERE title LIKE "

    for i in range(len(queryTerms)):

        if i == len(queryTerms) - 1:
            SQLquery += "? "
        else:
            SQLquery += "? OR title LIKE "

    SQLquery += "OR id=? ORDER BY id DESC LIMIT ?"

    print("SQL query: " + SQLquery)
    print("Parameters: ", queryTerms + [query] + [limit])
    cursor.execute(SQLquery, queryTerms + [query] + [limit])

    return list(cursor)

def readPostById(postID: int) -> str:
    
    path = getPath(postID)
    return readPost(path)

def readPost(path: str) -> str:
    try:

        with open(path, "r") as post:
            data = post.read()
        return data

    except:
        return ""

def getPostRecord(postID: int) -> tuple:

    query = "SELECT id, title, path FROM posts WHERE id = ?"    
    cursor.execute(query, (postID,))

    for record in cursor:
        return record
    

def getRecentPosts(number: int) -> list:

    query = "SELECT * FROM posts ORDER BY id DESC LIMIT ?"
    cursor.execute(query, (number,))

    return list(cursor)

def getRecent(column: str, number:int = 1) -> list:

    query = f"SELECT {column} FROM posts ORDER BY id DESC LIMIT ?"
    cursor.execute(query, (number,))
    
    return list(cursor)

def getPath(postID: int) -> str:
    record = getPostRecord(postID)
    if record:
        return record[2]
    return ""

def getTitle(postID: int) -> str:
    record = getPostRecord(postID)
    if record:
        return record[1]
    return ""

def getPostData(postID: int) -> str:
    return readPost(getPath(postID))

def createPost(title: str, body: str) -> int:
    recentEntries = getRecent("id")
    if len(recentEntries) > 0:
        postID = int(recentEntries[0][0]) + 1
    else:
        postID = 1
        
    print("ID: ", postID)
    print("TITLE: ", title)
    path = f"posts/{postID}.txt"
    print("PATH: ", path)
    print("BODY: ", body)

    with open(path, 'w') as file:
        file.write(body)

    cursor.execute("INSERT INTO posts (id, title, path) VALUES (?, ?, ?)", (postID, title, path))
    db.commit()
    
    return postID

def deletePost(postID: int) -> bool:
    record = getPostRecord(postID)
    if record:
        
        path = record[2]
        os.remove(path)
        query = "DELETE FROM posts WHERE id=?"
        cursor.execute(query, (postID,))
        db.commit()
        return True
    return False
