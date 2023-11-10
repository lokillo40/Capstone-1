function displayFlashMessage(status, message) {
    // Create a div that will act as the flash message
    const flashMessageDiv = $('<div>')
        .addClass(`alert alert-${status === 'success' ? 'success' : 'danger'}`)
        .html(message);

    
    $('body').prepend(flashMessageDiv);

}

