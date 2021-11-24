function myFunction() {



    var tableData = document.getElementById("dataSelect").value;
    var searchItem = document.getElementById("searchFile").value;

    dataQuery = tableData.concat(searchItem);



    fetch(dataQuery).then((response) => {

        return response.json();
        // } catch (err) { alert("The item you are searching for is too broad.  Please narrow your search.") }

    }).catch(function() { alert("The item you are searching for is too broad." + "\n" + "Please enter a more specific the search item.") })

    .then((data) => {





        // var fileTable = document.createElement("file_table");
        var fileTable = new Tabulator("#table-area", {
            height: 940,
            data: data,
            tooltips: function(cell) { return "Click on the path to copy it to the clipboard" },
            initialFilter: [
                { field: "SubFolder1", type: "like", value: "" }
            ],

            // autoColumns: true,
            columns: [
                { title: 'File Name', field: 'FileName', sorter: 'string', formatter: 'textarea', resizable: true, width: 320 },
                { title: 'Full Path', field: 'FullPath', sorter: 'string', formatter: 'textarea', resizable: true, width: 1145, cellClick: function(e, cell) { clickToCopy(cell.getValue()) }, },
                { title: 'Date Modified', field: 'TimeStamp', sorter: 'string', resizable: true, width: 145 },
                { title: 'Size', field: 'FileSize', sorter: 'string', resizable: true, width: 70 },
                { title: 'First Sub Folder', field: 'SubFolder1', visible: false },
                { title: 'Second Sub Folder', field: 'SubFolder2', visible: false },
                { title: 'Third Sub Folder', field: 'SubFolder3', visible: false },
                { title: 'Year', field: 'Year', visible: false },
                { title: 'Month', field: 'Month', visible: false },
            ]

        });

        $("#download-csv").click(function() {
            fileTable.download("csv", "searchdata.csv");
        });

        // var bar = new ProgressBar.Line(progressbar, {
        //     strokeWidth: 4,
        //     easing: 'easeInOut',
        //     duration: 1400,
        //     color: '#3399ff',
        //     trailColor: '#eee',
        //     trailWidth: 1,
        //     svgStyle: { width: '100%', height: '100%' }
        // });
        // bar.animate(1.0); // Number from 0.0 to 1.0


        emptyOutFilter("SubFolder1-dropdown");
        emptyOutFilter("SubFolder2-dropdown");
        emptyOutFilter("SubFolder3-dropdown");
        emptyOutFilter("Year-dropdown");
        emptyOutFilter("Month-dropdown");

        fileTable.clearFilter();

        subfolder1Array = [''];
        subfolder2Array = [''];
        subfolder3Array = [''];
        yearArray = [''];
        monthArray = [''];

        for (i = 0; i < data.length; i++) {

            if (subfolder1Array.indexOf(data[i].SubFolder1) == -1) {
                subfolder1Array = subfolder1Array.concat(data[i].SubFolder1);
            }

        }

        subfolder1Array = remove(subfolder1Array, null);
        subfolder1Array.sort();
        //     // console.log(subfolder1Array);
        var subFolder1Select = document.getElementById("SubFolder1-dropdown");
        for (folder in subfolder1Array) {
            subFolder1Select.add(new Option(subfolder1Array[folder]));
        }

        var subfolder1Menu = d3.select('#SubFolder1-dropdown');
        subfolder1Menu.on("change", function() {
            var subfolder1Item = document.getElementById("SubFolder1-dropdown");
            var subfolder1Selected = subfolder1Item.options[subfolder1Item.selectedIndex].text;

            var subfolder1FilteredData = data.filter(s1 => s1.SubFolder1 === subfolder1Selected);
            emptyOutFilter("SubFolder2-dropdown");
            subfolder2Array = [''];
            emptyOutFilter("SubFolder3-dropdown");
            subfolder3Array = [''];
            emptyOutFilter("Month-dropdown");
            monthArray = [''];


            fileTable.clearFilter();
            fileTable.addFilter("SubFolder1", "like", document.getElementById("SubFolder1-dropdown").value);
            // fileTable.addFilter("SubFolder2", "like", document.getElementById("SubFolder2-dropdown").value);
            // fileTable.addFilter("SubFolder3", "like", document.getElementById("SubFolder3-dropdown").value);
            // fileTable.addFilter("Year", "like", document.getElementById("Year-dropdown").value);
            // fileTable.addFilter("Month", "like", document.getElementById("Month-dropdown").value);


            for (i = 0; i < subfolder1FilteredData.length; i++) {

                if (subfolder2Array.indexOf(subfolder1FilteredData[i].SubFolder2) == -1) {
                    subfolder2Array = subfolder2Array.concat(subfolder1FilteredData[i].SubFolder2);

                }
            }
            subfolder2Array = remove(subfolder2Array, null);
            subfolder2Array.sort();

            var subFolder2Select = document.getElementById("SubFolder2-dropdown");

            for (folder in subfolder2Array) {
                subFolder2Select.add(new Option(subfolder2Array[folder]));
            }

            var subfolder2Menu = d3.select('#SubFolder2-dropdown');
            subfolder2Menu.on("change", function() {

                var subfolder2Item = document.getElementById("SubFolder2-dropdown");
                var subfolder2Selected = subfolder2Item.options[subfolder2Item.selectedIndex].text;
                var subfolder2FilteredData = subfolder1FilteredData.filter(s2 => s2.SubFolder2 === subfolder2Selected);
                // console.log(subfolder2FilteredData)
                emptyOutFilter("SubFolder3-dropdown");
                subfolder3Array = [''];

                fileTable.clearFilter();
                fileTable.addFilter("SubFolder1", "like", document.getElementById("SubFolder1-dropdown").value);
                fileTable.addFilter("SubFolder2", "like", document.getElementById("SubFolder2-dropdown").value);
                // fileTable.addFilter("SubFolder3", "like", document.getElementById("SubFolder3-dropdown").value);
                // fileTable.addFilter("Year", "like", document.getElementById("Year-dropdown").value);
                // fileTable.addFilter("Month", "like", document.getElementById("Month-dropdown").value);


                for (i = 0; i < subfolder2FilteredData.length; i++) {

                    if (subfolder3Array.indexOf(subfolder2FilteredData[i].SubFolder3) == -1) {
                        subfolder3Array = subfolder3Array.concat(subfolder2FilteredData[i].SubFolder3);
                    }

                }
                subfolder3Array = remove(subfolder3Array, null);
                subfolder3Array.sort();
                var subFolder3Select = document.getElementById("SubFolder3-dropdown");
                for (folder in subfolder3Array) {
                    subFolder3Select.add(new Option(subfolder3Array[folder]));
                }
                var subfolder3Menu = d3.select('#SubFolder3-dropdown');

                subfolder3Menu.on("change", function() {
                    var subfolder3Item = document.getElementById("SubFolder3-dropdown");
                    fileTable.clearFilter();
                    fileTable.addFilter("SubFolder1", "like", document.getElementById("SubFolder1-dropdown").value);
                    fileTable.addFilter("SubFolder2", "like", document.getElementById("SubFolder2-dropdown").value);
                    fileTable.addFilter("SubFolder3", "like", document.getElementById("SubFolder3-dropdown").value);
                    // fileTable.addFilter("Year", "like", document.getElementById("Year-dropdown").value);
                    // fileTable.addFilter("Month", "like", document.getElementById("Month-dropdown").value);
                })
            });
        });

        for (i = 0; i < data.length; i++) {

            if (yearArray.indexOf(data[i].Year) == -1) {
                yearArray = yearArray.concat(data[i].Year);
            }

        }
        yearArray.sort();

        var yearSelect = document.getElementById("Year-dropdown");
        for (folder in yearArray) {
            yearSelect.add(new Option(yearArray[folder]));
        }
        var yearMenu = d3.select('#Year-dropdown');
        yearMenu.on("change", function() {
            var yearItem = document.getElementById("Year-dropdown");
            var yearSelected = yearItem.options[yearItem.selectedIndex].text;

            var yearFilteredData = data.filter(yr => yr.Year === yearSelected);


            emptyOutFilter("Month-dropdown");
            monthArray = [''];
            emptyOutFilter("SubFolder2-dropdown");
            subfolder2Array = [''];
            emptyOutFilter("SubFolder3-dropdown");
            subfolder3Array = [''];

            fileTable.clearFilter();
            // fileTable.addFilter("SubFolder1", "like", document.getElementById("SubFolder1-dropdown").value);
            // fileTable.addFilter("SubFolder2", "like", document.getElementById("SubFolder2-dropdown").value);
            // fileTable.addFilter("SubFolder3", "like", document.getElementById("SubFolder3-dropdown").value);
            fileTable.addFilter("Year", "like", document.getElementById("Year-dropdown").value);
            // fileTable.addFilter("Month", "like", document.getElementById("Month-dropdown").value);


            for (i = 0; i < yearFilteredData.length; i++) {

                if (monthArray.indexOf(yearFilteredData[i].Month) == -1) {
                    monthArray = monthArray.concat(yearFilteredData[i].Month);
                }
            }
            monthArray.sort();
            var monthSelect = document.getElementById("Month-dropdown");
            for (folder in monthArray) {
                monthSelect.add(new Option(monthArray[folder]));
            }
            var monthMenu = d3.select('#Month-dropdown');
            monthMenu.on("change", function() {
                // var monthItem = document.getElementById("Month-dropdown");
                fileTable.clearFilter();
                // fileTable.addFilter("SubFolder1", "like", document.getElementById("SubFolder1-dropdown").value);
                // fileTable.addFilter("SubFolder2", "like", document.getElementById("SubFolder2-dropdown").value);
                // fileTable.addFilter("SubFolder3", "like", document.getElementById("SubFolder3-dropdown").value);
                fileTable.addFilter("Year", "like", document.getElementById("Year-dropdown").value);
                fileTable.addFilter("Month", "like", document.getElementById("Month-dropdown").value);
            });

        });





    });

};