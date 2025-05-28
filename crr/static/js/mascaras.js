document.addEventListener('DOMContentLoaded', function () {
    // === PLACEHOLDERS ===
    const placeholders = {
        // CRR
        'id_numeroCrr': 'Somente números',
        
        'id_dataFiscalizacao': 'dd/mm/aaaa',
        'id_horaFiscalizacao': 'hh:mm',
        'id_matriculaAgente': 'Somente números',
        'id_localPatio': 'Local do Pátio',
        'id_placaGuincho': 'Placa do Guincho',
        'id_encarregado': 'Encarregado do Guincho',

        'id_ait': 'A43-0123456',
        'id_enquadramento': 'Somente números',
        
        // VEÍCULO
        'id_placa': 'Placa',
        'id_chassi': 'Placa ou Chassi',

        // CONDUTOR
        'id_habilitacao_condutor': 'Somente números',
        'id_cpf': '000.000.000-00',
       
        

        // ARRENDATÁRIO
         'id_cnpj_arrendatario': '00.000.000/0000-00',
        'id_numero_arrendatario': 'Somente números',
        'id_cep_arrendatario': '00000-000',

        //NOTIFICAÇÃO
        'id_data_emissao': 'dd/mm/aaaa',
        'id_data_postagem': 'dd/mm/aaaa',
        'id_numero_controle': 'Somente números',
        'id_prazo_leilao': 'dd/mm/aaaa',
        'id_numero': 'Somente números',
        'id_cep': '00000-000'
    };

    for (const [id, text] of Object.entries(placeholders)) {
        const field = document.getElementById(id);
        if (field) {
            field.setAttribute('placeholder', text);
        }
    }

    // === MÁSCARAS ===
    function applyMask(input, maskFunction) {
        input.addEventListener('input', function (e) {
            e.target.value = maskFunction(e.target.value);
        });
    }

    function maskCPF(value) {
        return value.replace(/\D/g, '')
                    .replace(/(\d{3})(\d)/, '$1.$2')
                    .replace(/(\d{3})(\d)/, '$1.$2')
                    .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    }

    function maskCNPJ(value) {
        return value.replace(/\D/g, '')
                    .replace(/(\d{2})(\d)/, '$1.$2')
                    .replace(/(\d{3})(\d)/, '$1.$2')
                    .replace(/(\d{3})(\d)/, '$1/$2')
                    .replace(/(\d{4})(\d{1,2})$/, '$1-$2');
    }

    function maskCEP(value) {
        return value.replace(/\D/g, '')
                    .replace(/(\d{5})(\d)/, '$1-$2');
    }

    function maskDate(value) {
        return value.replace(/\D/g, '')
                    .replace(/(\d{2})(\d)/, '$1/$2')
                    .replace(/(\d{2})(\d)/, '$1/$2');
    }

    function maskTime(value) {
        return value.replace(/\D/g, '')
                    .replace(/(\d{2})(\d)/, '$1:$2');
    }

    function maskAIT(value) {
        return value.replace(/\W/g, '')
                    .replace(/^([A-Za-z])(\d{2})(\d+)/, '$1$2-$3')
                    .toUpperCase();
    }

    function maskPlaca(value) {
        return value.replace(/[^A-Za-z0-9]/g, '').toUpperCase();
    }

    function onlyNumbers(value) {
        return value.replace(/\D/g, '');
    }

    const masks = {
        'id_numeroCrr': onlyNumbers,
        'id_dataFiscalizacao': maskDate,
        'id_horaFiscalizacao': maskTime,
        'id_placaGuincho': maskPlaca,
        'id_matriculaAgente': onlyNumbers,

        'id_placa': maskPlaca,

        'id_cnpj_arrendatario': maskCNPJ,
        'id_cep_arrendatario': maskCEP,
        'id_cep': maskCEP,
        'id_numero_arrendatario': onlyNumbers,
        
        'id_numero': onlyNumbers,

        'id_ait': maskAIT,
        'id_enquadramento': onlyNumbers,
        
        'id_data_emissao': maskDate,
        'id_data_postagem': maskDate,
        'id_prazo_leilao': maskDate,
        'id_numero_controle': onlyNumbers,

        'id_cnh': onlyNumbers,
        'id_cpfCondutor': maskCPF
    };

    for (const [id, maskFunc] of Object.entries(masks)) {
        const field = document.getElementById(id);
        if (field) {
            applyMask(field, maskFunc);
        }
    }

    // === VALIDAÇÕES ANTES DE ENVIAR O FORMULÁRIO ===
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function (e) {
            let valid = true;
            const errors = [];

            function validateLength(id, length, name) {
                const value = document.getElementById(id)?.value.replace(/\D/g, '') || '';
                if (value.length !== length) {
                    errors.push(`${name} deve conter ${length} dígitos.`);
                    valid = false;
                }
            }

            validateLength('id_cpf', 11, 'CPF');
            validateLength('id_cnpj_arrendatario', 14, 'CNPJ');
            validateLength('id_cep_arrendatario', 8, 'CEP do arrendatário');
            validateLength('id_cep', 8, 'CEP');
            validateLength('id_numero_arrendatario', 1, 'Número do arrendatário'); // Opcional ajustar conforme sua regra
            //validateLength('id_numero_controle', 1, 'Número de controle'); // Opcional ajustar conforme sua regra

            if (!valid) {
                e.preventDefault();
                alert(errors.join('\n'));
            }
        });
    }

});

