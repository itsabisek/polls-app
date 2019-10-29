$(document).ready(() => {

  $.ajax({
    method: "get",
    url: "/api/recent",
    success: (response) => {
      if(response.length == 0){
        const no_content = '<p>No Polls have been asked</p>'
        $('#all-polls').hide()
        $('#notes-list').html(no_content)
      }else{
        const content = response.reduce((html,question) => {
          html+= `<li>${question.question_text}</li>`
          return html
        },'')
        $('#notes-list').html(`<ul>${content}</ul>`)
      }
    }
  })
})
