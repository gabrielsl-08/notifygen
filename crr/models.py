from django.db import models, transaction
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.contrib.auth.models import User

# ---------------- VEÍCULO ---------------- #
def upload_path(instance, filename):
    numero_crr = instance.crr.numero_crr if instance.crr.numero_crr else "sem_identificacao"
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

ORGAO_CHOICES = [
    ('detraf', 'DETRAF'), ('gcm', 'GCM'), ('pm', 'PM'),
]
class AgenteAutuador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='agente_autuador', blank=True, null=True)
    nome_agente = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nome do Agente')
    matricula = models.CharField(max_length=50, unique=True, blank=False, null=False)
    orgao = models.CharField(max_length=6, choices=ORGAO_CHOICES, blank=False, null=True, verbose_name='Órgão')
    assinatura_agente = models.ImageField(upload_to='signatures/', blank=True, null=True, verbose_name='Assinatura do Agente')

    def __str__(self):
        return self.matricula



class Crr(models.Model):
    numero_crr = models.CharField(max_length=10, unique=True, blank=True, null=True, verbose_name='número do crr')
    placa_chassi = models.CharField( max_length=17,blank=True, null=False,verbose_name='placa/chassi')
    marca = models.CharField(max_length=7, blank=True, null=False)
    modelo = models.CharField(max_length=7, blank=True, null=False)
    especie = models.CharField(max_length=20 ,choices=ESPECIE_CHOICES, blank=True, null=False,verbose_name='espécie')
    categoria = models.CharField(max_length=20,choices=CATEGORIA_CHOICES, blank=True, null=False)
    uf_veiculo = models.CharField(max_length=6, choices=ESTADO_CHOICES, blank=True, null=False,verbose_name='UF do veículo')
    municipio_veiculo = models.CharField(max_length=25, blank=True, null=False,verbose_name='Município do veículo')
    local_remocao = models.CharField(max_length=100, blank=False, null=False,verbose_name='Local da Remoção')
    data_remocao = models.DateField(blank=False, null=False,verbose_name='Data da remoção')
    hora_remocao = models.TimeField(blank=False, null=False,verbose_name='Hora da remoção')
    observacao = models.CharField(max_length=100, blank=True, null=False,verbose_name='Observação')
    agente_autuador = models.ForeignKey(AgenteAutuador, on_delete=models.PROTECT, related_name='crrs')
    matricula_agente  = models.CharField(max_length=10, blank=True, null=True,verbose_name='Agente autuador')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES,default='retido',help_text="Status atual do veículo (Retido/Liberado)")    
    not_gerada = models.BooleanField(default=False,verbose_name='Status da Notificação')
    edital_emitido = models.BooleanField(default=False) 

    criado_em = models.DateTimeField(auto_now_add=True)
    editado_em = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Definir os campos que devem ser convertidos para minúsculas
        lower_fields = [
            'placa_chassi','marca', 'modelo', 'municipio_veiculo', 'local_remocao',
            'observacao',
        ]
        
        # Aplicar normalização para minúsculas
        for field in lower_fields:
            value = getattr(self, field)
            if value and isinstance(value, str):
                setattr(self, field, value.lower())
                     
       
            
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "CRR"
        verbose_name_plural = "CRRs"
    def __str__(self):
         return self.numero_crr 
    
    def atualizar_status_not_gerada(self):
        """Atualiza automaticamente se a notificação já foi gerada."""
        if hasattr(self, 'notificacao'):  # Verifica se já há uma Notificação vinculada
            self.not_gerada = False
        else:
            self.not_gerada = self.data_remocao <= (date.today() - timedelta(days=10))
        self.save()

    def calcular_prazo_leilao(self):
        """Retorna a data de leilão (60 dias após a remoção)."""
        if self.data_remocao:
            return self.data_remocao + timedelta(days=60)
        return None



    
