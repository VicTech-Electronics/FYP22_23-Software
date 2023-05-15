var form = document.getElementById('submit_form');
var button = document.getElementById('submit_btn');
var label = button.textContent;

if(label == 'ON') button.style.backgroundColor = 'red';
else button.style.backgroundColor = 'green';

button.addEventListener('click', function(){
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'submited_value';

    if(label == 'ON'){
        input.value = 'OFF';
        form.appendChild(input);
    }else{
        input.value = 'ON';
        form.appendChild(input);
    }
    form.submit();
})