
<!DOCTYPE HTML>
<html>
<head>
</head>
<body>
<script type="text/javascript">

window.onload = function showChart(){

  // Retreive objects from python bottle
  var flow_dataPoints = []
  var bytes_dataPoints = []
  var thread_dataPoints = []

  var system_stats = JSON.parse('{{!system_stats}}');
  var pgnames = JSON.parse('{{!pgnames}}');
  var flowfiles = JSON.parse('{{!flowfilesQueued}}');
  var bytesqueued = JSON.parse('{{!bytesQueued}}');
  var threadcount = JSON.parse('{{!activeThreads}}');
  var total_threadcount = '{{!total_threads}}'
  var idle = total_threadcount

  // Initialize y axis variables
  var f_y_val = 0
  var b_y_val = 0
  var t_y_val = 0


  // Define the charts

  var flow_chart = new CanvasJS.Chart("chartContainer1", {
  animationEnabled: true,
  title: {  text: "FlowFile Queue buildup by Processor Group" },
  data: setData(flow_dataPoints,'pie')
  });

  for (items in flowfiles){
    f_y_val = (flowfiles[items]*100/'{{!total_flowqueue}}')
    if(f_y_val>1){
      flow_dataPoints.push({y: f_y_val,label: items, click: onClick })
      }
  }

  var bytes_chart = new CanvasJS.Chart("chartContainer2", {
  animationEnabled: true,
  title: {  text: "Bytes Queue buildup by Processor Group" },
  data: setData(bytes_dataPoints,'pie')
  });

  for (items in bytesqueued){
    b_y_val = (bytesqueued[items]*100/'{{!total_bytes}}')
    if(b_y_val>1){
      bytes_dataPoints.push({y: b_y_val,label: items, click: onClick})
      }
  }

  var thread_chart = new CanvasJS.Chart("chartContainer3", {
  animationEnabled: true,
  title: {   text: "Active Thread Counts by Processor Group" },
  data: setData(thread_dataPoints,'pie')
  });

  for (items in threadcount){
    t_y_val = (threadcount[items]*100/total_threadcount)
    idle = total_threadcount - threadcount[items]
    if(t_y_val>0){
      thread_dataPoints.push({y: t_y_val,label: items,click: onClick})
      }
  }
  thread_dataPoints.push({y: idle*100/total_threadcount,label: "Non-active threads"})

  flow_chart.render();
  bytes_chart.render();
  thread_chart.render();

  function setData(dataPoints,type){
  var data_arr =  [{
    type: type,
    startAngle: 240,
    yValueFormatString: "##0.00\"%\"",
    indexLabel: "{label} {y}",
    dataPoints: dataPoints
    }]
  return data_arr
  }

  function onClick(e){
  alert(pgnames[e.dataPoint.label])
  }
};

</script>

<div id="chartContainer1" style="height: 370px; width: 48%;display: inline-block"></div>
<div id="chartContainer2" style="height: 370px; width: 48%;display: inline-block"></div><br>
<div id="chartContainer3" style="height: 370px; width: 33%;display: inline-block"></div>

<script src="static/canvasjs.min.js"></script>
</body>
</html>
