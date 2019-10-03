document.getElementById("people_link").classList.add("nav-active");

function returnJsonWithFavDrink(person_first_name, person_last_name, person_fav_drink) {
    return JSON.stringify({
        first_name: person_first_name,
        last_name: person_last_name,
        fav_drink: parseInt(person_fav_drink, 10)
    });
}

function returnJsonWithoutFavDrink(person_first_name, person_last_name) {
    return JSON.stringify({
        first_name: person_first_name,
        last_name: person_last_name
    });
}

function postPersonJson(first_name, last_name, fav_drink) {
    if (first_name.value !== "" && last_name.value !== "") {
        const xhr = new XMLHttpRequest();
        let json;
        
        if (parseInt(fav_drink.value, 10) > 0) {
            json = returnJsonWithFavDrink(first_name.value, last_name.value, fav_drink.value); 
        } else {
            json = returnJsonWithoutFavDrink(first_name.value, last_name.value);
        }
        
        xhr.addEventListener("load", function() {
            if (xhr.status == 201) {
                alert(`${first_name.value} ${last_name.value} has been added`);
                location.reload();
            } else {
                alert(`Status Code: ${xhr.status}. Error: ${xhr.statusText}`);
            }
        })

        xhr.open("POST", "http://localhost:8000/api/people");
        xhr.setRequestHeader("Content-Type", "application/json; charset=utf-8");
        xhr.send(json);
    }
}

document.getElementById("submit_btn").addEventListener("click", function(event){
    event.preventDefault();

    let first_name = document.getElementById("first_name");
    let last_name = document.getElementById("last_name");
    let fav_drink = document.getElementById("fav_drink");
    postPersonJson(first_name, last_name, fav_drink);

    //reset form now person posted
    first_name.value = "";
    last_name.value = "";
    fav_drink.value = -1;

})

