//Inicia socket en localhost:5000
var socket = io.connect('http://' + document.domain + ':' + location.port);

//Cuando un usuario se conecta
socket.on('connect', function () {

    $('div.message_holder').scrollTop(100000)

    //Al hacer click en enviar mensaje
    $('form').on('submit', function (e) {

        e.preventDefault()

        let user_name = nombre
        let user_input = $('input.message').val()

        //Si el mensaje no esta vacio
        if (user_input != "") {

            //Envia nombre de usuario y mensaje al servidor
            socket.emit('event_message', {
                user_name: user_name, message: user_input
            })
        }
        //Limpia el input del mensaje
        $('input.message').val('').focus()
    })
})

//Imprime el mensaje enviado
socket.on('response', function (msg) {

    $('div.mensajes').append('<p><b>' + msg.user_name + ':</b> ' + msg.message + '<br></p>')

    //Scrolea hasta el final
    $('div.message_holder').scrollTop(100000)
})

//Cuando un usuario se conecta o desconecta actualiza la lista de usuarios conectadps
socket.on('users', function (log) {

    //Vacia la lista logueados
    $('div.logueados').empty()

    //Por cada item en la lista
    $.each(log, function () {
        $('div.logueados').append('<p><b>' + this + '</b></p>')
    })
})