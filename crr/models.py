from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import RegexValidator

# ---------------- VEÍCULO ---------------- #
def upload_path(instance, filename):
    return f"notificacoes/{instance.numero_controle}/{filename}"

ESPECIE_CHOICES = [
    ('passageiro', 'Passageiro'), ('carga', 'Carga'), ('misto', 'Misto'),
    ('tracao', 'Tração'), ('colecao', 'Coleção'), ('especial', 'Especial'),
]

CATEGORIA_CHOICES = [
    ('oficial', 'Oficial'), ('particular', 'Particular'), ('aluguel', 'Aluguel'),
]

ESTADO_CHOICES = [
    ('AC', 'Acre'),   ('AL', 'Alagoas'),('AP', 'Amapá'),('AM', 'Amazonas'),
    ('BA', 'Bahia'),('CE', 'Ceará'),('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'), ('MA', 'Maranhão'),('MT', 'Mato Grosso'),('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),('PA', 'Pará'),('PB', 'Paraíba'),('PR', 'Paraná'),('PE', 'Pernambuco'),
    ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),('RN', 'Rio Grande do Norte'),('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'),
      ('SE', 'Sergipe'),('TO', 'Tocantins'),('OUTROS', 'Outros'),
]

STATUS_CHOICES = [  ('retido', 'Retido'), ('liberado', 'Liberado'),]

PLACA_REGEX = r'^([A-Z]{3}-\d{4}|[A-Z]{3}-\d[A-Z]\d{2}|[A-Za-z0-9]{17})$' 
CPF_REGEX = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'

class Crr(models.Model):
    
    
    numero_crr = models.CharField(max_length=10, blank=False, null=False)
    placa_chassi = models.CharField( max_length=17,validators=[RegexValidator(regex=PLACA_REGEX, message='Formato inválido. Use: AAA-1234, AAA-1A23 ou 17 caracteres alfanuméricos')],blank=False, null=False)
    marca = models.CharField(max_length=20, blank=False, null=False)
    modelo = models.CharField(max_length=20, blank=False, null=False)
    especie = models.CharField(max_length=20 ,choices=ESPECIE_CHOICES, blank=False, null=False)
    categoria = models.CharField(max_length=20,choices=CATEGORIA_CHOICES, blank=False, null=False)
    uf_veiculo = models.CharField(max_length=6, choices=ESTADO_CHOICES,default='SP', blank=False, null=False)
    municipio_veiculo = models.CharField(max_length=25, blank=False, null=False)
    local_remocao = models.CharField(max_length=100, blank=False, null=False)
    data_remocao = models.DateField(blank=False, null=False)
    hora_remocao = models.TimeField(blank=False, null=False)
    observacao = models.CharField(max_length=100, blank=True, null=True)
    agente_autuador = models.CharField(max_length=10, blank=False, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='retido',help_text="Status atual do veículo (Retido/Liberado)")

    # ---------------- CONDUTOR ---------------- #
    habilitacao_condutor = models.CharField(max_length=11, blank=True, null=False)
    uf_cnh = models.CharField(max_length=6,choices=ESTADO_CHOICES,default='SP', blank=True, null=False)
    cpf = models.CharField(max_length=14,validators=[RegexValidator(regex=CPF_REGEX, message='CPF deve estar no formato 000.000.000-00')],unique=True,verbose_name='CPF', blank=True, null=False)
    nome_condutor = models.CharField(max_length=50, blank=True, null=False)

    def __str__(self):
         return f"CRR {self.numero_crr} - {self.placa_chassi}" 

class Ait(models.Model):
    AIT_REGEX = r'^[A-Z]\d{2}-\d{7}$'  # Padrão A12-0123456
    crr = models.ForeignKey(Crr,on_delete=models.CASCADE,related_name='ait')
    ait = models.CharField(max_length=11,validators=[RegexValidator(regex=AIT_REGEX,message='Formato inválido. Use: ''A12-0123456')],
    verbose_name='Código de AIT',help_text='Formato: Letra + 2 números + hífen + 7 números (Ex: A12-0123456)', blank=True, null=False
    )   
    def __str__(self):
        return self.ait
    
class Enquadramento(models.Model):    
    crr = models.ForeignKey(Crr,on_delete=models.CASCADE,related_name='enquadramento')
    enquadramento = models.CharField(max_length=5,blank=True, null=False)
    verbose_name='Código de enquadramento'     
    def __str__(self):
        return self.enquadramento


# ---------------- NOTIFICAÇÃO ---------------- #
CEP_REGEX = r'^\d{5}-\d{3}$'

class Notificacao(models.Model):
    AMPAROS_PREDEFINIDOS = [
        ('Art. 279-A C.T.B.', 'Art. 279-A C.T.B.'),
        ('Art. 230, V - C.T.B.', 'Art. 230, V - C.T.B.'),
    ]
    
    crr = models.OneToOneField(Crr, on_delete=models.CASCADE,related_name="notificacao")
    data_emissao = models.DateField(blank=False, null=False)
    data_postagem = models.DateField(blank=False, null=False)
    numero_controle = models.CharField(max_length=7, unique=True, blank=False)
    descricao_infracao = models.CharField(max_length=100, blank=True, null=False)
    amparo_legal = models.CharField(max_length=25, blank=False, null=False)
    prazo_leilao = models.DateField(blank=False, null=False)
    destinatario = models.CharField(max_length=25, blank=False, null=False)
    endereco = models.CharField(max_length=25, blank=False, null=False)
    numero = models.CharField(max_length=6, blank=False, null=False)
    complemento = models.CharField(max_length=10, blank=True, null=False)
    bairro = models.CharField(max_length=25, blank=False, null=False)
    cidade_destinatario = models.CharField(max_length=25, blank=False, null=False)
    uf_destinatario = models.CharField(max_length=6,choices=ESTADO_CHOICES, blank=False, null=False)
    cep = models.CharField(max_length=9,validators=[RegexValidator(regex=CEP_REGEX,message='CEP deve estar no formato 11600-000')],verbose_name='CEP',help_text='Formato: 11600-000')
    imagem = models.ImageField(upload_to=upload_path, blank=True, null=False, verbose_name="Imagem da Notificação")
    criado_em = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if not self.numero_controle:
            last_notificacao = Notificacao.objects.order_by('-id').first()
            last_number = int(last_notificacao.numero_controle) if last_notificacao else 0
            self.numero_controle = f"{last_number + 1:07d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Notificação {self.numero_controle} - {self.data_emissao}"