class TabelaArrendatario(models.Model):
    nome_arrendatario = models.CharField(max_length=25, unique=True,blank=True,null=False,verbose_name='Nome do arrendatário')
    cnpj_arrendatario = models.CharField(max_length=20,blank=True,null=False,verbose_name='CNPJ')
    endereco_arrendatario = models.CharField(max_length=25,blank=True,null=False,verbose_name='Endereço')
    numero_arrendatario = models.CharField(max_length=6,blank=True,null=False,verbose_name='número')
    complemento_arrendatario = models.CharField(max_length=10, blank=True,null=False,verbose_name='Complemento')
    bairro_arrendatario = models.CharField(max_length=25,blank=True,null=False,verbose_name='Bairro')
    cidade_arrendatario = models.CharField(max_length=25,blank=True,null=False,verbose_name='Cidade')
    uf_arrendatario = models.CharField(max_length=6, choices=ESTADO_CHOICES,blank=True,null=False,verbose_name='UF')
    cep_arrendatario = models.CharField(max_length=9,blank=True,null=False,verbose_name='CEP')

    def __str__(self):
        return f"{self.nome_arrendatario} - {self.cnpj_arrendatario}"

    def save(self, *args, **kwargs):
        campos_minusculos = [
            'nome_arrendatario','endereco_arrendatario','complemento_arrendatario','bairro_arrendatario','cidade_arrendatario',
        ]
        for field in campos_minusculos:
            valor = getattr(self, field)
            if valor and isinstance(valor, str):
                setattr(self, field, valor.lower())

        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Arrendatário"
        verbose_name_plural = "Arrendatários"

class Arrendatario(models.Model):
    crr = models.ForeignKey(Crr, on_delete=models.CASCADE, related_name='arrendatarios')
    arrendatario = models.ForeignKey(TabelaArrendatario, on_delete=models.PROTECT, verbose_name="Arrendatário")

    def __str__(self):
        return f"{self.arrendatario.nome_arrendatario} - {self.arrendatario.cnpj_arrendatario}"

    class Meta:
        verbose_name = "Arrendatário"
        verbose_name_plural = "Arrendatários"


class Condutor(models.Model):
    crr = models.ForeignKey(Crr, on_delete=models.CASCADE, related_name='condutores')
    habilitacao_condutor = models.CharField(max_length=11, blank=True, null=False, verbose_name='Habilitação do Condutor')
    uf_cnh = models.CharField(max_length=6, choices=ESTADO_CHOICES, blank=True, null=False, verbose_name='UF da CNH')
    cpf = models.CharField(max_length=14, blank=True, null=False, verbose_name='CPF')
    nome_condutor = models.CharField(max_length=50, blank=True, null=False, verbose_name='Nome do Condutor')
    assinatura_condutor = models.ImageField(upload_to='signatures/', blank=True, null=True, verbose_name='Assinatura do Condutor')

    def __str__(self):
        return f"{self.nome_condutor} ({self.cpf})"



class Ait(models.Model):
    crr = models.ForeignKey(Crr,on_delete=models.CASCADE,related_name='ait')
    ait = models.CharField(max_length=11,verbose_name='Código de AIT', blank=True, null=False)   
    def __str__(self):
        return self.ait
    

class TabelaEnquadramento(models.Model):
    codigo = models.CharField(max_length=6, unique=True,verbose_name='Código')
    amparo_legal = models.CharField(max_length=100)
    descricao_infracao = models.CharField(max_length=500,verbose_name='Descrição da informação')

    def __str__(self):
        return f"{self.codigo} - {self.descricao_infracao}"

    def save(self, *args, **kwargs): # normaliza banco de dados
        lower_fields = [
            'amparo_legal','descricao_infracao',
        ]
        
        # Aplicar normalização para minúsculas
        for field in lower_fields:
            value = getattr(self, field)
            if value and isinstance(value, str):
                setattr(self, field, value.lower())
                                 
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Enquadramento"
        verbose_name_plural = "Enquadramentos"

class Enquadramento(models.Model):
    crr = models.ForeignKey(Crr, on_delete=models.CASCADE, related_name='enquadramentos')
    enquadramento = models.ForeignKey(TabelaEnquadramento, on_delete=models.PROTECT, verbose_name="Enquadramento")

    def __str__(self):
        return f"{self.enquadramento.codigo} - {self.enquadramento.descricao_infracao[:30]}"


class ImagemCrr(models.Model):
    crr = models.ForeignKey('Crr', on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to=upload_path, blank=True, null=True, verbose_name="Imagem da Remoção")

    def __str__(self):
        return f"Imagem {self.id} para {self.crr.numero_crr}"