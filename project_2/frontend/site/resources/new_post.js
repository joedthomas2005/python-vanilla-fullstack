const API = "http://127.0.0.1:3001"

function submitPost() {

    const url = `${API}/posts`
    const title = document.getElementById("titlebox").value;
    const body = document.getElementById("bodybox").value;

    const req = new XMLHttpRequest()
    req.open("POST", url)
    req.setRequestHeader("Content-Type", "application/json")
    req.send(JSON.stringify({
        "postTitle": title,
        "postBody": body
    }))

    req.onreadystatechange = () => {
        if (req.readyState === 4) {
            if (req.status === 201) {
                const element = document.createElement("p");
                element.classList.add("success");
                element.appendChild(document.createTextNode("Post Created!"));
                document.getElementById("content").appendChild(element);
            } else {
                const element = document.createElement("p");
                element.classList.add("failure");
                element.appendChild(document.createTextNode("Sorry, something went wrong..."));
                document.getElementById("content").appendChild(element);
            }
        }
    }
}

function load() {
    document.getElementById("bodybox").addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
            submitPost();
        }
    });
}
window.addEventListener("load", load);