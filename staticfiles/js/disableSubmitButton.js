/* jshint esversion: 11 */

document.addEventListener("DOMContentLoaded", function() {
    var submitButton = document.getElementById("submitButton");
    var resetForm = document.getElementById("resetForm");

    submitButton.addEventListener("click", function() {
        submitButton.disabled = true;
        resetForm.submit();
    });

    setTimeout(function() {
        submitButton.disabled = false;
    }, 3000);
});