function generate_pill_chart(date){
  fetch("http://localhost:5001/weight/" + date)
  .then((response)=>response.json())
  .then((data)=>{
    var chartData = data.data;
    new Chart("pillWeightLineChart", {
      type: "line",
      data: {
        labels: chartData.map(item => item.time_created),
        datasets: [
          {fill: 'origin'},
          {
            backgroundColor: "rgba(217, 50, 150, 0.7)",
            borderColor: "rgba(217, 50, 150, 0.1)",
            data: chartData.map(d=>d.weight_data),
            pointRadius: 0.1
          }
        ]
      },
      options: {
        scales: {
          xAxes: [ {
              display: false,
            }
          ],
          yAxes: [{ticks: {min: 0, max:100}}],
        },
        legend: {display: false},
        title: {
          display: true,
          text: "Pill Box Weight Status"
        }
      }
    });
  })
}