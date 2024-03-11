/* jshint esversion: 11 */

document.addEventListener('DOMContentLoaded', () => {
    const positionAlertContainer = () => {
        const navbarHeight = document.querySelector('.navbar').offsetHeight;
        const alertContainer = document.querySelector('[data-alert]');
        alertContainer.style.top = `${navbarHeight + 10}px`;
    };

    // Call the function when the document is ready and if the window is resized
    positionAlertContainer();
    window.addEventListener('resize', positionAlertContainer);

    const alertElements = document.querySelectorAll('[data-alert] .alert');
    alertElements.forEach((alertElement) => {
        setTimeout(() => {
            alertElement.remove();
        }, 7000);
    });
});