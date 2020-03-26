// This function will retrieve the most recent passwords added to the database file
// It will then update the div with id "latest-attempts-box"
function get_latest(){
    var latest_attempts = $.ajax({
        type: "GET",
        dataType: "html",
        url: "latest.php",
        async: false,
        complete: function(){ setTimeout(function(){get_latest();}, 5000); }
    }).responseText;
    $('div#latest-attempts-box-inner').html(latest_attempts);
};

// This function gets the top ten most common seen passwords from the database file
// It will return this data as a string
function get_top_ten(){
    var top_ten = $.ajax({
        type: "GET",
        dataType: "json",
        url: "top_ten.php",
        async: false
    }).responseText;
    return top_ten;
};

// This function will retrieve various statistics about the password collection
// It will then update the div with id "stats-box"
function get_stats(){
    var stats = $.ajax({
        type: "GET",
        dataType: "html",
        url: "stats.php",
        async: false
    }).responseText;
    $('div#stats-box-inner').html(stats);
};

// Submits a password for testing against libcrack
function check_password(){
    var check = document.getElementById("testbutton").value;
    console.log(check);
    var result = $.ajax({
        type: "GET",
        dataType: "html",
        url: "check_password.php?check=" + check,
        async: false
    }).responseText;
    $('div#password-result-box').html(result);
};

// Gets the result of running a password policy update
function update_password_policy(){
    var result = $.ajax({
        type: "GET",
        dataType: "html",
        url: "update_password_policy.php",
        async: false
    }).responseText;
    $('div#policy-result-box').html(result);
};

// This script block draws a pie chart with the top-ten most common passwords displayed
$(document).ready(function(){
    new get_latest();
    new get_stats();

    google.charts.load("current", {packages:["imagepiechart"]});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        // ['Task', 'Hours per Day'],['Work',        11],['Sleep',       7]]
        var chart = new google.visualization.ImagePieChart(document.getElementById('chart-box-inner'));
        var data = google.visualization.arrayToDataTable(jQuery.parseJSON(get_top_ten())["data"]);
        var options = {
            width: 430,
            height: 240,
            backgroundColor: '#313131',
            legend: {
                textStyle: { color: 'white',
                            bold: true
                }
            }
        }
        chart.draw(data,options );
    };
});

// Make the DIV element draggable:
$(document).ready(function() {
    dragElement(document.getElementById("stats-box"));
    dragElement(document.getElementById("latest-attempts-box"));
    dragElement(document.getElementById("chart-box"));
    dragElement(document.getElementById("policy-box"));
    dragElement(document.getElementById("password-box"));
});

function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    elmnt.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        // stop moving when mouse button is released:
        document.onmouseup = null;
        document.onmousemove = null;
        document.getElementById("testbutton").focus();
    }
}