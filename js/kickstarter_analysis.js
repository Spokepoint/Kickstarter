function dotproduct(a, b) {
    var n = 0.0;
    var lim = Math.min(a.length, b.length);
    for (var i = 0; i < lim; i++) {
        n += a[i] * b[i];
    }
    return n;
}

function success_percent(days, amount, category) {
    var x = 0.0
    var i = 0.44
    if (category === 'Art') {
        x = dotproduct([days, amount, i], [-0.017053, -0.000084, 2.184309]);
    } else if (category === 'Comics') {
        x = dotproduct([days, amount, i], [-0.020134, -0.000062, 2.285823]);
    } else if (category === 'Dance') {
        x = dotproduct([days, amount, i], [-0.007381, -0.000088, 3.335226]);
    } else if (category == 'Design') {
        x = dotproduct([days, amount, i], [-0.010435, -0.000026, 0.631187]);
    } else if (category == 'Fashion') {
        x = dotproduct([days, amount, i], [-0.011923, -0.000028, -0.619011]);
    } else if (category == 'Film and Video') {
        x = dotproduct([days, amount, i], [-0.019536, -0.000035, 1.734891]);
    } else if (category == 'Food') {
        x = dotproduct([days, amount, i], [-0.019966, -0.000049, 1.883914]);
    } else if (category == 'Games') {
        x = dotproduct([days, amount, i], [-0.009907, -0.000032, 0.377766]);
    } else if (category == 'Journalism') {
        x = dotproduct([days, amount, i], [-0.003547, -0.000021, -0.220490]);
    } else if (category == 'Music') {
        x = dotproduct([days, amount, i], [-0.016127, -0.000055, 2.494321]);
    } else if (category == 'Photography') {
        x = dotproduct([days, amount, i], [-0.008885, -0.000063, 0.422430]);
    } else if (category == 'Publishing') {
        x = dotproduct([days, amount, i], [-0.016996, -0.000064, 0.541934]);
    } else if (category == 'Technology') {
        x = dotproduct([days, amount, i], [-0.014156, -0.000022, 0.726520]);
    } else {
        x = dotproduct([days, amount, i], [-0.018138, -0.000062, 3.623317]);
    }
    return 1 / (1 + Math.exp(-x))
}

function calculate_percentage() {
    var canvas = document.getElementById("canvas");
    var days = document.getElementById("days").value;
    var amount = document.getElementById("amount").value;
    var category = document.getElementById("category").value;
    var div = document.getElementById("textDiv");
    if (canvas.getContext) {
        var ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        div.textContent = "input a number of days (1-60) and an amount ($1-100,000)";
        ctx.fillStyle = "#0fbdcc";
        probability = success_percent(days, amount, category);
        percent = probability * 100
        //success_percent(projects, days, amount);
        if (percent == 0) {
            div.textContent = "Not enough historical data to compute accurate percentage"
        }
        if (days != 0 && amount != 0 && percent != 0) {
            ctx.fillRect(0, 0, 3 * percent, 10);
            div.textContent = "you have a " + percent.toFixed(2) + "% chance of success.";
        }
    }
}

function ChangePieChart() {
    var object = document.getElementById("pie-chart");
    var category = document.getElementById("chart_category").value;
    if (category === "Film and Video") {
        category = "Film & Video"
    }
    object.data = category + ".svg";
}


//