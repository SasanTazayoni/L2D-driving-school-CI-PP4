const logoutLink = document.querySelector('#logoutLink')
const logoutBtn = document.querySelector('#logoutBtn')
const logoutModal = new bootstrap.Modal(document.getElementById('logoutConfirmationModal'))
const closeModalButton = document.getElementById('closeModalButton')

logoutLink.addEventListener('click', (e) => {
    e.preventDefault()
    logoutModal.show()
})

logoutBtn.addEventListener('click', (e) => {
    e.preventDefault()
    logoutModal.show()
})

closeModalButton.addEventListener('click', () => {
    logoutModal.hide()
})