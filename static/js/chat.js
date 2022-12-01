


var chatarea = document.getElementById('chat_textarea');

var doc_url = document.URL;
var user_id = user_id;
var friend = friend_id;
var chat_id = chat_id;

function clearExpiredMessages(){
    var url = '/chat/clear_expired/';
    $.ajax({
        type: 'POST',
        url: url,
        data: {
                        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },

        success : function(data){
        },
        error: function(data){
        }
    })
}


function confirmDelivery(chat_id){
    var url = '/chat/confirm_delivery/' + chat_id;
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

function getUnreadMessages(){
    var url = '/chat/unread_messages/';
    $.ajax({
        type: 'GET',
        url: url,
        data: {

        },
        success: function(data){
            alert_msg = '';
            console.log('unread success');
            console.log(data);
            for (msg of data){
                alert_msg += 'from:';
                alert_msg += msg['sender'];
                alert_msg += '  ';
                alert_msg += 'msg:';
                alert_msg += msg['content'];
                alert_msg += '  ';
                alert_msg += 'chat:';
                alert_msg += msg['chat_id'];
                alert_msg += '\n';
                console.log(msg);
            }
            if (data.length > 0){
                alert('You have unread messages \n' + alert_msg);
            }

        },
        error: function(data){
            console.log('unread error');
            console.log(data);
        }
    })
}

function getMessages(){
    //var url = '/api/messages/';
    var url = '/api/chat/' + chat_id;
    $.ajax({
        type: 'GET',
          url: url,
              data: {
                    chat_id: chat_id,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()},
            success: function(response){
            console.log(response);
            chatarea.value = '';
            for (let key in response['chat_messages']){
                 let msg = '\n' + response['chat_messages'][key].timestamp.replace('T', ' ').slice(0, 16) + '  ' + response['chat_messages'][key].sender + ':   ' + response['chat_messages'][key].content;
                if (response['chat_messages'][key].remaining){
                    msg += '      ' + response['chat_messages'][key].remaining.toString() + ' s';
                }
                var status = 'sent';
                if (response['chat_messages'][key].delivered)
                {
                    status = 'delivered';
                }
                if (response['chat_messages'][key].seen)
                {
                    status = 'seen';
                }
                msg += '                 ' + status;
                chatarea.value += msg;
                setScroll();
            }
            confirmDelivery(chat_id);
            },
        error: function(response){
        //    alert('Error');
        }
    });
}

$(document).on('click', '#msg_text', function(){
    var url = '/chat/confirm_seen/' + chat_id;
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

$(document).on('click', '#rename_button', function(){
    var url = '/api/chat/' + chat_id + '/update_name/';
    var new_name = prompt('Rename chat');
    var crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
    console.log(new_name);
    console.log(crf_token);
    $.ajax({
        url: url,
        type: 'PUT',
        headers:{"X-CSRFToken": crf_token},
        data: {
            chat_name: new_name,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(data){
        console.log('rename success');
        console.log(data);
        location.reload();
        },
        error: function(data){
        console.log('rename error');
        console.log(data);
        }
        });
})


$(document).on('submit', '#msg_form', function(e){
    var url = '/chat/send';
    // var url = '/api/messages/';
    var now = new Date().toISOString().slice(0, 19)
    console.log(user_id);
    e.preventDefault();
    $.ajax({
    type: 'POST',
    url: url,
    data: {
        sender: user_id,
        chat: chat_id,
        content: $('#msg_text').val(),
        timestamp: now,
        destruct_timer: $('#destruct_select').val(),
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function(data){
        getMessages();
    }
    });
    document.getElementById('msg_text').value = '';
});

$(document).ready(function(){
    console.log(typeof(unread_msgs));
    var msgs2 = new Object
    var msg_text = '';
    for (msg in unread_msgs){
        console.log(unread_msgs[msg]);
        //console.log(unread_msgs[msg]);
        msg_text += 'from:' + unread_msgs[msg]['sender'];
    }
    if (unread_msgs){
            alert('You have unread messages.\n' + msg_text);
            }
});

$(document).ready(function(){

    if (chat_id){
            getMessages();
    }
    getUnreadMessages();
    setInterval(getMessages, 10000);
    setInterval(clearExpiredMessages, 5000);
    }
);


