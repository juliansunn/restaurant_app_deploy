$(document).ready(function(){
    
    // This is the state change in the explore function
    $("#state").change(function(){
        var state = $(this).val();
        $.ajax({
            url: "/dashboard/ajax/state_change",
            data: {
                'state': state
            },
            dataType: 'json',
            success: function(data){
                $("#city").empty();
                $("#category").empty()
                if (data.cities) {
                    $("#category").append(new Option("All", "all"))
                    for (i in data.cities) {
                        $("#city").append(new Option(data.cities[i], data.cities[i]));
                    }
                    
                    $("#city").trigger("change");
                    
                }
            }
        })
    })
    
    // This is the state change in the explore function
    $("#city").change(function(){
        var city = $(this).val();
        $.ajax({
            url: "/dashboard/ajax/city_change",
            data: {
                'city': city
            },
            dataType: 'json',
            success: function(data){
                $("#category").empty();
                $("#category").append(new Option("All", "all"));
                if (data.categories) {
                    for (i in data.categories) {
                        $("#category").append(new Option(data.categories[i], data.categories[i]));
                    }
                }
            }
        })
    })

    // This is the Search Bar Autocomplete Function.
    $(document).ready(function () {
        $( "#rest_search" ).autocomplete({
        source: "/dashboard/ajax/autocomplete"

        });
    });


    $( "#new-loc-search" ).autocomplete({
    source: "/dashboard/ajax/new_loc_autocomplete"
    });

    // discontinued button that was used in the explore_friends.html...
    $("#friend_btn").click(function(e){
        var friend_id = $(this).attr("value");
        e.preventDefault()
        $.ajax({
            url: "/dashboard/friend/" + friend_id,
            dataType: 'json',
            success: function(data){
                $("#friend_btn").text(data['status']);
            }
        })
    })

    // Like button that rides with the display for a restaurant
    $(".likebutton").click(function(e){
        e.preventDefault();
        var id = $(this).attr("data-catid");
        var status = $(this).text();
        $.ajax({
            type: "GET",
            url: "/dashboard/restaurants/favorite",
            data: {
                rest_id: id,
                status: status,
            },
            success: function(data){
                if (data['status'] == "Unfavorite"){
                    $("#like"+id).removeClass('btn btn-primary btn-sm');
                    $("#like"+id).addClass('btn btn-dark btn-sm');
                    $("#like"+id).text(data['status']);
                }
                else{
                    $("#like"+id).removeClass('btn btn-dark btn-sm');
                    $("#like"+id).addClass('btn btn-primary btn-sm');
                    $("#like"+id).text(data['status']);
                }
                


            }


        })
    })

    // Submit edit_reveiw on submit
    $('.edit_review_form').on('submit', function(event){
        // event.preventDefault();
        edit_review(this.id)
        
    })
    
    $("#db-search").click(function(e){
        var state = $("#state").val();
        var city = $("#city").val();
        var category = $("#category").val();
        // e.preventDefault();
        $.ajax({
            url: "/dashboard/explore",
            data: {
                'city': city,
                'state': state,
                'category': category,
            },
            dataType: 'json',
        })
    })

    // Star rating function below //

    $('.star').on('click', function(){
        var ratingList = ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent'];
        $('.star').removeClass('checked');
        var count = $(this).attr('value'); 
        var review = $(this).attr('id').slice(2);
        $("#rating"+count).prop("checked", true);
        $("#rating-desc"+review).text(ratingList[count-1]);
        for (var i=0; i<=count-1; i++){      
            var star = i + 1
            $('#'+star+"-"+review).addClass('checked');
        }
    });

    // toggle to show more/less reviews
    if ($('.review-list').length > 5) {
        $('.review-list:gt(4)').hide();
        $('.show-more-reviews').show();
    }
    else{
        $('.show-more-reviews').hide();
    }
    $('.show-more-reviews').on('click', function() {
        $('.review-list').toggle('slow');
        if ($(this).text() == "Show More"){
            $(this).text('Show Less');
        }
        else {
            $(this).text('Show More');
        }
    });

    // toggle to show more/less friends
    if ($('.friend-list').length > 5) {
        $('.friend-list:gt(4)').hide();
        $('.show-more-friends').show();
    }
    else{
        $('.show-more-friends').hide();
    }
    $('.show-more-friends').on('click', function() {
        $('.friend-list:gt(4)').toggle('slow');
        if ($(this).text() == "Show More"){
            $(this).text('Show Less');
        }
        else {
            $(this).text('Show More');
        }
    });

    // toggle to show more/less favorites
    if ($('.favorite-list').length > 5) {
        $('.favorite-list:gt(4)').hide();
        $('.show-more-favorites').show();
    }
    else{
        $('.show-more-favorites').hide();
    }
    $('.show-more-favorites').on('click', function() {
        $('.favorite-list:gt(4)').toggle('slow');
        if ($(this).text() == "Show More"){
            $(this).text('Show Less');
        }
        else {
            $(this).text('Show More');
        }
    });

    $("#details").hide();
    $("#det-btn").on('click', function(){
        $("#details").slideToggle('slow');
    })

    $("#rel-rests").hide();
    $("#btn-suggest-rests").on('click', function(){
        $("#rel-rests").slideToggle('slow');
    })

// update password AJAX validation
    $("#pw_update_form").on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: "/dashboard/user/change_password",
            type:"POST",
            data: $("#pw_update_form").serialize(),
            dataType: 'json',
            success: function (data){
                if (isEmpty(data)){
                    $("#change_password").modal('hide');
                }
                else {
                    for (var k in data){
                        if (k == 'password'){
                            $("#password_error").text(data[k]);
                        }
                        if (k == 'pw_confirm'){
                            $("#pw_confirm_error").text(data[k]);
                        }
                    }
                    $("#change_password").modal('show');
                }
            }
        })
    })

// Update profile AJAX validation
    $("#edit_profile_form").on('submit', function(e){
        e.preventDefault();
        $.ajax({
            url: "/dashboard/user/edit",
            type:"POST",
            data: $("#edit_profile_form").serialize(),
            dataType: 'json',
            success: function (data){
                if (isEmpty(data)){
                    $("#edit_user").modal('hide');
                }
                else {
                    console.log("data", data);
                    for (var k in data){
                        if (k == 'first_name'){
                            $("#first_name_error").text(data[k]);
                        }
                        if (k == 'last_name'){
                            $("#last_name_error").text(data[k]);
                        }
                        if (k == 'username'){
                            $("#username_error").text(data[k]);
                        }
                        if (k == 'email'){
                            $("#email_error").text(data[k]);
                        }
                        if (k == 'birthday'){
                            $("#birthday_error").text(data[k]);
                        }
                    }
                    $("#edit_user").modal('show');
                }
            }
        })
    })

    // function to check if js dictionary is empty
    function isEmpty(ob){
        for(var i in ob){ 
            return false;}
        return true;
    }

    $("#loading-div").toggle();
    $("#new_loc_search").on('submit', function(){
        
        $("#loading-div").slideToggle('slow');
    })

    $( function() {
        $( '[data-toggle="tooltip"]' ).tooltip();
    });

})

