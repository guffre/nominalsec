// This function will retrieve the most recent passwords added to the database file
// It will then update the div with id "latest-attempts-box"
// Default of 6000 "GET"s, which is a little over 8 hours of live updates
function get_latest(count=6000){
    var latest_attempts = $.ajax({
        type: "GET",
        dataType: "html",
        url: "latest.php",
        async: false,
        complete: function(){ 
            if (count > 0) {
                setTimeout(function(){ get_latest(count-1);}, 5000); }
            }
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

// Retrieves the counts of login attempts against the server
function get_attempts(){
    var attempts = $.ajax({
        type: "GET",
        dataType: "json",
        url: "attempts.php",
        async: false
    }).responseText;
    return attempts;
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

// Uses Plotly to create a line graph displaying login attempt counts
function make_attempt_chart() {
    var data = jQuery.parseJSON(get_attempts());
    var xval = data["dates"];
    var yval = data["values"];
    var trace1 = {
        x: xval,
        y: yval,
        type: 'bar',
        text: yval.map(String),
        textposition: 'auto',
        hoverinfo: 'none',
        marker: {
            color: 'darkslategray',
            opacity: 0.6,
            line: {
                color: 'white',
                width: 1.5
            }
        }
    };
    var data = [trace1];
    var layout = {
        margin: { l: "50", r:"20", t:"10", b:"35"},
        paper_bgcolor: "#313131",
        plot_bgcolor: "#313131",
        xaxis: { color: "white" },
        yaxis: { color: "white" }
    };
    Plotly.newPlot('attempt-box-inner', data, layout);
};

// Use Plotly to create a pie chart displaying top ten passwords
function make_top_ten_chart() {
    var data = jQuery.parseJSON(get_top_ten());
    var trace = [{
        type: "pie",
        values: data["values"],
        labels: data["words"],
        textinfo: "label",
        insidetextorientation: "radial"
    }]
      
    var layout = {
        margin: { l: "20", r:"20", t:"20", b:"20"},
        height: 320,
        width: 500,
        paper_bgcolor: "#313131",
        plot_bgcolor: "#313131",
        font: {
            color: "white"
        }
    }
    Plotly.newPlot('chart-box-inner', trace, layout)
}

// Make the DIV elements draggable
$(document).ready(function() {
    dragElement(document.getElementById("stats-box"));
    dragElement(document.getElementById("latest-attempts-box"));
    dragElement(document.getElementById("chart-box"));
    dragElement(document.getElementById("policy-box"));
    dragElement(document.getElementById("password-box"));
    dragElement(document.getElementById("attempt-box"));

    new get_latest();
    new get_stats();
    new make_attempt_chart();
    new make_top_ten_chart();
});

// Draggable functionality, retrieved from W3Schools
function dragElement(elmnt) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    elmnt.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // Snap to grid
        var top = Math.floor((elmnt.offsetTop - pos2)/10)*10;
        var left = Math.floor((elmnt.offsetLeft - pos1)/10)*10;
        // set the element's new position
        elmnt.style.top = top + "px";
        elmnt.style.left = left + "px";


        // stop moving when mouse button is released
        document.onmouseup = null;
        document.onmousemove = null;
        document.getElementById("testbutton").focus();
    }
}