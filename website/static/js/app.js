function myFunction() {



    var sdmDate = document.getElementById("dateSelect").value;
    var sdmName = document.getElementById("fullName").value;
    var sdmEmail = document.getElementById("emailAddress").value
    console.log(sdmDate, sdmName, sdmEmail)


    // var searchItem = document.getElementById("searchFile").value;
    return;
}

function getDates() {

    dataQuery = "https://savvy-booking.herokuapp.com/api/v1.0/calendar"

    fetch(dataQuery).then((response) => {

        console.log(response.json);
        return response.json();

    })