"""
Banco de questões do questionário educacional sobre legislação de trânsito
(baseado no material av1_taxistas).

Cada questão possui:
- id: identificador sequencial (1 a 10)
- enunciado: texto da pergunta
- imagem: caminho estático da imagem (em educacional/static/educacional/img/),
  ou None se a questão não tiver imagem
- alternativas: dicionário {"A": "...", "B": "...", "C": "...", "D": "..."}
- correta: letra da alternativa correta (gabarito)
"""

QUESTOES = [
    {
        'id': 1,
        'enunciado': 'Segundo o Código de Trânsito Brasileiro, considera-se trânsito:',
        'imagem': None,
        'alternativas': {
            'A': 'Apenas a circulação de veículos automotores.',
            'B': 'A circulação de veículos em vias urbanas.',
            'C': 'A utilização das vias por pessoas, veículos e animais para fins de '
                 'circulação, parada, estacionamento e operação de carga ou descarga.',
            'D': 'Apenas a circulação de pedestres e veículos.',
        },
        'correta': 'C',
    },
    {
        'id': 2,
        'enunciado': 'Antes de colocar o veículo em circulação, o condutor deverá:',
        'imagem': None,
        'alternativas': {
            'A': 'Verificar apenas os pneus.',
            'B': 'Verificar apenas a documentação do veículo.',
            'C': 'Verificar os equipamentos obrigatórios e assegurar combustível '
                 'suficiente para chegar ao destino.',
            'D': 'Verificar somente o sistema de iluminação.',
        },
        'correta': 'C',
    },
    {
        'id': 3,
        'enunciado': 'Qual das alternativas representa um dever do taxista?',
        'imagem': None,
        'alternativas': {
            'A': 'Utilizar o celular sempre que necessário.',
            'B': 'Priorizar a rapidez da viagem em detrimento da segurança.',
            'C': 'Conduzir com prudência e garantir a segurança do passageiro.',
            'D': 'Estacionar em qualquer local para embarque e desembarque.',
        },
        'correta': 'C',
    },
    {
        'id': 4,
        'enunciado': 'Observe a placa abaixo. O significado da placa é:',
        'imagem': 'educacional/img/placa_pare.png',
        'alternativas': {
            'A': 'Reduzir a velocidade.',
            'B': 'Dar preferência aos veículos da direita.',
            'C': 'Parada obrigatória antes de prosseguir.',
            'D': 'Proibido estacionar.',
        },
        'correta': 'C',
    },
    {
        'id': 5,
        'enunciado': 'Observe a placa abaixo. Esta sinalização determina que o condutor:',
        'imagem': 'educacional/img/placa_dar_preferencia.png',
        'alternativas': {
            'A': 'Deve parar obrigatoriamente.',
            'B': 'Deve conceder preferência aos veículos que transitam na via preferencial.',
            'C': 'Pode seguir sem reduzir a velocidade.',
            'D': 'Deve realizar retorno obrigatório.',
        },
        'correta': 'B',
    },
    {
        'id': 6,
        'enunciado': 'Observe a placa abaixo. Um taxista deixa o veículo aguardando '
                      'passageiros nesse local. Sua conduta:',
        'imagem': 'educacional/img/placa_proibido_estacionar.png',
        'alternativas': {
            'A': 'É permitida por ser veículo de transporte público.',
            'B': 'É permitida se permanecer dentro do veículo.',
            'C': 'Configura estacionamento em desacordo com a sinalização.',
            'D': 'É permitida por até cinco minutos.',
        },
        'correta': 'C',
    },
    {
        'id': 7,
        'enunciado': 'Observe a placa abaixo. O significado correto é:',
        'imagem': 'educacional/img/placa_proibido_parar_estacionar.png',
        'alternativas': {
            'A': 'Proibido apenas estacionar.',
            'B': 'Permitido embarque e desembarque.',
            'C': 'Proibido parar e estacionar.',
            'D': 'Permitido apenas para táxis.',
        },
        'correta': 'C',
    },
    {
        'id': 8,
        'enunciado': 'Observe a placa abaixo. A sinalização informa:',
        'imagem': 'educacional/img/placa_velocidade_60.png',
        'alternativas': {
            'A': 'Velocidade mínima de 60 km/h.',
            'B': 'Velocidade recomendada de 60 km/h.',
            'C': 'Velocidade máxima permitida de 60 km/h.',
            'D': 'Velocidade média da via.',
        },
        'correta': 'C',
    },
    {
        'id': 9,
        'enunciado': 'Um taxista possui registro EAR (Exerce Atividade Remunerada) em sua '
                      'CNH e atingiu 30 pontos no período de 12 meses. Segundo o CTB, ele poderá:',
        'imagem': None,
        'alternativas': {
            'A': 'Solicitar o cancelamento dos pontos.',
            'B': 'Realizar curso preventivo de reciclagem.',
            'C': 'Renovar a CNH antecipadamente.',
            'D': 'Transferir a pontuação para outro condutor.',
        },
        'correta': 'B',
    },
    {
        'id': 10,
        'enunciado': 'Um condutor possui 43 pontos registrados em seu prontuário. Entretanto, '
                      'a infração mais antiga ocorreu há mais de 15 meses. Para fins de análise '
                      'da suspensão por pontuação deverão ser considerados:',
        'imagem': None,
        'alternativas': {
            'A': 'Todos os pontos existentes no prontuário.',
            'B': 'Apenas os pontos dos últimos 12 meses.',
            'C': 'Apenas as infrações gravíssimas.',
            'D': 'Apenas as infrações cometidas no ano civil.',
        },
        'correta': 'B',
    },
]


def get_gabarito():
    """Retorna {numero_questao_str: alternativa_correta}."""
    return {str(q['id']): q['correta'] for q in QUESTOES}
