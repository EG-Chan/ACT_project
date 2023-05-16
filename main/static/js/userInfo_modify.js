
//이메일 정규식 확인
const regexPassword = new RegExp(/^(?=.*[a-zA-Z])(?=.*[0-9]).{6,16}$/);


let isPasswordValid = false;
let isPasswordConfirmed = false;

//패스워드 input에서 포커스가 벗어난경우
document.querySelector("#password").addEventListener("blur", (e) => {
    const pTag = document.querySelector("#password+p");
    const password = document.querySelector("#password").value;
    const confirmPassword = document.querySelector("#confirmPassword").value;

    //정규식이 맞은경우
    if (regexPassword.test(password)){ 
        isPasswordValid = true;
        pTag.innerHTML = "";

        //컨펌 패스워드와 같지않은경우 컨펌 패스워드 아래에 정보 노출시키기
        if (password == confirmPassword){ 
            isPasswordConfirmed = true;
            pTag.innerHTML = "";
            document.querySelector("#confirmPassword+p").innerHTML = "";
        }else{
            if (confirmPassword != ""){
                console.log("실행됨");
                isPasswordConfirmed = false;
                document.querySelector("#confirmPassword+p").innerHTML = "비밀번호가 같지 않습니다.";
            }
        }
    }else{
        isPasswordValid = false;
        pTag.innerHTML = "영문,숫자 6~16글자";
    }

    
});

//컨펌 패스워드 input에서 포커스가 벗어난경우
document.querySelector("#confirmPassword").addEventListener("blur", (e) => {
    const pTag = document.querySelector("#confirmPassword+p");
    const password = document.querySelector("#password").value;
    const confirmPassword = document.querySelector("#confirmPassword").value;

    //컨펌 패스워드와 같지않은경우 컨펌 패스워드 아래에 정보 노출시키기
    if (password == confirmPassword){ 
        isPasswordConfirmed = true;
        pTag.innerHTML = "";
    }else{
        isPasswordConfirmed = false;
        pTag.innerHTML = "비밀번호가 같지 않습니다.";
    }
});

//가입버튼을 누를때 모든 조건을 충족해야 폼 제출시키기
document.querySelector("#signUpButton").addEventListener("click", (e) => {
    if (isPasswordValid && isPasswordConfirmed){
        document.querySelector("form").submit();
    }else{
        document.querySelector(".signUp p").innerHTML = "회원정보를 수정해주세요.";
    }
});