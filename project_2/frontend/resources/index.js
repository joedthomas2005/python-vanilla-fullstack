function load(){
    document.getElementById("searchBar").addEventListener("keyup", (event) =>{
        if(event.key == "Enter"){
            let query = document.getElementById("searchBar").value;
            console.log(`search query ${query}`);
            queryBackend(query, 10);
        }
    })

    document.getElementById("searchButton").addEventListener("click", () =>{
        let query = document.getElementById("searchBar").value;
        console.log(`search query ${query}`);
        queryBackend(query, 10);
    })
}

function queryBackend(search, count){
    let request = new XMLHttpRequest();
    let url = `http://127.0.0.1:3000/search?query=${search}&count=${count}`;
    request.open("GET", url);
    request.send();

    let results = [];
    request.onreadystatechange = function(){
        if(request.readyState == 4){
            let data = request.responseText;
            console.log(data);
            results = JSON.parse(data);
             results.forEach((result) => {
                 console.log(result);
             })
        }
    }
}