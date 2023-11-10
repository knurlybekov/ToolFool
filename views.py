#COMP 3450: Karan Nurlybekov
import re
from datetime import datetime
import flask_login
import jinja2
from flask_login import login_required
from flask import Blueprint, render_template, request, flash, jsonify, session, send_file, url_for, redirect
import folium
from dbConn import connection, getTools, findTools, sendOrder

views = Blueprint('views', __name__)


# 386ce9d230e54b3bb0f64db8b0da1238


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    numbers = re.findall(r'\d+', str(flask_login.current_user))
    print(int(numbers[0]))
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    map_obj = map_create()
    map_html = map_obj._repr_html_()
    return render_template("home.html", map_html=map_html, current_time=current_time)


def map_create():
    lat = 50.676109
    lon = -120.340836
    zoom = 11

    # dfAreas = getAreas()

    map = folium.Map(location=[lat, lon],
                     zoom_start=zoom, control_scale=True)

    html_to_insert = "<style>.leaflet-popup-content-wrapper, .leaflet-popup.tip {background-color: transparent !important; border-shadow: none !important; }</style>"

    map.get_root().header.add_child(folium.Element(html_to_insert))
    markers = get_markers()
    for marker in markers:
        # print(marker.find_identifier())
        marker.add_to(map)

    map.get_root().width = "100%"
    map.get_root().height = "800px"

    return map

@views.route('sendorder', methods=['post'])
def sendorder():
    if request.method == 'POST':
        print('a')
        numbers = re.findall(r'\d+', str(flask_login.current_user))
        uid = int(numbers[0])
        startTime = request.form.get('startTime')
        endTime = request.form.get('endTime')
        tool_id = request.form.get('tool_id')
        sendOrder(str(startTime), str(endTime), str(tool_id), str(uid))
        return redirect(url_for('/', tool_id=tool_id))
