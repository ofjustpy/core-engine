
// {% raw %}
/**
 * justpy event handler
 */

function eventHandler(event) {
    let event_type = event.type;
    
    e = {
        'event_type': event_type,
        'id': event.currentTarget.id,
        'checked': event.target.checked,
        'data': event.data,
        'value': event.target.value,
        'page_id': justpy_core.page_id,
        'websocket_id': websocket_id,
    };
    send_to_server(e, 'event');
}

/**
 * send given event data to the justpy server
 * @param e - event data
 * @param {string} event_type - type of the event
 * @param {boolean} debug_flag - If true show debug messages in the console
 */
function send_to_server(e, event_type, debug_flag) {

    if (use_websockets) {
        if (web_socket_closed) {
            if (debug_flag) {
                console.log('Abort send_to_server (web socket is closed) → reloading site');
            }
            reload_site();
            return;
        }
        const data = JSON.stringify({'type': event_type, 'event_data': e});
        if (websocket_ready) {
          socket.send(JSON.stringify({'type': event_type, 'event_data': e, 'csrftoken': 'somevalue'}));
        } else {
            setTimeout(function () {
                socket.send(data);
            }, 1000);
        }
    } 
}

// {% endraw %}
