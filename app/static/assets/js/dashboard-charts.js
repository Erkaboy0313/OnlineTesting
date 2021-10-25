var trafficchart = document.getElementById("trafficflow");
var saleschart = document.getElementById("sales");
var datas = month.split(['&#x27;']).join(',').split('[').join(',').split(']').join(',').split(',')
var score = scores.split(['&#x27;']).join(',').split('[').join(',').split(']').join(',').split(',')
const label = datas.filter(word => word.trim().length > 0);
const date = score.filter(word => word.trim().length > 0);

// new
var myChart1 = new Chart(trafficchart, {
type: 'line',
data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [{
        data: ['1135', '1135', '1140', '1168', '1150', '1145', '1155', '1155', '1150', '1160', '1185', '1190'],
        backgroundColor: "rgba(48, 164, 255, 0.2)",
        borderColor: "rgba(48, 164, 255, 0.8)",
        fill: true,
        borderWidth: 1
    }]
},
options: {
    animation: {
        duration: 2000,
        easing: 'easeOutQuart',
    },
    plugins: {
        legend: {
            display: false,
            position: 'right',
        },
        title: {
            display: true,
            text: 'Number of Visitors',
            position: 'left',
        },
    },
}
});

// new
var myChart2 = new Chart(saleschart, {
type: 'bar',
data: {
    labels: label,
    datasets: [{
            label: 'Income',
            data: date,
            backgroundColor: "rgba(76, 175, 80, 0.5)",
            borderColor: "#6da252",
            borderWidth: 1,
    }]
},
options: {
    animation: {
        duration: 2000,
        easing: 'easeOutQuart',
    },
    plugins: {
        legend: {
            display: false,
            position: 'top',
        },
        title: {
            display: true,
            text: 'Number of Sales',
            position: 'left',
        },
    },
}
});
