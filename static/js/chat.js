


var chatarea = document.getElementById('chat_textarea');

var doc_url = document.URL;
var friend = friend_id;


function confirmDelivery(friend_id){
    var url = '/chat/confirm_delivery/' + friend_id;
    $.ajax({
                type: 'POST',
                url: url,
                data: {
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data){
                //getMessages();
            },
            error: function(data){
                //alert('Error');
            }
        })
}


function addFriend(friend_id){
    $.ajax({
    type: 'POST',
    url: '/chat/addFriend/' + friend_id,
    success: function(response){
            return;
            }
        }
    )
    }

function setScroll(){
    var $textarea = $('#chat_textarea');
    $textarea.scrollTop($textarea[0].scrollHeight);
}

function getMessages(){
    var url = '/api/messages/';
    $.ajax({
        type: 'GET',
          url: url,
              data: {
                    friend_id: friend_id,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
            success: function(response){
            chatarea.value = '';
            for (let key in response){
                 let msg = '\n' + response[key].timestamp.replace('T', ' ').slice(0, 16) + '  ' + response[key].sender_id + ':   ' + response[key].content;
                if (response[key].destruct_timer != 0){
                    msg += '      ' + response[key].destruct_timer.toString() + ' s';
                }
                var status = 'sent';
                if (response[key].delivered)
                {
                    status = 'delivered';
                }
                if (response[key].seen)
                {
                    status = 'seen';
                }
                msg += '  ' + status;
                chatarea.value += msg;
                setScroll();
            }
            confirmDelivery(friend_id);
            },
        error: function(response){
        //    alert('Error');
        }
    });
}

$(document).on('click', '#msg_text', function(){
    var url = '/chat/confirm_seen/' + friend_id;
    $.ajax({
    type: 'POST',
    url: url,
    data: {
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    },
    success: function(data){
        getMessages();
    }
    })
})


$(document).on('submit', '#msg_form', function(e){
    var url = '/chat/send';
    e.preventDefault();
    $.ajax({
    type: 'POST',
    url: url,
    data: {
        friend_id: friend_id,
        msg_text: $('#msg_text').val(),
        destr_timer: $('#destruct_select').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function(data){
        getMessages();
    }
    });
    document.getElementById('msg_text').value = '';
});


$(document).ready(function(){
    if (friend_id){
            getMessages();
    }
    setInterval(getMessages, 10000);
    }
);