function aplicarMascaras(contexto) {
    contexto.querySelectorAll('input[name$="ait"]').forEach(function(input) {
        input.placeholder = "A43-0123456";
        input.addEventListener('input', function () {
            this.value = this.value.toUpperCase().replace(/[^A-Z0-9-]/g, '').replace(/([A-Z0-9]{3})([0-9]{7})/, '$1-$2');
        });
    });

    contexto.querySelectorAll('input[name$="enquadramento"]').forEach(function(input) {
        input.placeholder = "Somente números";
        input.addEventListener('input', function () {
            this.value = this.value.replace(/\D/g, '');
        });
    });

    contexto.querySelectorAll('input[name$="cnpj_arrendatario"]').forEach(function(input) {
        input.placeholder = "00.000.000/0000-00";
        input.addEventListener('input', function () {
            let v = this.value.replace(/\D/g, '');
            this.value = v
                .replace(/^(\d{2})(\d)/, "$1.$2")
                .replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
                .replace(/\.(\d{3})(\d)/, ".$1/$2")
                .replace(/(\d{4})(\d{2})$/, "$1-$2");
        });
    });

    contexto.querySelectorAll('input[name$="numero_arrendatario"], input[name$="cep_arrendatario"]').forEach(function(input) {
        input.placeholder = input.name.includes('cep') ? "00000-000" : "Somente números";
        input.addEventListener('input', function () {
            this.value = this.name.includes('cep') ?
                this.value.replace(/\D/g, '').replace(/^(\d{5})(\d)/, "$1-$2") :
                this.value.replace(/\D/g, '');
        });
    });
}

// Ao carregar a página
document.addEventListener('DOMContentLoaded', function () {
    aplicarMascaras(document);

    // Quando adicionar novo inline
    document.body.addEventListener('click', function (event) {
        if (event.target && event.target.classList.contains('add-row')) {
            setTimeout(function () {
                aplicarMascaras(document);
            }, 100); // pequeno delay para garantir que o campo exista
        }
    });
});

// === REMOVER MÁSCARAS e NORMALIZAR ===
const normalizeFields = [
    
    'id_cnpj_arrendatario',
    'id_cep_arrendatario',
    'id_numero_arrendatario',
    'id_numero_controle',
    'id_numero',
    'id_enquadramento',
    'id_matriculaAgente',
    
    'id_placa',
    'id_chassi',
    'id_municipioVeiculo',
    'id_ufVeiculo',
    'id_endereco',
    'id_bairro',
    'id_cidade_destinatario',
    'id_destinatario',
    'id_nomeCondutor',
    'id_cnh',
    'id_cpfCondutor',
    
    
];

normalizeFields.forEach(id => {
    const field = document.getElementById(id);
    if (field) {
        // Remove caracteres não numéricos se for numérico, senão coloca em minúsculo
        const onlyDigits = ['cpfCondutor', 'cnpj', 'cep', 'numero', 'enquadramento', 'matriculaAgente', 'cnh'].some(k => id.includes(k));
        if (onlyDigits) {
            field.value = field.value.replace(/\D/g, '');
        } else {
            field.value = field.value.toLowerCase();
        }
    }
});
