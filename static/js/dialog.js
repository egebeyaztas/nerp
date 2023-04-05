$(document).ready(function() {
    const modal = $('#modal');
    htmx.on('htmx:afterSwap', (e) => {
        if(e.detail.target.id === 'dialog') {
            $('#modal').css('display','flex')
        }
    })
})
$(document).ready(function() {
    htmx.on('htmx:beforeSwap', (e) => {
        if(e.detail.target.id === 'dialog' && !e.detail.xhr.response) {
            console.log('closed')
            $('#modal').css('display','none')
        }
    })
})







