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

/* delete button */

let action=row.insertCell(4)

let btn=document.createElement("button")
btn.innerText="Delete"

btn.onclick=function(){
table.deleteRow(row.rowIndex)
}

action.appendChild(btn)

/* clear inputs */

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

/* END TIME */

let end=document.createElement("span")
end.innerText=g.end
end.style.marginLeft=(width-10)+"px"

timeRow.appendChild(end)

})

chart.appendChild(blockRow)
chart.appendChild(timeRow)

}

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

function priorityScheduling(processes){

let time=0
let completed=[]
let results=[]
let gantt=[]
let totalTat=0
let totalWt=0

let type=document.getElementById("priorityType").value

while(completed.length < processes.length){

let ready = processes.filter(p=>p.arrival<=time && !completed.includes(p.pid))

if(ready.length===0){
time++
continue
}

if(type==="low"){
ready.sort((a,b)=>a.priority - b.priority)
}

else{
ready.sort((a,b)=>b.priority - a.priority)
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

return {
results:results,
gantt:gantt,
avgTat:totalTat/processes.length,
avgWt:totalWt/processes.length
}

}

function roundRobin(processes, quantum, policy){

let time = 0
let queue = []
let gantt = []
let results = []
let remaining = {}

let totalTat = 0
let totalWt = 0

processes.forEach(p=>{
remaining[p.pid] = p.burst
})

processes.sort((a,b)=>a.arrival-b.arrival)

let i = 0

while(true){

while(i < processes.length && processes[i].arrival <= time){
queue.push(processes[i])
i++
}

if(queue.length === 0){

if(i >= processes.length) break

time++
continue
}

if(policy === "sjf"){
queue.sort((a,b)=>a.burst - b.burst)
}

if(policy === "srtf"){
queue.sort((a,b)=>remaining[a.pid] - remaining[b.pid])
}

if(policy === "priorityLow"){
queue.sort((a,b)=>a.priority - b.priority)
}

if(policy === "priorityHigh"){
queue.sort((a,b)=>b.priority - a.priority)
}

let p = queue.shift()

let run = Math.min(quantum, remaining[p.pid])

gantt.push({
pid:p.pid,
start:time,
end:time+run
})

time += run
remaining[p.pid] -= run

while(i < processes.length && processes[i].arrival <= time){
queue.push(processes[i])
i++
}

if(remaining[p.pid] > 0){

queue.push(p)

}
else{

let completion = time
let tat = completion - p.arrival
let wt = tat - p.burst

results.push({
pid:p.pid,
completion:completion,
tat:tat,
wt:wt
})

totalTat += tat
totalWt += wt

}

}

return {
results:results,
gantt:gantt,
avgTat: totalTat / processes.length,
avgWt: totalWt / processes.length
}

}

function run(){

let processes=getProcesses()

let algo=document.getElementById("algorithm").value
let quantum=parseInt(document.getElementById("quantum").value)

let result

if(algo==="fcfs") result=fcfs(processes)
if(algo==="sjf") result=sjf(processes)
if(algo==="priority") result=priorityScheduling(processes)
else if(algo==="rr"){

let policy = document.getElementById("rrPolicy").value

result = roundRobin(processes, quantum, policy)

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

document.getElementById("avgTat").innerText="Average TAT: "+result.avgTat
document.getElementById("avgWt").innerText="Average WT: "+result.avgWt

}

function runComparison(){

let processes=getProcesses()

let checks=document.querySelectorAll('input[type="checkbox"]:checked')

let container=document.getElementById("comparisonResults")

container.innerHTML=""

let quantum=parseInt(document.getElementById("quantum").value)

checks.forEach(c=>{

let algo=c.value
let result

if(algo==="fcfs") result=fcfs([...processes])
if(algo==="sjf") result=sjf([...processes])
if(algo==="priority") result=priorityScheduling([...processes])
if(algo==="rr") result=roundRobin([...processes],quantum)

let div=document.createElement("div")
div.className="panel"

div.innerHTML="<h3>"+algo.toUpperCase()+"</h3>"

/* Gantt Chart */

let ganttDiv=document.createElement("div")
ganttDiv.className="gantt-row"

result.gantt.forEach(g=>{

let block=document.createElement("div")

let duration=g.end-g.start

block.className="gantt-block"
block.innerText=g.pid
block.style.width=(duration*50)+"px"

ganttDiv.appendChild(block)

})

div.appendChild(ganttDiv)

/* Results Table */

let table=document.createElement("table")

table.innerHTML="<tr><th>PID</th><th>Completion</th><th>TAT</th><th>WT</th></tr>"

result.results.forEach(r=>{

let row=table.insertRow()

row.insertCell(0).innerText=r.pid
row.insertCell(1).innerText=r.completion
row.insertCell(2).innerText=r.tat
row.insertCell(3).innerText=r.wt

})

div.appendChild(table)

/* Average values */

let avg=document.createElement("p")

avg.innerText="Average TAT: "+result.avgTat.toFixed(2)+" | Average WT: "+result.avgWt.toFixed(2)

div.appendChild(avg)

container.appendChild(div)

})

}

function goBack(){
window.location="index.html"
}