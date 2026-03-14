function goNext(){

let mode=document.querySelector('input[name="mode"]:checked')

if(!mode){
alert("Please select mode")
return
}

if(mode.value==="comparison"){
window.location="comparison.html"
}

if(mode.value==="single"){
window.location="single.html"
}

}

function addProcess(){

let table=document.getElementById("processTable")

let pid=document.getElementById("pid").value
let arrival=document.getElementById("arrival").value
let burst=document.getElementById("burst").value

let row=table.insertRow()

row.insertCell(0).innerText=pid
row.insertCell(1).innerText=arrival
row.insertCell(2).innerText=burst

}