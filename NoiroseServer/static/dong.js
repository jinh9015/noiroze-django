function loadDongContent(dong) {
    // Ajax 요청을 생성합니다.
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          // Ajax 요청이 성공한 경우 동적으로 내용을 변경합니다.
          var content = xhr.responseText;
          document.getElementById("dong-content").innerHTML = content;
        } 
        else {
          // Ajax 요청이 실패한 경우 에러 처리를 수행합니다.
          console.error('Request failed. Error code:', xhr.status);
        }
      }
    };
    
    // 서버로 요청을 보냅니다.
    xhr.open('GET', '/dong/' + dong + '/', true);
    xhr.send();
  }
  