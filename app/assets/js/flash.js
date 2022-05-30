for (let message of document.querySelectorAll('#flash-messages li')) {
  const button = message.querySelector('.close');
  button.onclick = function() {
    message.remove();
  };
}