def get_markers():
    params = request.args.get('srch-term')

    # Convert None to an empty string
    params = str(params) if params is not None else ""

    print(params)

    # Get the DataFrame based on the filter criteria
    if params:
        df = findTools(params)
    else:
        df = getTools()
    print(df)
    markers = []
    sendorder = url_for('views.sendorder')
    html_popup_template = """
                <html>
    <!DOCTYPE html>
    <html>
    <!--Bootstrap and JQuery dependency-->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>

        <style>
            #infoDiv{
                width:200px;
                height:500px;
                border:2px solid black;
                z-index: 3;
                border-radius: 30px;
                position: absolute;
                right: 50px;
                top: calc(50% - 250px);
                transition: width 1s;
                background-color: white;
            }

            #imgDisplay{
                width:120px;
                height:120px;
                position: absolute;
                top:20px;
                right: calc(50% - 60px);
                border-radius: 30px;
            }
            #orderForm{
                position:absolute;
                top:60px;
                left:50px;
                display:none;
                transition:visibility 1s;
            }
            #sellerInfo{
                display:none;
                position:absolute;
                top:60px;
                right:70px;
                text-align: center;
            }
            body{
            background-color: transparent;
            }
        </style>

        <div id = "map" class =''> <!--Map container, just used for demonstration-->
            <!--Start of wigit-->
            <div id = "infoDiv">
                <img id = "imgDisplay"> <!--Piece image, needs to be updated based on selection-->

                <!--Piece info-->
                <div style = "text-align: center; width: 100%; top: 160px; position: absolute;">
                    <h3>{{row["tool_name"]}}</h3>
                    <br>
                    <p id="description">{{row["tool_description"]}}</p>
                </div>

                <!--Seller info (displayed on show more-->
                <div id="sellerInfo">
                    <h3 style="margin:0;">{{row["user_fname"]}} {{row["user_lname"]}}</h3>
                    <br><br>
                    <p>Owner Info</p>
                </div>

                <!--Order controls, displayed on show more-->
                <div id = "orderForm">
                    <form class="form-group" method="post" action="{{'sendorder'}}">
    <input type="hidden" id="tool_id" name="tool_id" value="{{ row['tool_id'] }}">

    <!-- Rent from control, value needs to be updated and limited -->
    <label for="startTime">Rent From:</label>
    <input type="datetime-local" class="form-control" name="startTime" id="startTime" value="2023-10-31T12:00"><br>

    <!-- Rent to control, value needs to be updated and limited -->
    <label for="endTime">To:</label>
    <input type="datetime-local" class="form-control" name="endTime" id="endTime" value="2023-10-31T12:00"><br>

    <!-- Deliver/pickup control -->
    <div class="form-check">
        <input type="radio" name="deliver" class="form-check-input" id="deliver_deliver" checked>
        <label class="form-check-label" for="deliver_deliver">Deliver</label>
    </div>
    <div class="form-check">
        <input type="radio" name="deliver" class="form-check-input" id="deliver_pickup">
        <label class="form-check-label" for="deliver_pickup">Pickup</label>
    </div>
    <br><br>

    <!-- Total price display -->
    <h4 id="total">Total: $0.00</h4>
    <input type="submit" class="btn btn-primary" name="submit_button">
</form>

                </div>

                <!--Button to expand/collapse info-->
                <button id="openInfodiv" class = "btn btn-info" style = "position: absolute; width:95px; bottom:30px; right:30px;">Show more</button>
            </div>

            <!--End of wigit-->
        </div>

        <script>
            let CAD = new Intl.NumberFormat('en-US', {style:'currency', currency:'USD'}); //USD number format

            /****************Event Listeners****************/
            //Event listener to expand/collapse info
            $("#openInfodiv").click(showInfoDiv);

            //Changes total price on end-time change
            $("#endTime").change(function(){
                let totTime = document.getElementById('endTime').valueAsNumber - document.getElementById('startTime').valueAsNumber;
                totTime /= 1000*60*60;
                $("#total").text("Total: " + CAD.format(totTime * 7.32));
                //Needs update from database
            });

            //Changes total price on start-time change
            $("#startTime").change(function(){
                let totTime = document.getElementById('endTime').valueAsNumber - document.getElementById('startTime').valueAsNumber;
                totTime /= 1000*60*60;
                $("#total").text("Total: " + CAD.format(totTime * 7.32));
                //Needs update from database
                //Needs to change min value for end-time so not negative time
            });

            //Expands infoDiv and displays more info
            function showInfoDiv(){
                $("#infoDiv").css("width", "calc(100% - 90px)");
                setTimeout(function(){
                    $("#orderForm").show();
                    $("#sellerInfo").show();
                }, 750);
                $("#description").text('{{row["tool_description"]}}'); //Needs to be updated from database

                //Changes event listener to collapseInfoDiv
                $("#openInfodiv").off();
                $(this).text("Show less");
                $("#openInfodiv").click(collapseInfoDiv);
            }

            //Collapses infoDiv and hides more info
            function collapseInfoDiv(){
                $("#infoDiv").css("width", "200px");
                $("#description").text('{{row["tool_description"]}}'); //Needs to be updated from database
                $("#orderForm").hide();
                $("#sellerInfo").hide();

                //Changes event listener to showInfoDiv
                $("#openInfodiv").off();
                $(this).text("Show more");
                $("#openInfodiv").click(showInfoDiv);
            }
        </script>
    <script>
            $(document).ready(function() {
                $("#getDataBtn").click(function() {
                    $.ajax({
                        type: "GET",
                        url: "/get_data",
                        success: function(response) {
                            var data = response.data;
                            $("#dataElement").text(data);
                        }
                    });
                });
            });

            var markerElements = document.querySelectorAll("[name^='marker_']");

    // Loop through the markerElements and alert their names
    markerElements.forEach(function(element) {
        // Get the element's name attribute
        var markerName = element.getAttribute("name");

        // Display the marker name using alert
        alert(markerName);
    });

        </script>
        
    
        
    </html>"""
    for i, row in df.iterrows():
        html_popup = jinja2.Template(html_popup_template).render(row=row, sendorder=sendorder)
        iframe = folium.IFrame(html=html_popup, width=800, height=500)
        popup = folium.Popup(iframe, max_width=2650)
        marker = folium.Marker(location=[row['accouint_lat'], row['accouint_lon']], popup=popup, elemet_id="marker_sss")
        markers.append(marker)
    return markers
