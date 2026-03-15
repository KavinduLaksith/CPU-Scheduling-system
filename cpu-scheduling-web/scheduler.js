const inputs = [
document.getElementById("pid"),
document.getElementById("arrival"),
document.getElementById("burst"),
document.getElementById("priority")
];

inputs.forEach((input,index)=>{

input.addEventListener("keydown",function(e){

if(e.key==="Enter"){

e.preventDefault()

if(index < inputs.length-1){
inputs[index+1].focus()
}
else{
addProcess()
}

}

})

})

function addProcess(){

let table=document.getElementById("processTable")

let pid=document.getElementById("pid").value
let arrival=parseInt(document.getElementById("arrival").value)
let burst=parseInt(document.getElementById("burst").value)
let priority=parseInt(document.getElementById("priority").value || 0)

let row=table.insertRow()

row.insertCell(0).innerText=pid
row.insertCell(1).innerText=arrival
row.insertCell(2).innerText=burst
row.insertCell(3).innerText=priority

let action=row.insertCell(4)

let btn=document.createElement("button")
btn.innerText="Delete"

btn.onclick=function(){
table.deleteRow(row.rowIndex)
}

action.appendChild(btn)

document.getElementById("pid").value=""
document.getElementById("arrival").value=""
document.getElementById("burst").value=""
document.getElementById("priority").value=""

}

function getProcesses(){

let rows=document.querySelectorAll("#processTable tr")
let processes=[]

for(let i=1;i<rows.length;i++){

let c=rows[i].cells

processes.push({
pid:c[0].innerText,
arrival:parseInt(c[1].innerText),
burst:parseInt(c[2].innerText),
priority:parseInt(c[3].innerText)
})

}

return processes

}

/* ---------------- GANTT ---------------- */

function drawGantt(gantt){

let chart=document.getElementById("ganttChart")
if(!chart) return

chart.innerHTML=""

let blockRow=document.createElement("div")
blockRow.className="gantt-row"

let timeRow=document.createElement("div")
timeRow.className="gantt-time"

gantt.forEach((g,i)=>{

let duration = g.end - g.start
let width = duration * 60

/* BLOCK */

let block=document.createElement("div")
block.className="gantt-block"
block.innerText=g.pid
block.style.width = width + "px"

blockRow.appendChild(block)

/* START TIME */

if(i===0){

let start=document.createElement("span")
start.innerText=g.start
timeRow.appendChild(start)

}

let end=document.createElement("span")
end.innerText=g.end
end.style.marginLeft=(width-10)+"px"

timeRow.appendChild(end)

})

chart.appendChild(blockRow)
chart.appendChild(timeRow)

}

/* ---------------- FCFS ---------------- */

function fcfs(processes){

processes.sort((a,b)=>a.arrival-b.arrival)

let time=0
let results=[]
let gantt=[]
let totalTat=0
let totalWt=0

processes.forEach(p=>{

if(time<p.arrival) time=p.arrival

let start=time
let end=time+p.burst

gantt.push({pid:p.pid,start:start,end:end})

let completion=end
let tat=completion-p.arrival
let wt=tat-p.burst

results.push({pid:p.pid,completion:completion,tat:tat,wt:wt})

totalTat+=tat
totalWt+=wt

time=end

})

return {results,gantt,avgTat:totalTat/processes.length,avgWt:totalWt/processes.length}

}

/* ---------------- SJF ---------------- */

function sjf(processes){

let time=0
let completed=[]
let results=[]
let gantt=[]
let totalTat=0
let totalWt=0

while(completed.length<processes.length){

let ready=processes.filter(p=>p.arrival<=time && !completed.includes(p.pid))

if(ready.length===0){
time++
continue
}

ready.sort((a,b)=>a.burst-b.burst)

let p=ready[0]

let start=time
let end=time+p.burst

gantt.push({pid:p.pid,start:start,end:end})

let completion=end
let tat=completion-p.arrival
let wt=tat-p.burst

results.push({pid:p.pid,completion:completion,tat:tat,wt:wt})

totalTat+=tat
totalWt+=wt

time=end
completed.push(p.pid)

}

return {results,gantt,avgTat:totalTat/processes.length,avgWt:totalWt/processes.length}

}

/* ---------------- PRIORITY ---------------- */

function priorityScheduling(processes,type){

let time=0
let completed=[]
let results=[]
let gantt=[]
let totalTat=0
let totalWt=0

while(completed.length < processes.length){

let ready = processes.filter(p=>p.arrival<=time && !completed.includes(p.pid))

if(ready.length===0){
time++
continue
}

if(type==="low"){
ready.sort((a,b)=>a.priority-b.priority)
}
else{
ready.sort((a,b)=>b.priority-a.priority)
}

let p=ready[0]

let start=time
let end=time+p.burst

gantt.push({pid:p.pid,start:start,end:end})

let completion=end
let tat=completion-p.arrival
let wt=tat-p.burst

results.push({pid:p.pid,completion:completion,tat:tat,wt:wt})

totalTat+=tat
totalWt+=wt

time=end
completed.push(p.pid)

}

return {results,gantt,avgTat:totalTat/processes.length,avgWt:totalWt/processes.length}

}

/* ---------------- ROUND ROBIN ---------------- */

