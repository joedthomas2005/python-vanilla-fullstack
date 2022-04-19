import mysql.connector

credFile = open("sqlcreds.creds", "r")
fileData = credFile.readlines()
credFile.close()
user = fileData[0].strip("\n")
password = fileData[1].strip("\n")

db = mysql.connector.connect(
    host = "localhost",
    user = user,
    password = password,
    database = "blogapp"
)

cursor = db.cursor()

def search(query, limit):
    query = f"""SELECT id, title, path FROM posts WHERE title LIKE \"%{query}%\" 
    OR id=\"{query}\" ORDER BY id DESC LIMIT {limit}"""
    cursor.execute(query)

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
