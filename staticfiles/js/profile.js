

document.addEventListener('DOMContentLoaded', function () {
    if (window.location.pathname.endsWith('/profile/edit/')) {
        // select the image div containers, and get the image href/url
        const imageDiv = document.querySelector('#div_id_profile_picture')
        const imageSrcDiv = imageDiv.querySelector('.input-group')
        const imageSrc = imageDiv.querySelector('a')

        // change the image src div to show the image
        imageSrcDiv.innerHTML = `<div class="col-12">Current Image:<img style="display: block;" src="${imageSrc.href}"></div>`
    }
})