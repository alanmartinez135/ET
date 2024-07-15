$(document).ready(function() {
    /* FUNCION PARA VALIDACIONES DE REGISTRO*/
    /*para que se pueda validar la estructura del correo*/
    var expr = /^[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9_\-]+\.[a-zA-Z0-9_\-\.]+$/;

    $("#registroForm").submit(function(event) {
        // Evitar que el formulario se envíe automáticamente
        event.preventDefault();
        
        // Realizar las validaciones de registro
        var nombre = $("#InputUsuario").val();
        var correo = $("#InputEmail1").val();
        var run = $("#run").val();
        var contrasena1 = $("#InputPassword1").val();
        var check = $("#Check1").prop("checked");

        // Limpiar mensajes previos
        $("#mensajeAlerta").hide().text("");

        // Validación de usuario
        if (nombre.length < 3 || nombre.length > 20) {
            mostrarMensaje("El nombre de usuario debe tener entre 3 y 20 caracteres.");
            return false;
        }

        // Validación de correo
        if (correo === "" || !expr.test(correo) || correo.length < 10 || correo.length > 30) {
            mostrarMensaje("El correo electrónico debe ser válido y tener entre 10 y 30 caracteres.");
            return false;
        }

        // Verificar si el correo termina con .com o .cl
        var dominioValido = /\.com$|\.cl$/;
        if (!dominioValido.test(correo)) {
            mostrarMensaje("El correo debe terminar en .com o .cl.");
            return false;
        }

        // Validación de RUT
        if (run.length < 8 || run.length > 9) {
            mostrarMensaje("El RUT debe tener entre 8 y 9 caracteres.");
            return false;
        }

        // Validación de contraseña
        if (contrasena1.length < 8 || contrasena1.length > 15) {
            mostrarMensaje("La contraseña debe tener entre 8 y 15 caracteres.");
            return false;
        }

        // Validación de aceptación de términos y condiciones
        if (!check) {
            mostrarMensaje("Debe aceptar los términos y condiciones.");
            return false;
        }

        // Si todas las validaciones pasan, enviar el formulario
        alert("Registro exitoso");
        this.submit();
    });

    function mostrarMensaje(mensaje) {
        $("#mensajeAlerta").text(mensaje).fadeIn();
    }
});
