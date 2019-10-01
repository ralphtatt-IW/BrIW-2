document.getElementById("submit-btn").addEventListener("click", function(event){
    event.preventDefault();

    const person_name = document.getElementById("person-name");
    const drink_name = document.getElementById("drink-name");
    const form = document.getElementById("add-person-form");

    if (person_name.value !== "" || drink_name.value !== "") {
      form.submit();
    }
});