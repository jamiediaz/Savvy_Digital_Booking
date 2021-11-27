function getDates() {

    dataQuery = "https://savvy-booking.herokuapp.com/api/v1.0/calendar";

    fetch(dataQuery).then((response) => {

        console.log(response.json());
        return response.json();

    });
}