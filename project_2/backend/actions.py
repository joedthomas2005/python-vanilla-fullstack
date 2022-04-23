import http
import json
import posts
import modules.httpFormatter as httpFormatter


def search(params: dict, body: str) -> httpFormatter.httpResponse:
    """
    Requires the parameters "query" and "count". Searches the database for any posts who's titles
    contain any of the words in the query and returns a set of posts up to a maximum set by count.
    """
    try:
        query = params["query"]
        count = int(params["count"])
        databaseEntries = posts.search(query, count)

        items = []
        for i in range(len(databaseEntries)):
            items.append({
                "number": i,
                "query": query,
                "id": databaseEntries[i][0],
                "title": databaseEntries[i][1],
                "body": posts.readPost(databaseEntries[i][2])
            })
        
        return httpFormatter.httpResponse(200,  json.dumps(items).encode())

    except (KeyError, ValueError):

        return httpFormatter.httpResponse(400)
    
    except Exception as e:

        print("Unhandled exception occured: ", e)
        return httpFormatter.httpResponse(500)


def readPost(params: dict, body: str) -> httpFormatter.httpResponse:
    """
    Requires the parameter "id". Gets the contents of the requested post by its ID in the database.
    """
    try:
        postId = int(params["id"])
        
        postData = posts.readPostById(postId)

        if postData:
            return httpFormatter.httpResponse(200, postData.encode())
        return httpFormatter.httpResponse(404)
    
    except (ValueError, KeyError):

        return httpFormatter.httpResponse(400)
    
    except:
        return httpFormatter.httpResponse(500)
        
def new(params: dict, body: str) -> httpFormatter.httpResponse:

    try:
        postJSON = json.loads(body)
    except:
        print("INVALID JSON")
        return httpFormatter.httpResponse(400)
    
    try:
        title = postJSON["postTitle"]
        postBody = postJSON["postBody"]
    except:
        print("Key Error")
        return httpFormatter.httpResponse(400)

    try:    
        postID = posts.createPost(title, postBody)
    except Exception as e:
        print("Could not create post: ", e)
        return httpFormatter.httpResponse(500)
        
    return httpFormatter.httpResponse(201, str(postID).encode())

def delete(params: dict, body: str) -> httpFormatter.httpResponse:
    
    try:
        postID = params["id"]
    except:
        return httpFormatter.httpResponse(400)
    
    try:
        successful = posts.deletePost(postID)
    except:
        return httpFormatter.httpResponse(500)
    
    if successful:
        return httpFormatter.httpResponse(200, "true".encode())

    return httpFormatter.httpResponse(404, params["id"].encode())
