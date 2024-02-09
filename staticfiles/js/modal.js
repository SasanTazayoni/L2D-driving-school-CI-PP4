function initialiseLogoutFunctionality() {
    const logoutLink = document.getElementById('logoutLink')
    const logoutBtn = document.getElementById('logoutBtn')
    const logoutModal = new bootstrap.Modal(document.getElementById('logoutConfirmationModal'))

    // Function to open the logout modal
    const openLogoutModal = () => {
        logoutModal.show()
    }

    // Event listeners for both logout link and logout button
    if (logoutLink) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault()
            openLogoutModal()
        })
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault()
            openLogoutModal()
        })
    }
}

// Call the function when the DOM content is loaded
document.addEventListener('DOMContentLoaded', initialiseLogoutFunctionality)