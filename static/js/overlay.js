document.addEventListener("DOMContentLoaded", function() {
    const overlay = document.querySelector('.overlay')

    if (overlay) {
        setTimeout(function() {
            overlay.classList.add('active')
        }, 3000)
    }
})