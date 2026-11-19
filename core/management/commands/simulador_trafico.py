import random
from django.core.management.base import BaseCommand
from core.models import EventoLog


class Command(BaseCommand):
    help = "Genera logs de tráfico HTTP simulados (normales y sospechosos)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--cantidad",
            type=int,
            default=15,
            help="Cantidad de eventos a generar (por defecto: 15)",
        )

    def handle(self, *args, **options):
        cantidad = options["cantidad"]

        ips_normales = ["192.168.1.10", "192.168.1.24", "10.0.0.15"]
        ips_sospechosas = ["45.133.1.82", "185.220.101.4", "91.240.118.172"]

        rutas_normales = ["/", "/dashboard/", "/api/status/", "/perfil/"]
        rutas_sospechosas = [
            "/.env",
            "/wp-login.php",
            "/admin/login/",
            "/api/v1/usuarios?id=1' OR '1'='1",
        ]

        creados = 0

        for _ in range(cantidad):
            es_ataque = random.random() < 0.35  # ~35% de eventos sospechosos

            if es_ataque:
                ip = random.choice(ips_sospechosas)
                metodo = random.choice(["GET", "POST"])
                endpoint = random.choice(rutas_sospechosas)
                estado = random.choice([401, 403, 404])
                detalles = "Patrón anómalo detectado en ruta o parámetro de entrada."
            else:
                ip = random.choice(ips_normales)
                metodo = random.choice(["GET", "POST"])
                endpoint = random.choice(rutas_normales)
                estado = random.choice([200, 200, 200, 201])
                detalles = "Tráfico habitual dentro de parámetros esperados."

            EventoLog.objects.create(
                ip_origin=ip,
                metodo_http=metodo,
                endpoint=endpoint,
                codigo_estado=estado,
                detalles=detalles,
                es_sospechoso=es_ataque,
            )
            creados += 1

        self.stdout.write(
            self.style.SUCCESS(f"Se generaron {creados} registros en EventoLog.")
        )