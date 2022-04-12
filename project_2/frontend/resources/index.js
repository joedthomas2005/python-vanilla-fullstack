function load(){
    document.getElementById("search").addEventListener("keyup", (event) =>{
        if(event.key == "Enter"){
            let query = document.getElementById("search").value;
            console.log(`search query ${query}`);
            queryBackend(query, 1);
        }
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
            results = JSON.parse(data);
            results.forEach((result) => {
                console.log(result);
            })
        }
    }
}