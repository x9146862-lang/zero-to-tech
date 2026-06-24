function changeText() {
  document.getElementById('msg').innerText = '你点了我！CSS 和 JS 都生效啦 🎉';
}

function sayHello() {
  alert('你好！这是来自 app.js 的消息！');
}

function changeBgColor() {
  document.body.style.backgroundColor =
    '#' + Math.floor(Math.random()*16777215).toString(16).padStart(6, '0');
}
