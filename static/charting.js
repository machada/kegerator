
//Al's windows machine ip
url = 'http://10.0.0.52/getChartData';

//Al's rasp pi ip
url = 'http://10.0.0.150:1050/getChartData';

getData(url);



function getData(url){
    
    fetch(url)
        .then(res => res.json())
        .then(json => {
            
            renderChart(json.beer1.currentVolume, json.beer1.amountConsumed, "1", "bar")
            renderChart(json.beer2.currentVolume, json.beer2.amountConsumed, "2", "bar")
            renderLineChart(json.tempSeries1.tempReadings,json.tempSeries2.tempReadings,json.tempSeries3.tempReadings, json.tempSeries1.dateSeries, "3", "line")
            //renderLineChart()
        }
        )
}

function renderChart(amountLeft, consumed, chartNumber, chartType){
let currentChart = 'myChart' + chartNumber
let myChart = document.getElementById(currentChart).getContext('2d');

console.log('rendering chart');
let kegRemaining = new Chart(myChart, {
    type:"bar", //bar, horizontalBar, pie, Line, doughnut, radar, polarArea
    data:{
        labels:['Keg Status'],
        datasets:[
            {
            label:'Pints Remaining',
            data: [amountLeft],
            backgroundColor: '#D6E9C6', // green
           
        },
        {
        label: 'Pints Consumed',
        data: [consumed],
        backgroundColor: '#EBCCD1', // red
        
        }
        ]
    },
    options:{
        legend: {
            display: true,
        
          
        },
        scales: {
            xAxes: [{ stacked: true}],
            yAxes: [{ stacked: true}]
        },
       
    }
})
}

function renderLineChart(sensor1Temps,sensor2Temps,sensor3Temps, dateSeries, chartNumber, chartType){
    let currentChart = 'myChart' + chartNumber
    let myChart = document.getElementById(currentChart).getContext('2d');
    console.log('rendering chart');
    let kegRemaining = new Chart(myChart, {
        type:"line", //bar, horizontalBar, pie, Line, doughnut, radar, polarArea
        data:{
            labels:dateSeries,
            datasets:[
                {
                label:'Sensor 1',
                data: sensor1Temps,
                backgroundColor: '#B42033', // red
               
            },
            {
            label: 'Sensor 2',
            data: sensor2Temps,
            backgroundColor: '#FEFEFE', // White
            
            },
            {
                label: 'Sensor 3',
                data: sensor3Temps,
                backgroundColor: '#3C3B6E', // blue
                
                }


            ]
        },
        options:{
            legend: {
                display: true,
            
              
            },
            scales: {
                xAxes: [{ stacked: false}],
                yAxes: [{ stacked: false}]
            },
           
        }
    })
    }    
    