// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';


//////시간별 평균 데시벨
var ctx = document.getElementById('myAreaChart').getContext('2d');

// API 요청
fetch('http://noiroze.com/api/sound_level/')
    .then(response => response.json()) // 응답 데이터를 JSON 형식으로 변환
    .then(data => {
        // 103동에 해당되는 데이터 필터링
        var filteredData = data.filter(item => item.dong === '103');

        // 시간대별로 데이터 그룹화
        var groupedData = {
            '02-06시': [],
            '06-10시': [],
            '10-14시': [],
            '14-18시': [],
            '18-22시': [],
            '22-02시': []
        };
        filteredData.forEach(item => {
            const createdAt = new Date(item.created_at);
            const hours = createdAt.getHours();
            const time = hours < 2 || hours >= 22 ? '22-02시' :
                         hours < 6 ? '02-06시' :
                         hours < 10 ? '06-10시' :
                         hours < 14 ? '10-14시' :
                         hours < 18 ? '14-18시' :
                         '18-22시';

            groupedData[time].push(item.value);
        });

        // 시간대별로 평균 계산
        var labels = ['02-06시', '06-10시', '10-14시', '14-18시', '18-22시', '22-02시'];
        var values = labels.map(time => {
            if (groupedData.hasOwnProperty(time)) {
                var group = groupedData[time];
                var sum = group.reduce((a, b) => a + b, 0);
                var average = sum / group.length;
                return average.toFixed(2); // 소수점 둘째 자리까지 표시 (선택사항)
            } else {
                return 0; // 데이터가 없을 경우 0으로 설정 (선택사항)
            }
        });

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
                    borderColor: 'rgba(2,117,216,1)',
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



/////////////일별 평균 데시벨

var ctx2 = document.getElementById('myBarChart').getContext('2d');

// API 요청
fetch('http://noiroze.com/api/sound_level/') // API 엔드포인트 URL로 변경
    .then(response => response.json()) // 응답 데이터를 JSON 형식으로 변환
    .then(data => {
        // "dong" 값이 103인 데이터 필터링
        var filteredData = data.filter(item => item.dong === "103");

        // 일별로 데이터 그룹화
        var groupedData = {};
        filteredData.forEach(item => {
            const createdAt = new Date(item.created_at);
            const date = createdAt.toISOString().split('T')[0];

            if (groupedData.hasOwnProperty(date)) {
                groupedData[date].push(item);
            } else {
                groupedData[date] = [item];
            }
        });

        // 최근 7일의 데이터 추출
        var currentDate = new Date();
        var labels = [];
        var values = [];
        for (let i = 0; i < 7; i++) {
            var date = currentDate.toISOString().split('T')[0];
            labels.unshift(date);

            var items = groupedData[date] || [];
            if (items.length === 0) {
                values.unshift('');
            } else {
                var sum = items.reduce((total, item) => total + item.value, 0);
                var average = sum / items.length;
                values.unshift(average.toFixed(2));
            }

            currentDate.setDate(currentDate.getDate() - 1);
        }

        // 옵션 및 스타일 설정
        var options = {
            scales: {
                xAxes: [{
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: 10, // 최대 10개의 눈금 표시
                        maxRotation: 0, // 눈금 텍스트 회전 없음
                        callback: function(value, index) {
                            if (value === '') return ''; // 데이터가 없는 경우 비워둡니다.

                            // value에는 labels의 각 요소가 순차적으로 전달됩니다.
                            // 예: "2023-06-01"
                            var date = new Date(value);
                            var month = date.getMonth() + 1;
                            var day = date.getDate();
                            return month + '/' + day; // 월/일 형식으로 표시 (예: "6/1")
                        }
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        };

        // 차트 생성
        var myBarChart = new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Sound Level',
                    data: values,
                    backgroundColor: 'rgba(2,117,216,0.2)',
                    borderColor: 'rgba(2,117,216,1)',
                    borderWidth: 1
                }]
            },
            options: options
        });
    });

// 매일 자정마다 데이터를 업데이트합니다.
setInterval(updateChartData, 86400000); // 24시간(1일) 간격으로 업데이트

function updateChartData() {
    fetch('http://noiroze.com/api/sound_level/') // API 엔드포인트 URL로 변경
        .then(response => response.json()) // 응답 데이터를 JSON 형식으로 변환
        .then(data => {
            // "dong" 값이 103인 데이터 필터링
            var filteredData = data.filter(item => item.dong === "103");

            // 일별로 데이터 그룹화
            var groupedData = {};
            filteredData.forEach(item => {
                const createdAt = new Date(item.created_at);
                const date = createdAt.toISOString().split('T')[0];

                if (groupedData.hasOwnProperty(date)) {
                    groupedData[date].push(item);
                } else {
                    groupedData[date] = [item];
                }
            });

            // 최근 7일의 데이터 추출
            var currentDate = new Date();
            var labels = [];
            var values = [];
            for (let i = 0; i < 7; i++) {
                var date = currentDate.toISOString().split('T')[0];
                labels.unshift(date);

                var items = groupedData[date] || [];
                if (items.length === 0) {
                    values.unshift('');
                } else {
                    var sum = items.reduce((total, item) => total + item.value, 0);
                    var average = sum / items.length;
                    values.unshift(average.toFixed(2));
                }

                currentDate.setDate(currentDate.getDate() - 1);
            }

            // 차트 데이터 업데이트
            myBarChart.data.labels = labels;
            myBarChart.data.datasets[0].data = values;
            myBarChart.update();
        });
}


/////// 호수별 평균 데시벨

var ctx3 = document.getElementById('myHoChart').getContext('2d');

// 호수 목록
var hoList = ['101', '102', '201', '202', '301', '302', '401', '402', '501', '502', '601', '602', '701', '702', '801', '802', '901', '902', '1001', '1002'];

// API 요청
fetch('http://noiroze.com/api/sound_level/')
    .then(response => response.json()) // 응답 데이터를 JSON 형식으로 변환
    .then(data => {
        // "dong" 값이 103인 데이터 필터링
        var filteredData = data.filter(item => item.dong === "103");

        // 호수별로 데이터 그룹화 및 평균 계산
        var groupedData = {};
        filteredData.forEach(item => {
            var ho = item.ho;
            if (groupedData.hasOwnProperty(ho)) {
                groupedData[ho].push(item.value);
            } else {
                groupedData[ho] = [item.value];
            }
        });

        // x 축 라벨 설정
        var labels = hoList;

        // 호수별 평균값 계산
        var values = hoList.map(ho => {
            var group = groupedData[ho] || [];
            if (group.length === 0) {
                return 0;
            } else {
                var sum = group.reduce((a, b) => a + b, 0);
                var average = sum / group.length;
                return average.toFixed(2);
            }
        });

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
        var myHoChart = new Chart(ctx3, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Sound Level',
                    data: values,
                    backgroundColor: 'rgba(2,117,216,0.2)',
                    borderColor: 'rgba(2,117,216,1)',
                    borderWidth: 1,
                    hoverBackgroundColor: 'rgba(2,117,216,0.4)',
                    hoverBorderColor: 'rgba(2,117,216,1)',
                }]
            },
            options: options
        });

        // 그래프 컨테이너의 너비 조정
        var chartContainer = document.getElementById('myHoChart').parentNode;
        chartContainer.style.width = '1450px'; // 원하는 가로 길이로 설정
    });

