$(document).ready(function(){
    // check if email alrady exists when registering
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



    // checks if email is in the database before loggin in
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

    // check if you have a unique username
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

    $('.register').on('click', function() {
        $('.reg-body').toggle('slow');
    });

    $('.login').on('click', function() {
        $('.login-body').toggle('slow');
    });
    $('#info').hide();
    $('#about').on('click', function() {
        $('#info').show('slow', 'swing');
        $("#content").text("The Taste was created by Julian Sunn in 2021 after a deep desire to find cool restaurants off the beaten path in new areas.  Most people trust their friends and families recommendations the most and this site does just that.  We will show you restaurants in the areas you would like that are catered most to your and your networks tastes in restaurants.  Enjoy the journey towards your next amazing restaurant experience!")
    });

    $('#contact').on('click', function() {
        $('#info').show('slow', 'swing');
        $("#content").html(
        "<p>Please contact Julian Sunn using the contact methods below:</p><p>Phone: 1(530) 514-2519</p><p>Email: juliansunn@gmail.com</p><a href='https://www.github.com/juliansunn'>Julian's Github</a>")
    });

    $('#advertise').on('click', function() {
        $('#info').show('slow', 'swing');
        $("#content").text("As a restaurant owner, have you ever been irked by that pesky review that didn't understand your restaurant's mission or purpose?  If so, this is the site for you.  We will make sure the right users see your restaurant even if you aren't the most popular restaurant on Yelp.  Users also have a weighted recommendation of restaurants so the reviews they see first are from people in their network along with ratings.  This is a win/win!  Users will get recommended the restaurants they would most enjoy all while your restaurant is marketed to the right crowd.  Please contact Julian Sunn if you are looking to advertise on this website.")
    });
})