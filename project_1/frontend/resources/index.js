function additems(){

    let elements = new Array(10).fill("");
    let elementCount = 0

    for(let i = 0; i < 10; i++){
        let requestHandler = new XMLHttpRequest();
        let url = `http://127.0.0.1:3000/words/${i}`;
        requestHandler.open("GET", url);
        requestHandler.send()

        requestHandler.onreadystatechange = function(){
            if(requestHandler.readyState == 4){
                data = requestHandler.responseText;
                elements[i] = data;
                elementCount++;
            }
        }
    }   

    let funcId = setInterval(function(){
        if(elementCount == 10){
            console.log("Done loading elements");

            elements.forEach(element =>{
                let domElement = document.createElement("p");
                let textNode = document.createTextNode(element);
                domElement.appendChild(textNode);
                document.getElementById("items").appendChild(domElement);
                clearInterval(funcId);

            })
        }
    }, 10)
}

