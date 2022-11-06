
google.charts.load("current", {packages:["calendar"]});
google.charts.setOnLoadCallback(drawChart);

function drawChart(){
  fetch("http://localhost:5001/calendar")
  .then((response)=>response.json())
  .then((data)=>{
    var dataTable = new google.visualization.DataTable();
    dataTable.addColumn({ type: 'date', id: 'Date' });
    dataTable.addColumn({ type: 'number', id: 'Taken/Not Taken' });
    var dataRow = []
    for(d of data.data){
      c = -1
      if (d.weight_data == 0){
        c = 1
      }
      dataRow.push([new Date(d.time_created),c])
    }
    dataTable.addRows(dataRow);
    var chart = new google.visualization.Calendar(document.getElementById('calendar_basic'));
    var options = {
      title: "Medication Calendar",
    };
    chart.draw(dataTable, options);
  })
}