var modal = document.getElementById('accessDeniedModal');

var btn = document.getElementById("buttonModal");

var span = document.getElementsByClassName("close")[0];
 
btn.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var btn = document.querySelector('input');
var txt = document.querySelector('p');

btn.addEventListener('click', updateBtn);

function updateBtn() {
  if (btn.value === 'Allumer la lumière') {
    btn.value = 'Arrêter la lumière';
    txt.textContent = 'La lumière est allumée !';
  } else {
    btn.value = 'Allumer la lumière';
    txt.textContent = 'La lumière est arrêtée.';
  }
}