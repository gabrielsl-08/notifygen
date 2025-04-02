// static/js/amparo_legal.js
document.addEventListener('DOMContentLoaded', function() {
    const input = document.querySelector('[list="amparoLegalOptions"]');
    if (input) {
        input.addEventListener('input', function(e) {
            console.log('Valor selecionado/digitado:', e.target.value);
            // Adicione lógica adicional aqui (ex: validação)
        });
    }
});