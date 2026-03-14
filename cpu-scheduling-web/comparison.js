function runComparison(){

let algorithm =
document.querySelector('input[name="algorithm"]:checked').value;

let rows = document.querySelectorAll("#processTable tr");

let processes=[];

for(let i=1;i<rows.length;i++){

let cells = rows[i].cells;

processes.push({
pid:cells[0].innerText,
arrival:parseInt(cells[1].innerText),
burst:parseInt(cells[2].innerText)
});

}

let time=0;

let resultTable=document.getElementById("resultTable");

resultTable.innerHTML=
"<tr><th>PID</th><th>Completion</th><th>TAT</th><th>WT</th></tr>";

let gantt=document.getElementById("ganttChart");
gantt.innerHTML="";

let totalTat=0;
let totalWt=0;

processes.forEach(p=>{

if(time<p.arrival) time=p.arrival;

let completion=time+p.burst;

let tat=completion-p.arrival;
let wt=tat-p.burst;

totalTat+=tat;
totalWt+=wt;

let row=resultTable.insertRow();

row.insertCell(0).innerText=p.pid;
row.insertCell(1).innerText=completion;
row.insertCell(2).innerText=tat;
row.insertCell(3).innerText=wt;

let block=document.createElement("div");

block.className="gantt-block";
block.innerText=p.pid;

gantt.appendChild(block);

time=completion;

});

document.getElementById("algorithmName").innerText=
"Algorithm: "+algorithm.toUpperCase();

document.getElementById("avgTat").innerText=
"Average TAT: "+(totalTat/processes.length);

document.getElementById("avgWt").innerText=
"Average WT: "+(totalWt/processes.length);

}