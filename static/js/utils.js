//정규표현식으로 이메일 유효성 검사
function validateEmail(email) {
  const regex =
    /^[0-9?A-z0-9?]+(\.)?[0-9?A-z0-9?]+@[0-9?A-z]+\.[A-z]{2}.?[A-z]{0,3}$/;

  return regex.test(email);
}

//입력시 공백 제거
function removeWhitespace(text) {
  var pattern = /\s/g;
  return text.ma(regex, '');
}
