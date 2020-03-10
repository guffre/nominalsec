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
    $('div#latest-attempts-box').html(latest_attempts);
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
    $('div#stats-box').html(stats);
};

// todo: Submit value for testing with libcrack
function clickTest(){
    var test = document.getElementById("testbutton").value;
    console.log(test);
  };

// This script block draws a pie chart with the top-ten most common passwords displayed
$(document).ready(function(){
    new get_latest();
    new get_stats();

    google.charts.load("current", {packages:["imagepiechart"]});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        // ['Task', 'Hours per Day'],['Work',        11],['Sleep',       7]]
        var data = google.visualization.arrayToDataTable(jQuery.parseJSON(get_top_ten())["data"]);
        var chart = new google.visualization.ImagePieChart(document.getElementById('chart_div'));
        chart.draw(data, {width: 430, height: 240, title: 'Top Ten Passwords'});
    };
});