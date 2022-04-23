window.addEventListener("load", load);
let API = "http://127.0.0.1:3001"

function load() {
    document.getElementById("bodybox").addEventListener("keyup", (event) => {
        if(event.key == "Enter"){
            submitPost();
        }
    });
}

function submitPost(){

    let url = `${API}/posts`
    let title = document.getElementById("titlebox").value;
    let body = document.getElementById("bodybox").value;

    let req = new XMLHttpRequest()
    req.open("POST", url)
    req.setRequestHeader("Content-Type", "application/json")
    req.send(JSON.stringify({
        "postTitle": title,
        "postBody": body
    }))

    req.onreadystatechange = ()=>{
        if(req.readyState == 4){
            if(req.status == 201){
                alert("Post Made!");
            }
            else{
                alert("Sorry, something went wrong...");
            }
        }
    }

}