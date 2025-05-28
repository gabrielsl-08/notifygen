from django.db import models, transaction
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from .choices import STATUS_CHOICES,CATEGORIA_CHOICES,ESTADO_CHOICES,STATUS_CHOICES,ESPECIE_CHOICES

# ---------------- VEÍCULO ---------------- #
def upload_path(instance, filename):
    numeroCrr = instance.crr.numeroCrr if instance.crr.numeroCrr else "sem_identificacao"
    return f"notificacoes/{numeroCrr}/{filename}"




class Crr(models.Model):  
    numeroCrr = models.CharField(max_length=10, unique=True, blank=False, null=True, verbose_name='número do crr')
    localFiscalizacao = models.CharField(max_length=100, blank=False, null=False,verbose_name='Local da Fiscalização')
    municipioEstadoFiscalizacao = models.CharField(max_length=50,default='São Sebastião - SP' ,blank=True, null=True,verbose_name='Município da Fiscalização')
    dataFiscalizacao = models.DateField(blank=False, null=False,verbose_name='Data da fiscalização')
    horaFiscalizacao = models.TimeField(blank=False, null=False,verbose_name='Hora da fiscalização')
    observacao = models.CharField(max_length=300, blank=True, null=False,verbose_name='Observação')
    matriculaAgente = models.CharField(max_length=10, blank=False, null=False)
    medidaAdministrativa  = models.CharField(max_length=100, blank=True,default='Remoção do veículo ao Depósito', null=True,verbose_name='Medida Administrativa')
    localPatio =  models.CharField(max_length=100,default='RUA BOLIVIA, JARAGUA - SÃO SEBASTIÃO/SP - 11600-748', blank=True, null=False,verbose_name='Pátio')
    placaGuincho = models.CharField(max_length=7, blank=True, null=False,verbose_name='Placa do guicho')
    encarregado = models.CharField(max_length=50, blank=True, null=False,verbose_name='encarregado do guincho')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES,default='retido',help_text="Status atual do veículo (Retido/Liberado)")    
    not_gerada = models.BooleanField(default=False,verbose_name='Status da Notificação')
    edital_emitido = models.BooleanField(default=False) 
    criado_em = models.DateTimeField(auto_now_add=True)
    editado_em = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Definir os campos que devem ser convertidos para minúsculas
        lower_fields = [
             'numeroCrr','localFiscalizacao','municipioEstadoFiscalizacao','observacao',
             'medidaAdministrativa','localPatio','placaGuincho','encarregado',
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
         return self.numeroCrr 
    
    def atualizar_status_not_gerada(self):
        """Atualiza automaticamente se a notificação já foi gerada."""
        if hasattr(self, 'notificacao'):  # Verifica se já há uma Notificação vinculada
            self.not_gerada = False
        else:
            self.not_gerada = self.dataFiscalizacao <= (date.today() - timedelta(days=10))
        self.save()

    def calcular_prazo_leilao(self):
        """Retorna a data de leilão (60 dias após a remoção)."""
        if self.dataFiscalizacao:
            return self.dataFiscalizacao + timedelta(days=60)
        return None


class Veiculo(models.Model):
    crr = models.ForeignKey(Crr, on_delete=models.CASCADE, related_name='veiculo')
    placa = models.CharField( max_length=7,blank=True,null=False)
    chassi = models.CharField( max_length=20,blank=True, null=False)
    marca = models.CharField(max_length=20, blank=True, null=False)
    modelo = models.CharField(max_length=20, blank=True, null=False)
    cor = models.CharField( max_length=20,blank=True, null=False)
    especie = models.CharField(max_length=20 ,choices=ESPECIE_CHOICES, blank=True, null=False,verbose_name='espécie')
    categoria = models.CharField(max_length=20,choices=CATEGORIA_CHOICES, blank=True, null=False)
    ufVeiculo = models.CharField(max_length=6, choices=ESTADO_CHOICES, blank=True, null=False,verbose_name='UF do veículo')
    municipioVeiculo = models.CharField(max_length=30, blank=True, null=False,verbose_name='Município do veículo')

    def __str__(self):
        return self.placa or "Veículo sem placa"
    def save(self, *args, **kwargs):
        # Definir os campos que devem ser convertidos para minúsculas
        lower_fields = [ 'placa','chassi','marca', 'modelo','cor' ,
                        'especie','categoria','ufVeiculo','municipioVeiculo',
                       ]
        
        # Aplicar normalização para minúsculas
        for field in lower_fields:
            value = getattr(self, field)
            if value and isinstance(value, str):
                setattr(self, field, value.lower())
                                        
        super().save(*args, **kwargs)
    
    
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
    cnh = models.CharField(max_length=11, blank=True, null=False, verbose_name='cnh')
    cnhEstrangeira = models.CharField(max_length=11, blank=True, null=False, verbose_name='cnh estrangeira')
    ufCnh = models.CharField(max_length=6, choices=ESTADO_CHOICES, blank=True, null=False, verbose_name='UF da CNH')
    cpfCondutor = models.CharField(max_length=14, blank=True, null=False, verbose_name='CPF')
    nomeCondutor = models.CharField(max_length=50, blank=True, null=False, verbose_name='Nome do Condutor')


    def __str__(self):
        return f"{self.nomeCondutor} ({self.cpfCondutor})"



class Ait(models.Model):
    crr = models.ForeignKey(Crr,on_delete=models.CASCADE,related_name='aits')
    ait = models.CharField(max_length=11,verbose_name='Código de AIT', blank=True, null=False)   
    
    def __str__(self):
        return self.ait
    
    def save(self, *args, **kwargs): # normaliza banco de dados
        lower_fields = [
            'ait',
        ]
        
        # Aplicar normalização para minúsculas
        for field in lower_fields:
            value = getattr(self, field)
            if value and isinstance(value, str):
                setattr(self, field, value.lower())
                                 
        super().save(*args, **kwargs)


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
    enquadramento = models.ForeignKey(TabelaEnquadramento, on_delete=models.PROTECT, verbose_name="Enquadramento",null=True)

    def __str__(self):
        return f"{self.enquadramento.codigo} - {self.enquadramento.descricao_infracao[:30]}"


class ImagemCrr(models.Model):
    crr = models.ForeignKey('Crr', on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to=upload_path, blank=True, null=True, verbose_name="Imagem (upload via Admin)")
    nomeArquivo = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(max_length=1000, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Atualiza os campos com base na imagem enviada
        if self.imagem and (not self.url or not self.nomeArquivo):
            self.nomeArquivo = self.imagem.name
            self.url = self.imagem.url
            super().save(update_fields=['nomeArquivo', 'url'])

    def __str__(self):
        return self.url or f"Imagem {self.id} para {self.crr.numeroCrr}"