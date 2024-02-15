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

document.addEventListener('DOMContentLoaded', function() {
    showDeleteProfileModal()
})