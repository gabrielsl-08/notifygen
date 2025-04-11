document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('id_amparo_legal');
    if (input) {
        input.addEventListener('focus', function() {
            this.setAttribute('autocomplete', 'off');
        });
    }
});