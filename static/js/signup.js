function validateForm() {
  let id = document.getElementById('id').value;
  let password = document.getElementById('password').value;
  let passwordconfirm = document.getElementById('password-confirm').value;
  let cardinal = document.getElementById('cardinal').value;
  let number = document.getElementById('number').value;

  if (validate(id, password, passwordconfirm, cardinal, number)) {
    return true;
  } else {
    return false;
  }
}

function validate(id, password, passwordconfirm, cardinal, number) {
  var space = /\s/g;

  console.log(id, password, passwordconfirm, cardinal, number);

  // 공백 검사
  if (id === '') {
    alert('아이디를 입력해주세요!');
    return false;
  }
  if (password === '') {
    alert('비밀번호를 입력해주세요!');
    return false;
  }
  if (passwordconfirm == '') {
    alert('비밀번호 확인을 입력해주세요!');
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
  if (password.match(space)) {
    alert('비밀번호에 공백이 포함되어 있습니다.');
    return false;
  }
  if (passwordconfirm.match(space)) {
    alert('비밀번호 확인에 공백이 포함되어 있습니다.');
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

  // 길이 검사
  if (id.length < 6) {
    alert('아이디는 6자 이상이어야 합니다.');
    return false;
  }
  if (password.length < 6) {
    alert('비밀번호는 6자 이상이어야 합니다.');
    return false;
  }

  // 비밀번호 확인 검사
  if (password !== passwordconfirm) {
    alert('비밀번호 확인 입력값이 비밀번호와 다릅니다.');
    return false;
  }

  // 모든 검사 통과
  alert('회원가입이 완료되었습니다!');
  return true;
}

function handleSubmit(event) {
  event.preventDefault();
}
