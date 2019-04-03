//modal pour code bouton
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

// btn pour éteindre la led
var btn = document.querySelector('input');
var txt = document.getElementsByClassName("ledStatus")[0];

btn.addEventListener('click', updateBtn);

function updateBtn() 
{
  if (btn.value === 'Allumer la lumière') 
    {
        btn.value = 'Arrêter la lumière';
        txt.textContent = 'La lumière est allumée.';
    } 
  else 
    {
        btn.value = 'Allumer la lumière';
        txt.textContent = 'La lumière est arrêtée.';
    }
}

document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.modal');
  var instances = M.Modal.init(elems, options);
});