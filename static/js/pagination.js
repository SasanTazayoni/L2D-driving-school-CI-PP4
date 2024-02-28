const searchForm = document.querySelector('[data-search-form]')
const pageButtons = document.querySelectorAll('.pagination-button')

if (searchForm) {
    pageButtons.forEach(pageButton => {
        pageButton.addEventListener('click', function (e) {
            e.preventDefault()        
            const page = this.dataset.page
            searchForm.innerHTML += `<input value=${page} name="page" hidden/>`
            searchForm.submit()
        })
    })
}