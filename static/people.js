function returnJsonWithFavDrink(first_name, last_name, fav_drink) {
    return JSON.stringify({
        "first_name": first_name,
        "last_name": last_name,
        "fav_drink": parseInt(fav_drink, 10)
    });
}

function returnJsonWithoutFavDrink(first_name, last_name, fav_drink) {
    return JSON.stringify({
        first_name: first_name,
        last_name: last_name
    });
}

document.getElementById("submit_btn").addEventListener("click", function(event){
    event.preventDefault();

    let first_name = document.getElementById("first_name").value;
    let last_name = document.getElementById("last_name").value;
    let fav_drink = document.getElementById("fav_drink").value;

    if (first_name !== "" && last_name !== "") {
        const xhr = new XMLHttpRequest();
        //let json;

        //if (fav_drink > 0) {
        //    json = returnJsonWithFavDrink(first_name, last_name, fav_drink); 
        //} else {
        //    json = returnJsonWithoutFavDrink(first_name, last_name);
        //}
        let json = JSON.stringify({
            first_name: "Test",
            last_name: "Person"
        })
        xhr.open("POST", "http://localhost:8000/api/people");
        xhr.setRequestHeader("Content-Type", "apllication/json; charset=utf-8");
        console.log("post now");
        xhr.send(json);
    }
})

