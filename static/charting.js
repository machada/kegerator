
url = 'http://10.0.0.52/getChartData';
getData(url);

console.log("in charting");

function getData(url){
    fetch(url)
        .then(res => res.json())
        .then(json => {
            
            renderChart(json.beer1.currentVolume, json.beer1.amountConsumed, "1", "bar")
            renderChart(json.beer2.currentVolume, json.beer2.amountConsumed, "2", "bar")
            renderLineChart(json.beer2.currentVolume, json.beer2.amountConsumed, "3", "bar")
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

function renderLineChart(amountLeft, consumed, chartNumber, chartType){
    let currentChart = 'myChart' + chartNumber
    let myChart = document.getElementById(currentChart).getContext('2d');
    
    console.log('rendering chart');
    let kegRemaining = new Chart(myChart, {
        type:"line", //bar, horizontalBar, pie, Line, doughnut, radar, polarArea
        data:{
            labels:[0, 10, 20 ,30, 40, 50, 60],
            datasets:[
                {
                label:'Sensor 1',
                data: [10,15,10,20,5,6,25],
                backgroundColor: '#D6E9C6', // green
               
            },
            {
            label: 'Sensor 2',
            data: [20,25,20,30,25,6,25],
            backgroundColor: '#EBCCD1', // red
            
            },
            {
                label: 'Sensor 3',
                data: [20,25,20,30,25,6,25],
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
    