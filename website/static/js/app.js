function myFunction() {



    var sdmDateTime = document.getElementById("dateSelect").value;
    var sdmFName = document.getElementById("fName").value;
    var sdmLName = document.getElementById("lName").value;
    var sdmEmail = document.getElementById("emailAddress").value

    sdmDateTime = sdmDateTime.replaceAll('/', '-')

    var sdmDate = sdmDateTime.slice(0, 10)
    var sdmTime = sdmDateTime.slice(10, 19)
    sdmTIme = moment(sdmTime, ["h:mm A"]).format("HH:mm");

    console.log(sdmDate, sdmLName, sdmFName, sdmEmail, sdmTime)
        // window.location = 'https://savvy-booking.herokuapp.com/v1.0/DBentry/' + sdmDate + sdmName + sdmEmail;

    // var searchItem = document.getElementById("searchFile").value;
    return;
}