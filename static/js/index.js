
function get_latest() {
    var latest_attempts = $.ajax({
        type: "GET",
        dataType: "html",
        url: "latest.php",
    }).complete(function () {
        setTimeout(function () { get_latest(); }, 2000);
    }).responseText;
    $('div.latest-attempts-box').html(latest_attempts);
};

function get_top_ten() {
    var top_ten = $.ajax({
        type: "GET",
        dataType: "json",
        url: "top_ten.php",
        async: false
    }).responseText;
};

function get_stats() {
    var stats = $.ajax({
        type: "GET",
        dataType: "html",
        url: "stats.php",
    }).responseText;
    $('div.stats-box').html(stats);
};
