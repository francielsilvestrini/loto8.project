from django.db import models


class Resultado(models.Model):
    concurso = models.IntegerField(unique=True)
    bola_01 = models.IntegerField()
    bola_02 = models.IntegerField()
    bola_03 = models.IntegerField()
    bola_04 = models.IntegerField()
    bola_05 = models.IntegerField()
    bola_06 = models.IntegerField()
    bola_07 = models.IntegerField()
    bola_08 = models.IntegerField()
    bola_09 = models.IntegerField()
    bola_10 = models.IntegerField()
    bola_11 = models.IntegerField()
    bola_12 = models.IntegerField()
    bola_13 = models.IntegerField()
    bola_14 = models.IntegerField()
    bola_15 = models.IntegerField()
    data_sorteio = models.DateField()
    arrecadacao_total = models.FloatField()
    ganhadores_15_numeros = models.IntegerField()
    ganhadores_14_numeros = models.IntegerField()
    ganhadores_13_numeros = models.IntegerField()
    ganhadores_12_numeros = models.IntegerField()
    ganhadores_11_numeros = models.IntegerField()
    valor_rateio_15_numeros = models.FloatField()
    valor_rateio_14_numeros = models.FloatField()
    valor_rateio_13_numeros = models.FloatField()
    valor_rateio_12_numeros = models.FloatField()
    valor_rateio_11_numeros = models.FloatField()

    def bolas(self):
        b = []
        b.append(self.bola_01)
        b.append(self.bola_02)
        b.append(self.bola_03)
        b.append(self.bola_04)
        b.append(self.bola_05)
        b.append(self.bola_06)
        b.append(self.bola_07)
        b.append(self.bola_08)
        b.append(self.bola_09)
        b.append(self.bola_10)
        b.append(self.bola_11)
        b.append(self.bola_12)
        b.append(self.bola_13)
        b.append(self.bola_14)
        b.append(self.bola_15)
        return b

    def __str__(self):
        return str(self.concurso) + '[%s]'.format(','.join(self.bolas()))