function answer1() {
    if(document.querySelector('#ans').value=="scripts")
        {
           swal("Congratulations!", "You are awesome!", "success");
        }
    else
        {
          swal("Awww!", "Try Again!", "warning");  
        }
}

function answer() {
    if(document.querySelector('#ans').value==".html")
        {
           swal("Good job!", "You are awesome!", "success");
        }
    else
        {
            swal("Awww!", "Try Again!", "warning");
             
        }
}