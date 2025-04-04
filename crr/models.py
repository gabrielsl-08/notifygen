from django.db import models, transaction
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# ---------------- VEÍCULO ---------------- #
def upload_path(instance, filename):
    numero_crr = instance.numero_crr if instance.numero_crr else "sem_identificacao"
    return f"notificacoes/{numero_crr}/{filename}"

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



class Crr(models.Model):
    numero_crr = models.CharField(max_length=10,unique=True, blank=False, null=False,verbose_name='número do crr')
    placa_chassi = models.CharField( max_length=17,blank=True, null=False,verbose_name='placa~chassi')
    marca = models.CharField(max_length=20, blank=True, null=False)
    modelo = models.CharField(max_length=20, blank=True, null=False)
    especie = models.CharField(max_length=20 ,choices=ESPECIE_CHOICES, blank=True, null=False)
    categoria = models.CharField(max_length=20,choices=CATEGORIA_CHOICES, blank=True, null=False)
    uf_veiculo = models.CharField(max_length=6, choices=ESTADO_CHOICES,default='SP', blank=True, null=False)
    municipio_veiculo = models.CharField(max_length=25, blank=False, null=False)
    local_remocao = models.CharField(max_length=100, blank=False, null=False)
    data_remocao = models.DateField(blank=False, null=False)
    hora_remocao = models.TimeField(blank=False, null=False)
    observacao = models.CharField(max_length=100, blank=True, null=False, default='abandonado')
    agente_autuador = models.CharField(max_length=10, blank=False, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='retido',help_text="Status atual do veículo (Retido/Liberado)")    
    habilitacao_condutor = models.CharField(max_length=11, blank=True, null=False)
    uf_cnh = models.CharField(max_length=6,choices=ESTADO_CHOICES,default='SP', blank=True, null=False)
    cpf = models.CharField(max_length=14,verbose_name='CPF', blank=True, null=False)
    nome_condutor = models.CharField(max_length=50, blank=True, null=False)
    not_gerada = models.BooleanField(default=True) 
    criado_em = models.DateTimeField(auto_now_add=True)
    editado_em = models.DateTimeField(auto_now=True)
 
    def __str__(self):
         return f"CRR {self.numero_crr} - {self.placa_chassi}" 
    
    def atualizar_status_not_gerada(self):
        """Atualiza automaticamente se a notificação já foi gerada."""
        if hasattr(self, 'notificacao'):  # Verifica se já há uma Notificação vinculada
            self.not_gerada = False
        else:
            self.not_gerada = self.data_remocao <= (date.today() - timedelta(days=10))
        self.save()
    
   
    

class Ait(models.Model):
    crr = models.ForeignKey(Crr,on_delete=models.CASCADE,related_name='ait')
    ait = models.CharField(max_length=11,verbose_name='Código de AIT', blank=True, null=False)   
    def __str__(self):
        return self.ait
    
    
class Enquadramento(models.Model):    
    crr = models.ForeignKey(Crr,on_delete=models.CASCADE,related_name='enquadramento')
    enquadramento = models.CharField(max_length=5,blank=True, null=False)
    verbose_name='Código de enquadramento'     
    def __str__(self):
        return self.enquadramento


class Notificacao(models.Model):
    AMPAROS_PREDEFINIDOS = [
        ('Art. 279-A C.T.B.', 'Art. 279-A C.T.B.'),
        ('Art. 230, V - C.T.B.', 'Art. 230, V - C.T.B.'),
    ]
    
    crr = models.OneToOneField(Crr, on_delete=models.CASCADE,related_name="notificacao")
    data_emissao = models.DateField(blank=False, null=False)
    data_postagem = models.DateField(blank=False, null=False)
    numero_controle = models.PositiveIntegerField(unique=True, blank=True, null=True)
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
    cep = models.CharField(max_length=9,verbose_name='CEP',help_text='Formato: 11600-000')
    imagem = models.ImageField(upload_to='notifcacoes/', blank=True, null=False, verbose_name="Imagem da Notificação")
    criado_em = models.DateTimeField(auto_now_add=True)
    editado_em = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.numero_controle:
            with transaction.atomic():  
                ultimo = Notificacao.objects.select_for_update().order_by('-numero_controle').first()
                self.numero_controle = (ultimo.numero_controle + 1) if ultimo else 1

        super().save(*args, **kwargs)
        self.crr.atualizar_status_not_gerada()  # Atualiza o status no Crr após salvar

    def __str__(self):
        return f"Notificação {self.numero_controle} - {self.crr}"



class Arrendatario(models.Model):
    arrendatario = models.CharField(max_length=25, blank=True, null=False)
    endereco_arrendatario = models.CharField(max_length=25, blank=True, null=False)
    numero_arrendatario = models.CharField(max_length=6, blank=True, null=False)
    complemento_arrendatario = models.CharField(max_length=10, blank=True, null=False)
    bairro_arrendatario = models.CharField(max_length=25, blank=True, null=False)
    cidade_arrendatario = models.CharField(max_length=25, blank=True, null=False)
    uf_arrendatario= models.CharField(max_length=6,choices=ESTADO_CHOICES, blank=True, null=False)
    cep_arrendatario = models.CharField(max_length=9,verbose_name='CEP')
    cidade_arrendatario = models.CharField(max_length=25, blank=True, null=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    editado_em = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.arrendatario

