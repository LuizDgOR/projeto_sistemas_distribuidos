
const styleForm = document.querySelector('form .my-3');
console.log(styleForm)
  
const errorsEl = styleForm.querySelector('.errorlist');
if(errorsEl){
  errorsEl.classList.add('text-sm', 'text-red-500');
}

const p = styleForm.querySelectorAll('p');

p.forEach((el) => {
  console.log(el)
  el.classList.add('my-3');
  
  const labelEl = el.querySelector('label');
  if (labelEl) {
    labelEl.classList.add('font-extrabold');
  }

  const spanEl = el.querySelector('span');
  if (spanEl) {
    spanEl.classList.add('text-sm');
  }

  const aEl = el.querySelector('a');
  if (aEl) {
    aEl.classList.add('text-sm', 'text-blue-300');
    aEl.target = '_blank'
  }
})