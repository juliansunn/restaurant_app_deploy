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
        console.log('here');
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
    

})

