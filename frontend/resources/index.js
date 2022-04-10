function additems(){

    for(let i = 0; i < 100; i++){
        let requestHandler = new XMLHttpRequest();
        let url = "http://127.0.0.1:3000/words/"+i;
        requestHandler.open("GET", url);
        requestHandler.send()

        requestHandler.onreadystatechange = function(){
            if(requestHandler.readyState == 4){
                let word = requestHandler.responseText;
                console.log(word);
            }
        }
    }
}