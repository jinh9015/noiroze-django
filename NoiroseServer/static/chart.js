// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

var ctx = document.getElementById('myAreaChart').getContext('2d');
// API 요청
fetch("http://127.0.0.1:8000/api/sound_level/") // API 엔드포인트 URL로 변경
    .then(response => response.json()) // 응답 데이터를 JSON 형식으로 변환
    .then(data => {
        var labels = data.map(item => item.place); // API 응답에서 place 데이터 추출
        var values = data.map(item => item.value); // API 응답에서 value 데이터 추출

        // 옵션 및 스타일 설정
        var options = {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        };

        // 차트 생성
        var myAreaChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Sound Level',
                    data: values,
                    backgroundColor: 'rgba(2,117,216,0.2)',
                    borderColor: 'rgba(22,117,216,1)',
                    pointRadius: 5,
                    pointBackgroundColor: 'rgba(2,117,216,1)',
                    pointBorderColor: 'rgba(255,255,255,0.8)',
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: 'rgba(2,117,216,1)',
                    pointHitRadius: 20,
                    pointBorderWidth: 2,
                    fill: false
                }]
            },
            options: options
        });
    });
