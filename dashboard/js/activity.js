var barColors = ["green","blue","red"];
const walkImage = new Image(20,25);
const restImage = new Image(25,20);
const fallImage = new Image(30,30);
// walkImage.src = 'https://cdn-icons-png.flaticon.com/128/5340/5340966.png';
// restImage.src = 'https://cdn-icons-png.flaticon.com/128/680/680593.png';
// fallImage.src = 'https://cdn-icons-png.flaticon.com/128/4939/4939171.png';
walkImage.src = "img/walk.png"
restImage.src = "img/rest.png"
fallImage.src = "img/fall.png"

function generate_activity_chart(date){
  fetch("http://localhost:5001/acceleration/"+date)
  .then((response)=>response.json())
  .then((data)=>{
    var pointsArray = [];
    var walk = 0;
    var fall = 0;
    var rest = 0;

    var chartData = data.data;

    for (d of chartData){
      d.y = d.acc;
      if(d.acc < 50){
        pointsArray.push(restImage);
        rest += 1;
      }
      else if(d.acc < 200){
        pointsArray.push(walkImage);
        walk += 1;
      }
      else{
        pointsArray.push(fallImage);
        fall += 1;
      }
    }

    var activityArray = [rest,walk,fall];
    console.log(window.activityLineChart)
    if( window.ALC!==undefined){
      window.ALC.destroy();
    }

    if( window.APC!==undefined){
      window.APC.destroy();
    }


    window.ALC = new Chart("activityLineChart", {
      type: "line",
      data: {
        labels: chartData.map(item => item.time_created),
        datasets: [{
          fill: false,
          lineTension: 0,
          backgroundColor: "rgba(0,0,255,1.0)",
          borderColor: "rgba(0,0,255,0.1)",
          data: chartData
        }]
      },
      options: {
        scales: {
          xAxes: [ {
              display: false,
            }
          ],
        },
        elements: {
          point: {
            pointStyle: pointsArray
          }
        },
        tooltips: {
          enabled: true,
          mode: 'single',
          callbacks: {
            label: function (tooltipItems, data) {
              var multistringText = ['Value: ' + tooltipItems.yLabel];
              multistringText.push('Device Status: ' + data['datasets'][tooltipItems.datasetIndex]['data'][tooltipItems.index].tilt);
              return multistringText;
            }
          }
        },
        legend: {display: false},
        title: {
          display: true,
          text: "Activity Status of User"
        }
      }
    });

    window.APC = new Chart("activityPieChart", {
      type: "pie",
      data: {
        labels: ["rest","walk","fall"],
        datasets: [{
          backgroundColor: barColors,
          data: activityArray
        }]
      },
      options: {
        title: {
          display: true,
          text: "Activity Breakdown of User"
        }
      }
    });
  });
}