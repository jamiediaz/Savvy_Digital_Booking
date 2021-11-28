function myFunction() {



    var sdmDate = document.getElementById("dateSelect").value;
    var sdmName = document.getElementById("fullName").value;
    var sdmEmail = document.getElementById("emailAddress").value
    sdmDateISO = sdmDate.toISOString()

    console.log(sdmDateISO, sdmName, sdmEmail)


    // var searchItem = document.getElementById("searchFile").value;
    return;
}