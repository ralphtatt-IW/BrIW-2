document.getElementById("drinks_link").classList.add("nav-active");

function postDrinkJson(drink_name, drink_instructions) {
    if (drink_name !== "") {
        const xhr = new XMLHttpRequest();
        let json = JSON.stringify({
            name: drink_name,
            instructions: drink_instructions
        });
        console.log(`built json: ${json}`);
        
        xhr.addEventListener("load", function() {
            if (xhr.status == 201) {
                alert(`${drink_name} has been added`);
                location.reload();
            } else {
                alert(`Status Code: ${xhr.status}. Error: ${xhr.statusText}`);
            }
        })
        
        xhr.open("POST", "http://localhost:8000/api/drinks");
        xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");        
        xhr.send(json);
    }
}

document.getElementById("submit_btn").addEventListener("click", function(event){
    event.preventDefault();
    let name = document.getElementById("name");
    let instructions = document.getElementById("instructions");

    postDrinkJson(name.value, instructions.value);

    //reset form now drink added posted
    name.value = "";
    instructions.value = "";
})

