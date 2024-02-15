document.addEventListener('DOMContentLoaded', function () {
    if (window.location.pathname.endsWith('/profile/edit/')) {  
        const imageDiv = document.querySelector('#profile_picture-clear_id')
        const imageDivParent = imageDiv.parentNode
        const firstAnchorChild = imageDivParent.querySelector('a')
        const textNode = document.createTextNode('Current: ')
        let hrefValue = ''

        if (firstAnchorChild && firstAnchorChild.href.includes('cloudinary')) {
            hrefValue = firstAnchorChild.href
        }

        const imgElement = document.createElement('img')
        imgElement.src = hrefValue

        imgElement.style.borderRadius = '20px'
        imgElement.style.objectFit = 'cover'
        imgElement.style.objectPosition = 'center'
        imgElement.style.height = '200px'
        imgElement.style.width = '200px'
        imgElement.style.margin = '20px'

        for (let i = 0; i < 8; i++) {
            imageDivParent.removeChild(imageDivParent.firstChild)
        }
        imageDivParent.insertBefore(imgElement, imageDivParent.firstChild)
        imageDivParent.insertBefore(textNode, imgElement)
    }
})