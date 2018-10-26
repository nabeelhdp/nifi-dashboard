
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
  var heap_dataPoints = []
  var nonheap_dataPoints = []
  var flowfilerepousage_dataPoints = []

  var system_stat = JSON.parse('{{!system_stats}}');
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
  title: {   text: "Load Average: " + system_stat['loadAverage'] + " \n Active Thread Counts by Processor Group"},
  //system_stat['loadAverage'] processorLoadAverage']
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

  var heap_chart = new CanvasJS.Chart("chartContainer4", {
  animationEnabled: true,
  title: {  text: "Heap Usage" },
  data: setData(heap_dataPoints,'pie')
  });

  h_y_val = (system_stat['usedHeap']*100/system_stat['totalHeap'])
  heap_dataPoints.push({y: h_y_val,label: "Used Heap"})
  h_y_val = (system_stat['freeHeap']*100/system_stat['totalHeap'])
  heap_dataPoints.push({y: h_y_val,label: "Free Heap"})

  var nonheap_chart = new CanvasJS.Chart("chartContainer5", {
  animationEnabled: true,
  title: {  text: "Non Heap Usage" },
  data: setData(nonheap_dataPoints,'pie')
  });

  nh_y_val = (system_stat['usedNonHeap']*100/system_stat['totalNonHeap'])
  nonheap_dataPoints.push({y: nh_y_val,label: "Used Heap"})
  nh_y_val = (system_stat['freeNonHeap']*100/system_stat['totalNonHeap'])
  nonheap_dataPoints.push({y: nh_y_val,label: "Free Heap"})

  var flowfilerepousage_chart = new CanvasJS.Chart("chartContainer6", {
  animationEnabled: true,
  title: {  text: "FlowFile Repository Storage Usage" },
  data: setData(flowfilerepousage_dataPoints,'pie')
  });

  ff_y_val = (system_stat['flowfileRepoUsed']*100/system_stat['flowfileRepoTotal'])
  flowfilerepousage_dataPoints.push({y: nh_y_val,label: "Used Heap"})
  ff_y_val = (system_stat['flowfileRepofree']*100/system_stat['flowfileRepoTotal'])
  flowfilerepousage_dataPoints.push({y: nh_y_val,label: "Free Heap"})


  flow_chart.render();
  bytes_chart.render();
  thread_chart.render();
  heap_chart.render();
  nonheap_chart.render();
  flowfilerepousage_chart.render();

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
<div id="chartContainer1" style="height: 370px; width: 33%;display: inline-block"></div>
<div id="chartContainer2" style="height: 370px; width: 33%;display: inline-block"></div>
<div id="chartContainer3" style="height: 370px; width: 33%;display: inline-block"></div><br><br>
<div id="chartContainer4" style="height: 370px; width: 33%;display: inline-block"></div>
<div id="chartContainer5" style="height: 370px; width: 33%;display: inline-block"></div>
<div id="chartContainer6" style="height: 370px; width: 33%;display: inline-block"></div>

<script src="static/canvasjs.min.js"></script>
</body>
</html>
