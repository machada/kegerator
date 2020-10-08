
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
            backgroundColor: 'rgba(60,59,110,1)',// blue
            size: '50',
           
        },
        {
        label: 'Pints Consumed',
        data: [consumed],
        backgroundColor: 'rgba(178,34,52)', // red
        
        }
        ]
    },
    options:{
        legend: {
            display: true,
        
          
        },
        scales: {
            xAxes: [{ stacked: true,
                ticks:{
                    fontSize:30
                }}],
            yAxes: [{ stacked: true,
                ticks:{
                    fontSize:20
                }
            }]
        },
       
    }
})
}

function renderLineChart(sensor1Temps,sensor2Temps,sensor3Temps, dateSeries, chartNumber, chartType){
    let currentChart = 'myChart' + chartNumber
    let myChart = document.getElementById(currentChart).getContext('2d');
    console.log('rendering chart1');
    let kegRemaining = new Chart(myChart, {
        type:"line", //bar, horizontalBar, pie, Line, doughnut, radar, polarArea
        fillOpacity: .3,
        data:{
            labels:dateSeries,
            datasets:[
                {
                label:'Sensor 1',
                data: sensor1Temps,
                //backgroundColor: '#B42033', // red
                fillOpacity: .1,
                backgroundColor:'rgba(178,34,52,.3)',
                borderColor:'#B42033',
                borderWidth:'5',

            
               
            },
            {
            label: 'Sensor 2',
            data: sensor2Temps,
            backgroundColor: 'rgba(0,0,0,0)', // White
            borderColor:'rgba(207,207,207)',//grey
            borderWidth:'5',
            },
            {
                label: 'Sensor 3',
                data: sensor3Temps,
                //backgroundColor: '#3C3B6E', // blue
                borderColor:'rgba(60,59,110,.6)',
                borderWidth:'5',
                
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
    