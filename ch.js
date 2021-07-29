var xmlhttp = new XMLHttpRequest();
var url = "https://api.thingspeak.com/channels/1426475/fields/1.json?api_key=9FPG13PUBB18V8UU&results=2"
xmlhttp.open("GET", url, true);
xmlhttp.send();
xmlhttp.onreadystatechange = function(){
    if(this.readyState == 4 && this.status == 200){
        var data = JSON.parse(this.responseText);
        console.log(data);
    }
}

var ctx = document.getElementById('mycanvas').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange'],
        datasets: [{
            label: 'Pulse',
            data: [15, 19, 3, 5, 2, 3],
            backgroundColor: 'transparent',
            borderColor: 'red',
            borderWidth: 3
        },
        {
            label: 'SpO2',
            data: [9, 19, 3, 5, 2, 3],
            backgroundColor: 'transparent',
            borderColor: 'blue',
            borderWidth: 3
        },
        {
            label: 'Pressure (Mean)',
            data: [11, 19, 3, 5, 2, 3],
            backgroundColor: 'transparent',
            borderColor: 'green',
            borderWidth: 3
        },
        {
            label: 'Temperature',
            data: [10, 19, 3, 5, 2, 3],
            backgroundColor: 'transparent',
            borderColor: 'yellow',
            borderWidth: 3
        },
        {
            label: 'Stress',
            data: [14, 19, 3, 5, 2, 3],
            backgroundColor: 'transparent',
            borderColor: 'purple',
            borderWidth: 3
        }
        ]
    },
    options: {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        yAxes: [{
            ticks: {
                beginAtZero:true
            }
        }]
    }
}
});