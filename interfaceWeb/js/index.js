// btn pour éteindre la led
var btn = document.querySelector('a');
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

/** MODAL **/
document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.modal');
  var instances = M.Modal.init(elems, 0.5);
});