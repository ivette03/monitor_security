from django.db import models
from django.contrib import admin
# Create your models here.
class EventoLog(models.Model):
    nivel=[
        ('INFO','INFORMATIVO'),
        ('WARNING','ADVERTENCIA'),
        ('LOW','BAJO'),
        ('HIGHT','ALTO'),
        ('CRITICAL','CRITICO'),
    ]
    ip_origin=models.GenericIPAddressField()
    metodo_http=models.CharField(max_length=10)
    endpoint=models.CharField(max_length=100)
    codigo_estado=models.IntegerField()
    detalles=models.TextField(blank=True, null=True)
    es_sospechoso=models.BooleanField(default=False)
    fecha_ingreso=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha_ingreso}- {self.ip_origin} - {self.metodo_http} {self.endpoint} - {self.codigo_estado} - {self.nivel}"

class Alerta(models.Model):
    evento=models.ForeignKey(EventoLog, on_delete=models.CASCADE, related_name='alertas')
    nivel_amenaza=models.CharField(max_length=10, choices=EventoLog.nivel)
    analisis=models.TextField()
    recomendacion=models.TextField()
    fecha_alerta=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alerta  {self.nivel_amenaza} - ip: {self.evento.ip_origin}"