function initialiseLogoutFunctionality() {
    const logoutLink = document.getElementById('logoutLink')
    const logoutBtn = document.getElementById('logoutBtn')
    const logoutModal = new bootstrap.Modal(document.getElementById('logoutConfirmationModal'))
    const closeLogoutModal = document.getElementById('closeLogoutModal')

    const openLogoutModal = () => {
        logoutModal.show()
    }

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

    if (closeLogoutModal) {
        closeLogoutModal.addEventListener('click', () => {
            logoutModal.hide()
        })
    }
}

document.addEventListener('DOMContentLoaded', function() {
    initialiseLogoutFunctionality()
})