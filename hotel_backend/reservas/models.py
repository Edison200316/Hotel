from django.db import models

# Modelo de Cliente
class Cliente(models.Model):
    cedula = models.CharField(max_length=10, primary_key=True, blank=False)
    nombre = models.CharField(max_length=50, blank=False)
    apellido = models.CharField(max_length=50, blank=False)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.cedula} - {self.nombre} {self.apellido}'

# Modelo de Habitacion
class Habitacion(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)
    numero = models.CharField(max_length=10)
    tipo = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Habitación {self.numero} - {self.tipo}'

# Modelo de Reserva
class Reserva(models.Model):
    cedula = models.ForeignKey(Cliente, on_delete=models.RESTRICT)
    codigo = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_ingreso = models.DateField()
    fecha_salida = models.DateField()

    def __str__(self):
        return f'Reserva de {self.cedula.nombre} {self.cedula.apellido} en habitación {self.codigo.numero}'
