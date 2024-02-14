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

function showDeleteProfileModal() {
    const deleteProfileButton = document.getElementById('deleteProfileButton')
    const deleteProfileModal = new bootstrap.Modal(document.getElementById('deleteProfileModal'))
    const closeModalButton = document.getElementById('closeDeleteProfileModal')

    const openDeleteModal = () => {
        deleteProfileModal.show()
    }

    deleteProfileButton.addEventListener('click', openDeleteModal)

    if (closeModalButton) {
        closeModalButton.addEventListener('click', () => {
            deleteProfileModal.hide()
        })
    }
}

function showDeleteReviewModal() {
    const deleteReviewButton = document.getElementById('deleteReviewButton')
    const deleteReviewModal = new bootstrap.Modal(document.getElementById('deleteReviewModal'))
    const closeModalButton = document.getElementById('closeDeleteReviewModal')

    const openDeleteReviewModal = () => {
        deleteReviewModal.show()
    }

    deleteReviewButton.addEventListener('click', openDeleteReviewModal)

    if (closeModalButton) {
        closeModalButton.addEventListener('click', () => {
            deleteReviewModal.hide()
        })
    }
}

document.addEventListener('DOMContentLoaded', function() {
    initialiseLogoutFunctionality()
    showDeleteProfileModal()
    showDeleteReviewModal()
})