function roundRobin(processes, quantum, policy){

let time=0
let queue=[]
let gantt=[]
let results=[]
let remaining={}
let totalTat=0
let totalWt=0

processes.forEach(p=>{
remaining[p.pid]=p.burst
})

processes.sort((a,b)=>a.arrival-b.arrival)

let i=0

while(true){

while(i<processes.length && processes[i].arrival<=time){
queue.push(processes[i])
i++
}

if(queue.length===0){

if(i>=processes.length) break

time++
continue
}

if(policy==="sjf"){
queue.sort((a,b)=>a.burst-b.burst)
}

if(policy==="priorityLow"){
queue.sort((a,b)=>a.priority-b.priority)
}

if(policy==="priorityHigh"){
queue.sort((a,b)=>b.priority-a.priority)
}

let p=queue.shift()

let run=Math.min(quantum,remaining[p.pid])

gantt.push({pid:p.pid,start:time,end:time+run})

time+=run
remaining[p.pid]-=run

while(i<processes.length && processes[i].arrival<=time){
queue.push(processes[i])
i++
}

if(remaining[p.pid]>0){
queue.push(p)
}
else{

let completion=time
let tat=completion-p.arrival
let wt=tat-p.burst

results.push({pid:p.pid,completion:completion,tat:tat,wt:wt})

totalTat+=tat
totalWt+=wt

}

}

return {results,gantt,avgTat:totalTat/processes.length,avgWt:totalWt/processes.length}

}

/* ---------------- SINGLE MODE ---------------- */

function run(){

let processes=getProcesses()

let algo=document.getElementById("algorithm").value
let quantum=parseInt(document.getElementById("quantum").value)
let result

if(algo==="fcfs") result=fcfs(processes)

else if(algo==="sjf") result=sjf(processes)

else if(algo==="priority"){

let type=document.getElementById("priorityType").value
result=priorityScheduling(processes,type)

}

else if(algo==="rr"){

let policy=document.getElementById("rrPolicy").value
result=roundRobin(processes,quantum,policy)

}

drawGantt(result.gantt)

let table=document.getElementById("resultTable")

table.innerHTML="<tr><th>PID</th><th>Completion</th><th>TAT</th><th>WT</th></tr>"

result.results.forEach(r=>{

let row=table.insertRow()

row.insertCell(0).innerText=r.pid
row.insertCell(1).innerText=r.completion
row.insertCell(2).innerText=r.tat
row.insertCell(3).innerText=r.wt

})

document.getElementById("avgTat").innerText="Average TAT: "+result.avgTat.toFixed(2)
document.getElementById("avgWt").innerText="Average WT: "+result.avgWt.toFixed(2)

}

/* ---------------- COMPARISON MODE ---------------- */

function runComparison(){

let processes = getProcesses()
let checks = document.querySelectorAll('input[type="checkbox"]:checked')
let container = document.getElementById("comparisonResults")

container.innerHTML=""

let quantum = parseInt(document.getElementById("quantum").value)

let summary=[]   // store algorithm results

checks.forEach(c=>{

let algo=c.value
let result

if(algo==="fcfs") result=fcfs([...processes])
if(algo==="sjf") result=sjf([...processes])
if(algo==="priorityLow") result=priorityScheduling([...processes],"low")
if(algo==="priorityHigh") result=priorityScheduling([...processes],"high")
if(algo==="rr_fcfs") result=roundRobin([...processes],quantum,"fcfs")
if(algo==="rr_sjf") result=roundRobin([...processes],quantum,"sjf")
if(algo==="rr_srtf") result=roundRobin([...processes],quantum,"srtf")    
if(algo==="rr_priorityLow") result=roundRobin([...processes],quantum,"priorityLow")
if(algo==="rr_priorityHigh") result=roundRobin([...processes],quantum,"priorityHigh")

/* show gantt chart */

/* show gantt chart */

let div = document.createElement("div")
div.className = "panel"

div.innerHTML = "<h3>" + algo.toUpperCase() + "</h3>"

/* gantt row */

let ganttDiv = document.createElement("div")
ganttDiv.className = "gantt-row"

/* timeline row */

let timeDiv = document.createElement("div")
timeDiv.className = "time-row"

result.gantt.forEach((g,i)=>{

let block=document.createElement("div")
let duration=g.end-g.start

block.className="gantt-block"
block.innerText=g.pid
block.style.width=(duration*50)+"px"

ganttDiv.appendChild(block)

/* timeline numbers */

let time=document.createElement("span")

if(i==0){
time.innerText=g.start
timeDiv.appendChild(time)
}

let endTime=document.createElement("span")
endTime.innerText=g.end
endTime.style.marginLeft=(duration*50-10)+"px"

timeDiv.appendChild(endTime)

})

div.appendChild(ganttDiv)
div.appendChild(timeDiv)

/* averages */

let avg=document.createElement("p")

avg.innerText="Average TAT: "+result.avgTat.toFixed(2)+" | Average WT: "+result.avgWt.toFixed(2)

div.appendChild(avg)

container.appendChild(div)

/* save for summary table */

summary.push({
algorithm:algo.toUpperCase(),
wt:result.avgWt,
tat:result.avgTat
})

})

/* ---------- FINAL COMPARISON TABLE ---------- */

let table=document.createElement("table")

table.innerHTML=`
<tr>
<th>Algorithm</th>
<th>Avg WT</th>
<th>Avg TAT</th>
</tr>
`

let bestAlgo=summary[0]

summary.forEach(r=>{

if(r.wt < bestAlgo.wt){
bestAlgo = r
}

let row=table.insertRow()

row.insertCell(0).innerText=r.algorithm
row.insertCell(1).innerText=r.wt.toFixed(2)
row.insertCell(2).innerText=r.tat.toFixed(2)

})

container.appendChild(document.createElement("hr"))

let title=document.createElement("h2")
title.innerText="Final Comparison"
container.appendChild(title)

container.appendChild(table)

/* ---------- BEST ALGORITHM ---------- */

let best=document.createElement("h2")
best.innerText="Best Scheduling Algorithm: "+bestAlgo.algorithm

best.style.color="#22c55e"

container.appendChild(best)

}

function goBack(){
window.location="index.html"
}