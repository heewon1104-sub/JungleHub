function validateForm() {
  let id = document.getElementById('id').value;
  let nickname = document.getElementById('nickname').value;
  let cardinal = document.getElementById('cardinal').value;
  let number = document.getElementById('number').value;

  if (validate(id, nickname, cardinal, number)) {
    return true;
  } else {
    return false;
  }
}

function validate(id, nickname, cardinal, number) {
  var space = /\s/g;

  console.log(id, nickname, cardinal, number);

  // 공백 검사
  if (id === '') {
    alert('아이디를 입력해주세요!');
    return false;
  }
  if (nickname === '') {
    alert('비밀번호를 입력해주세요!');
    return false;
  }
  if (cardinal == '') {
    alert('기수를 입력해주세요!');
    return false;
  }
  if (number == '') {
    alert('번호를 입력해주세요!');
    return false;
  }

  // 공백 포함 검사
  if (id.match(space)) {
    alert('아이디에 공백이 포함되어 있습니다.');
    return false;
  }
  if (nickname.match(space)) {
    alert('닉네임에 공백이 포함되어 있습니다.');
    return false;
  }
  if (cardinal.match(space)) {
    alert('기수에 공백이 포함되어 있습니다.');
    return false;
  }
  if (number.match(space)) {
    alert('번호에 공백이 포함되어 있습니다.');
    return false;
  }
  // 모든 검사 통과
  alert('회원가입이 완료되었습니다!');
  return true;
}

function handleSubmit(event) {
  event.preventDefault();
}
