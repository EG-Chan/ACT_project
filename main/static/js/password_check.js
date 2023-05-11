const div = document.querySelector('[name=modify_id]');
const div2 = document.querySelector('[name=delete_id]');

const regexPassword = new RegExp(/^(?=.*[a-zA-Z])(?=.*[0-9]).{6,16}$/);
// console.log(sessionInfo)

function checkPassword() {
  // let password = prompt("패스워드를 입력해주세요.");
  // if (password) {
  //   const hash = sha256(password);
  //   console.log(hash)
  // }
  let div_input =  div.querySelector('#pw_id_modify');
  if (div_input) {
    div.removeChild(div_input);
  }
  else {
    let input = document.createElement('input');
    input.type = 'password';
    input.placeholder = '비밀번호를 입력후 엔터를 눌러주세요.';
    input.className = 'input_class';
    input.name = 'pw_name';
    input.id = 'pw_id_modify'
    div.appendChild(input);
  }
}
function checkPassword2() {
  // let password = prompt("패스워드를 입력해주세요.");
  // if (password) {
  //   const hash = sha256(password);
  //   console.log(hash)
  // }
  let div_input2 =  div2.querySelector('input');
  if (div_input2) {
    div2.removeChild(div_input2);
  }
  else {
    let input2 = document.createElement('input');
    input2.type = 'password';
    input2.placeholder = '비밀번호를 입력후 엔터를 눌러주세요.';
    input2.className = 'input_class';
    input2.name = 'pw_name';
    input2.id = 'pw_id_delete'
    div2.appendChild(input2);
  }
}

//패스워드 input에서 포커스가 벗어난경우
document.querySelector("#pw_id_modify").addEventListener("blur", (e) => {
  const pTag = document.querySelector("#pw_id_modify+p");
  const password = document.querySelector("#pw_id_modify").value;

  //정규식이 맞은경우
  if (regexPassword.test(password)){ 
      isPasswordValid = true;
      pTag.innerHTML = "";
  }else{
      isPasswordValid = false;
      pTag.innerHTML = "영문,숫자 6~16글자";
  }

  
});