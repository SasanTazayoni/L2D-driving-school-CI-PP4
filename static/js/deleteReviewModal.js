function showDeleteReviewModal() {
    const deleteReviewButton = document.getElementById('deleteReviewButton')

    if (deleteReviewButton) {
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
}

document.addEventListener('DOMContentLoaded', function() {
    showDeleteReviewModal()
})