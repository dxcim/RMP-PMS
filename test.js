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
              const csv = require("csvtojson");

              (async () => {
                const data = await csv().fromFile("dataset1.csv");
              })();

              hr = data[].HR;
              hr = data[].HR;
              hr = data[].HR;
              hr = data[].HR;
              hr = data[].HR;

              var ctx = document.getElementById('mycanvas').getContext('2d');
              var myChart = new Chart(ctx, {
                  type: 'line',
                  data: {
                      labels: ['14:27:00', '14:27:10', '14:27:20', '14:27:30', '14:27:40', '14:27:50'],
                      datasets: [{
                          label: 'Pulse',
                          data: [68, 69, 68, 68, 69, 71],
                          backgroundColor: 'transparent',
                          borderColor: 'red',
                          borderWidth: 2
                      },
                      {
                          label: 'SpO2',
                          data: [98, 98, 98, 99, 99, 98],
                          backgroundColor: 'transparent',
                          borderColor: 'blue',
                          borderWidth: 2
                      },
                      {
                          label: 'Pressure (Mean)',
                          data: [99.23, 99.9, 98.3, 98.5, 97.2, 99.3],
                          backgroundColor: 'transparent',
                          borderColor: 'green',
                          borderWidth: 2
                      },
                      {
                          label: 'Temperature',
                          data: [37.23, 37.19, 37.3, 37.85, 38.92, 37.83],
                          backgroundColor: 'transparent',
                          borderColor: 'yellow',
                          borderWidth: 2
                      },
                      {
                          label: 'Stress',
                          data: [214, 219, 213, 215, 212, 213],
                          backgroundColor: 'transparent',
                          borderColor: 'purple',
                          borderWidth: 2
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