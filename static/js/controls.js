function press(type) {
  fetch('/api/button_press', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({type})
  });
}
