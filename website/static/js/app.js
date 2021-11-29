function myFunction() {



    var sdmDateTime = document.getElementById("dateSelect").value;
    var sdmFName = document.getElementById("fName").value;
    var sdmLName = document.getElementById("lName").value;
    var sdmEmail = document.getElementById("emailAddress").value

    //sdmDateTime = sdmDateTime.replaceAll('/', '-')

    var sdmDate = sdmDateTime.slice(0, 10)
    var sdmTime = sdmDateTime.slice(10, 19)
    var sdmStartTime = moment(sdmTime, "h:mm:ss A").format("HH:mm:ss")
    var sdmDate = moment(sdmDate).format('YYYY-MM-DD');

    console.log(sdmDate, sdmLName, sdmFName, sdmEmail, sdmStartTime)
    window.location = 'https://savvy-booking.herokuapp.com/DBentry?sdmDate=' + sdmDate + '&sdmStartTime=' + sdmStartTime + '&sdmFName=' + sdmFName + '&sdmLName=' + sdmLName + '&sdmEmail=' + sdmEmail;

    // var searchItem = document.getElementById("searchFile").value;
    return;
}