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
    if (category === 'category') {
        x = dotproduct([days, amount, i], [-0.016001, -0.000044, 1.643558]);
    } else if (category === 'Art') {
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
        x = dotproduct([days, amount, i], [-0.016003, -0.000058, 2.517292]);
    } else if (category == 'Photography') {
        x = dotproduct([days, amount, i], [-0.008850, -0.000067, 0.456913]);
    } else if (category == 'Publishing') {
        x = dotproduct([days, amount, i], [-0.016993, -0.000070, 0.602225]);
    } else if (category == 'Technology') {
        x = dotproduct([days, amount, i], [-0.015348, -0.000009, 0.426567]);
    } else {
        x = dotproduct([days, amount, i], [-0.018138, -0.000062, 3.623234]);
    }
    return 1 / (1 + Math.exp(-x))
}

function ChangePieChart() {
    var object = document.getElementById("pie-chart");
    var category = document.getElementById("chart_category").value;
    if (category === "Film and Video") {
        category = "Film & Video"
    }
    object.data = "Charts/" + category + ".svg";
}

function suggest(category, duration, goal, avg_goal, avg_length, short_goal) {
    if (duration < 10) {
        if (goal > short_goal) {
            return "WARNING: this estimate is extrapolated, for under 10 days the highest goal of a success project was " + short_goal + ". We suggest picking a more realistic duration/goal combination!";
        }
    }
    if (goal > avg_goal) {
        return "The average goal for this category is " + avg_goal + "! keep that in mind.";
    }
    return "Good luck!"
}


function form_suggestions(category, duration, goal) {
    var s = document.getElementById("suggestions")
    switch (category) {
        case 'Art':
            s.textContent = suggest(category, duration, goal, 10000, 30, 12000);
            break;
        case 'Comics':
            s.textContent = suggest(category, duration, goal, 1000, 30, 2000);
            break;
        case 'Dance':
            s.textContent = suggest(category, duration, goal, 1000, 30, 8000);
            break;
        case 'Design':
            s.textContent = suggest(category, duration, goal, 10, 30, 5000);
            break;
        case 'Fashion':
            s.textContent = suggest(category, duration, goal, 10000, 30, 10000);
            break;
        case 'Film and Video':
            s.textContent = suggest(category, duration, goal, 100, 30, 50000);
            break;
        case 'Food':
            s.textContent = suggest(category, duration, goal, 10000, 30, 10000);
            break;
        case 'Games':
            s.textContent = suggest(category, duration, goal, 1000, 30, 125000);
            break;
        case 'Journalism':
            s.textContent = suggest(category, duration, goal, 1000, 30, 3500);
            break;
        case 'Music':
            s.textContent = suggest(category, duration, goal, 10, 30, 37500);
            break;
        case 'Photography':
            s.textContent = suggest(category, duration, goal, 10, 30, 7500);
            break;
        case 'Publishing':
            s.textContent = suggest(category, duration, goal, 10000, 30, 13500);
            break;
        case 'Technology':
            s.textContent = suggest(category, duration, goal, 100, 30, 5000);
            break;
        case 'Theater':
            s.textContent = suggest(category, duration, goal, 100, 30, 3500);
            break;
    }
}



function show_results() {
    var canvas = document.getElementById("canvas");
    var duration = document.getElementById("days").value;
    var goal = document.getElementById("amount").value;
    var category = document.getElementById("category").value;
    var div = document.getElementById("textDiv");
    if (canvas.getContext) {
        var ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        div.textContent = "input a number of days (1-60) and an amount ($1-100,000)";
        ctx.fillStyle = "#0fbdcc";
        probability = success_percent(duration, goal, category);
        percent = probability * 100
        if (duration != 0 && goal != 0 && percent != 0) {
            form_suggestions(category, duration, goal);
            document.getElementById('chance-panel').style.display = "block";
            ctx.fillRect(0, 0, canvas.width * probability, 10);
            div.textContent = "you have a " + percent.toFixed(2) + "% chance of success.";
        }
    }
}



//