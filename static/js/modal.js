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

function showDeleteProfileModal() {
    const deleteButton = document.getElementById('deleteButton')
    const deleteProfileModal = new bootstrap.Modal(document.getElementById('deleteProfileModal'))
    const closeModalButton = document.getElementById('closeDeleteProfileModal')

    const openDeleteModal = () => {
        deleteProfileModal.show()
    }

    deleteButton.addEventListener('click', openDeleteModal)

    if (closeModalButton) {
        closeModalButton.addEventListener('click', () => {
            deleteProfileModal.hide()
        })
    }
}

document.addEventListener('DOMContentLoaded', function() {
    initialiseLogoutFunctionality()
    showDeleteProfileModal()
})