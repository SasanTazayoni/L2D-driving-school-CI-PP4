document.addEventListener('DOMContentLoaded', function () {
    function generateStarRating(rating, container) {
        container.innerHTML = ''
        const yellowStars = rating
        const greyStars = 5 - rating

        // Add yellow stars
        for (let i = 0; i < yellowStars; i++) {
            const star = document.createElement('img')
            star.src = '../static/images/star.png'
            star.style.width = '25px'
            star.style.height = '25px'
            star.style.margin = '5px 0'
            container.appendChild(star)
        }

        // Add grey stars
        for (let i = 0; i < greyStars; i++) {
            const star = document.createElement('img')
            star.src = '../static/images/greystar.png'
            star.style.width = '25px'
            star.style.height = '25px'
            star.style.margin = '5px 0'
            container.appendChild(star)
        }
    }

    const ratingElements = document.querySelectorAll('[data-rating]')

    ratingElements.forEach(function(element) {
        const ratingValue = parseInt(element.innerText.trim())
        generateStarRating(ratingValue, element)
    })
})