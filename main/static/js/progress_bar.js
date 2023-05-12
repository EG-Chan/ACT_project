const form = document.querySelector('#service_form');
const progressBar = document.querySelector('#progress_bar');
const trendCheckBox = document.querySelector('#trend_check_box');

// 트렌트분석 체크시
trendCheckBox.addEventListener('change', (e) => {
    if (e.target.checked){
        alert(`최근 트렌트 분석은 개발자가 가난하여 데이터 수집에 10초가 걸릴 수 있으며 트래픽에 일부 제한이 있습니다.`)
    }else{
        alert('최근 트렌트 분석을 해제합니다.')
    }
});

// progressbar 업데이트시키기
function updateProgressBar(progress) {
    progressBar.style.width = progress + '%';
}

let progress = 0;

// 버튼 눌렀을 때 작동할 함수
form.addEventListener('submit', (e) => {
    
    // 바로 보내는 것 막기
    e.preventDefault();
    
    // bar 속도 조절, 2체크시에만 맞춰서
    let intervalTime = 500
    let progressTime = 10
    if (trendCheckBox.checked){
        intervalTime = 1000
        progressTime = 4
    }

    // bar 보여주기
    progressBar.style.display = 'block';

    // bar 색 채워주는 함수
    const intervalId = setInterval(() => {
        progress += progressTime;
        updateProgressBar(progress);

        if (progress >= 100) {
            clearInterval(intervalId);
        }
    }, intervalTime);

    // ajax
    const formData = new FormData(form);
    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    }).then(response => response.text())
        .then(data => {
            // 스포티파이 19+ 곡 검색시 예외처리
            if(data.slice(0, 13)=='spofty_limit:'){
                alert('스포티파이 정책에 의해 제한이 걸린 노래입니다.');
                let locationPath = '/result/' + data.slice(13);
                window.location.assign(locationPath);
            }else{
            document.documentElement.innerHTML = data;
            }
        }).finally(() => {
            progressBar.style.display = 'none';
        });
});