let API = "http://127.0.0.1:3001"

function load() {

    document.getElementById("searchBar").addEventListener("keyup", (event) => {
        if (event.key == "Enter") {
            let query = document.getElementById("searchBar").value;
            console.log(`search query ${query}`);
            searchAPI(query, 10);
        }
    })

    document.getElementById("searchButton").addEventListener("click", () => {
        let query = document.getElementById("searchBar").value;
        console.log(`search query ${query}`);
        searchAPI(query, 10);
    })

    searchAPI("", 10);
}

function searchAPI(search, count) {
    document.getElementById("content").innerHTML = "";
    let request = new XMLHttpRequest();
    let url = `${API}/search?query=${search}&count=${count}`;
    request.open("GET", url);
    request.send();

    let results = [];
    request.onreadystatechange = function () {
        if (request.readyState == 4) {
            let data = request.responseText;
            console.log(data);
            results = JSON.parse(data);
            results.forEach((result) => {
                console.log(result);
                createCard(result);
            })
        }
    }
}

function createCard(post) {

    element = document.createElement("div");
    element.classList.add("card");

    headerContainer = document.createElement("h2");
    headerContainer.classList.add("cardHeader");

    bodyContainer = document.createElement("p");
    bodyContainer.classList.add("cardBody");

    header = document.createTextNode(post.title);
    body = document.createTextNode(post.body);
    headerContainer.appendChild(header);
    bodyContainer.appendChild(body);

    element.appendChild(headerContainer);
    element.appendChild(bodyContainer);

    document.getElementById("content").appendChild(element);
}