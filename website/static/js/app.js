function myFunction() {



    var sdmDate = document.getElementById("dateSelect").value;
    var sdmName = document.getElementById("fullName").value;
    var sdmEmail = document.getElementById("emailAddress").value

    sdmDate = sdmDate.replace('/', '-')


    console.log(sdmDate, sdmName, sdmEmail)
        // window.location = 'https://savvy-booking.herokuapp.com/v1.0/DBentry/' + sdmDate + sdmName + sdmEmail;

    // var searchItem = document.getElementById("searchFile").value;
    return;
}