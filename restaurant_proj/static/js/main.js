$(document).ready(function(){
    
    $("#email").keyup(function(){
        var email = $(this).val();
        console.log(email);
        $.ajax({
            url: "/ajax/validate-email",
            data: {
                'email': email
            },
            dataType: 'json',
            success: function(data){
                if (data.found) {
                    $("#emailmsg").html("<p class='text-danger'>A User has already registered with this email.</p>")
                }
                else {
                    $("#emailmsg").html("")
                }
            }
        })
    })

    $("#login-email").focusout(function(){
        var email = $(this).val();
        $.ajax({
            url: "/ajax/validate-email",
            data: {
                'email': email
            },
            dataType: 'json',
            success: function(data){
                if (data.found) {
                    $("#login-emailmsg").html("")
                }
                else {
                    $("#login-emailmsg").html("<p class='text-danger'>This email is not in our database.</p>")
                }
            }
        })
    })


    $("#username").keyup(function(){
        var username = $(this).val();
        $.ajax({
            url: "/ajax/validate-username",
            data: {
                'username': username
            },
            dataType: 'json',
            success: function(data){
                if (data.found) {
                    $("#usernamemsg").html("<p class='text-danger'>This Username is already taken.  Please pick a different one.</p>")
                }
                else {
                    $("#usernamemsg").html("<p class='text-success'>Valid Username</p>")
                }
            }
        })
    })
})