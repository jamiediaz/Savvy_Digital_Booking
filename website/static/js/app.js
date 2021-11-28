function myFunction() {



    var sdmDate = document.getElementById("dateSelect").value;
    var sdmName = document.getElementById("fullName").value;
    var sdmEmail = document.getElementById("emailAddress").value
    var sdmDateISO = Date(sdmDate);

    sdmDateISO = sdmDateISO.toISOString();

    console.log(sdmDateISO, sdmName, sdmEmail)


    // var searchItem = document.getElementById("searchFile").value;
    return;
}