$('#login').click((evt) => {
  evt.preventDefault()
  var form_data = $("#form-login").serialize()

  $.ajax({
      type: "post",
      url: '/polls/api/login',
      data: form_data,
      success: (response) => {
        $('body').html(response)
      },
      error: () => {
        alert("Error")
      }
  })
})

$('#signup').click((evt) => {
  evt.preventDefault()
  var password = $('#password').val()
  var confirm = $('#confirm').val()

  if(password.length < 8){
    alert('Password should be atleast 8 characters')
  }

  else if(password != confirm){
    alert("Passwords don't match")
  }

  else{
    var form_data = $('#form-signup').serialize()

    $.ajax({
      type: "post",
      url: "/polls/api/register",
      data: form_data,
      success: (response) => {
        $('body').html(response)
      }
    })
  }
})


$('#logout').bind('click', () => {

  $.ajax({
    request: "post",
    url: 'polls/api/logout',
    success: (response) => {
      $('body').html(response)
    },
    error: () => {
      alert("Error")
    }
  })
})

// $('#password,#confirm').on('keyup', () => {
//   if ($('#password').val() == $('#confirm'))
// })
