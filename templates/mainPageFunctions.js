
        /***********Filter Code***********/
        const brandArray = ["Makita", "Dewalt", "Craftsman"]; //Hard coded in brands, need to be updated by controller or AJAX
        populateBrands(brandArray);

        //Populates brand holder with brands
        function populateBrands(brandArray) {
            let brandString = "";
            //Iterates, adding a label and checkbox for each brand
            for (let brand in brandArray) {
                brandString += "<label for = '" + brandArray[brand] + "' class = 'form-check-label'>" + brandArray[brand] + "</label>";
                brandString += "<input type = 'checkbox' name = '" + brandArray[brand] + "' class = 'form-check-input'><br>";
            }

            $("#brands").html(brandString);
        }

        //Event listener for updating price slider
        $("#priceRange").on('input change', function(){
            var val = $(this).val();
            let USD = new Intl.NumberFormat('en-US', {style:'currency', currency:'USD'}); //USD number format
            $("#priceLabel").text("" + USD.format(val));
        });

        $("#filterButton").click(showModal);

        function showModal(){
            $("#modal").show();
            $("#filterButton").click(hideModal);
        }

        function hideModal(){
            $("#modal").hide();
            $("#filterButton").click(showModal);
        }

        //Need to do:
        //Filter choices based on database, not hardcoded (AJAX)
        //Join into map


        /***********Info Code***********/
        let CAD = new Intl.NumberFormat('en-US', {style:'currency', currency:'USD'}); //USD number format

        /****************Event Listeners****************/
        //Event listener to expand/collapse info
        $("#openInfodiv").click(showInfoDiv);

        //Changes total price on end-time change
        $("#endTime").change(function(){
            let totTime = document.getElementById('endTime').valueAsNumber - document.getElementById('startTime').valueAsNumber;
            totTime /= 1000*60*60;
            $("#total").text("Total: $" + CAD.format(totTime * 7.32));
            //Needs update from database
        });

        //Changes total price on start-time change
        $("#startTime").change(function(){
            let totTime = document.getElementById('endTime').valueAsNumber - document.getElementById('startTime').valueAsNumber;
            totTime /= 1000*60*60;
            $("#total").text("Total: $" + CAD.format(totTime * 7.32));
            //Needs update from database
            //Needs to change min value for end-time so not negative time
        });

        //Expands infoDiv and displays more info
        function showInfoDiv(){
            $("#infoDiv").css("width", "calc(100% - 200px)");
            setTimeout(function(){
                $("#orderForm").show();
                $("#sellerInfo").show();
            }, 750);
            $("#description").text('Long Description'); //Needs to be updated from database

            //Changes event listener to collapseInfoDiv
            $("#openInfodiv").off();
            $(this).text("Show less");
            $("#openInfodiv").click(collapseInfoDiv);
        }

        //Collapses infoDiv and hides more info
        function collapseInfoDiv(){
            $("#infoDiv").css("width", "200px");
            $("#description").text('Short Description'); //Needs to be updated from database
            $("#orderForm").hide();
            $("#sellerInfo").hide();

            //Changes event listener to showInfoDiv
            $("#openInfodiv").off();
            $(this).text("Show more");
            $("#openInfodiv").click(showInfoDiv);
        }