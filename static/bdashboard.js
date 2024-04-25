let canvasElement= document.getElementById('bchart')

let config ={
    type: "bar",
    data: {
        label:[ "Aug31", "Sept30", "Oct31", "Nov30", "Dec31", "Jan30", "Feb28", "March31"],
        datasets: [{
            label: "number of applicants" , 
            data:[0,5.000,5.000,5.000,5.000, 5.000, 5.000 ],
            backgroundColor:[
               "#3355FD;",
               "#FDE355",
            ],

        }],
    },
} ;

let bchart = new Chart(canvasElement,config);