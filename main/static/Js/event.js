

function seatClick(obj) {
  const id_name = document.getElementById("1")
  if (id_name === 1){
      obj.style.background="#00ff48";
  }
  else{
    obj.style.background = "#ff0000";
    const id = document.getElementById("1")
    const n = document.getElementById('1').value = id.value
    console.log(n)
  }


}
function overdown(obj){
 obj.style.background="#00ff48";
}
function overup(obj){
 obj.style.background="#fff";
}
