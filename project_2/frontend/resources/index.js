function load(){
    document.getElementById("search").addEventListener("keyup", (event) =>{
        if(event.key == "Enter"){
            console.log(`search query ${document.getElementById("search").value}`)
        }
    })
}