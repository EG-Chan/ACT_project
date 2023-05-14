const ul = document.querySelector('.one_li')
const ul_out = document.querySelector('.one_li_output')
const text = ul.textContent;
// 공백제거
const lines = text.split('\n').map(line => line.trim());
// console.log(lines)
lines.forEach(line => {
  const li = document.createElement('li');
  li.textContent = line;
  li.classList.add('li_inner_q');
  if (line === '') {
    li.style.listStyleType = 'none';
    li.innerHTML = '<br>';
  }
  ul_out.appendChild(li);
});
ul.textContent = '';