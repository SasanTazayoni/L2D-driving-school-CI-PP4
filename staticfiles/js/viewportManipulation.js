document.addEventListener("DOMContentLoaded", function() {
    // Get the navbar and footer elements
    const navbar = document.querySelector(".navbar")
    const footer = document.querySelector(".footer")

    // Get the heights of the navbar and footer
    const navbarHeight = navbar.offsetHeight
    const footerHeight = footer.offsetHeight

    // Calculate the height of the block dynamically
    const block = document.querySelector("[data-block]")
    block.style.height = "calc(100vh - (" + navbarHeight + "px + " + footerHeight + "px))"
})