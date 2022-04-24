const API = "http://127.0.0.1:3001"

function createCard(post) {

    const element = document.createElement("div");
    element.classList.add("card");

    const headerContainer = document.createElement("h2");
    headerContainer.classList.add("cardHeader");

    const bodyContainer = document.createElement("p");
    bodyContainer.classList.add("cardBody");

    const header = document.createTextNode(post.title);
    const body = document.createTextNode(post.body);

    headerContainer.appendChild(header);
    bodyContainer.appendChild(body);

    element.appendChild(headerContainer);
    element.appendChild(bodyContainer);

    document.getElementById("content").appendChild(element);
}

function searchAPI(search, count) {
    document.getElementById("content").innerHTML = "";
    const request = new XMLHttpRequest();
    const url = `${API}/search?query=${search}&count=${count}`;
    request.open("GET", url);
    request.send();

    request.onreadystatechange = function () {
        if (request.readyState === 4) {
            const data = request.responseText;
            const results = JSON.parse(data);
            results.forEach((result) => {
                createCard(result);
            })
        }
    }
}

function load() {
    document.getElementById("searchBar").addEventListener("keyup", (event) => {
        if (event.key === "Enter") {
            const query = document.getElementById("searchBar").value;
            searchAPI(query, 10);
        }
    })

    document.getElementById("searchButton").addEventListener("click", () => {
        const query = document.getElementById("searchBar").value;
        searchAPI(query, 10);
    })
    searchAPI("", 10);
}
window.addEventListener('load', load)
