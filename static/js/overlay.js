/* jshint esversion: 11 */

document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.querySelector('.overlay')
    if (overlay) {
        setTimeout(() => {
            overlay.classList.add('active')
        }, 3000)
    }
})