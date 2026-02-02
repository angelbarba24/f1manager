from django.core.management.base import BaseCommand
from core.models import Escuderia, Piloto, Circuito
from datetime import date

class Command(BaseCommand):
    help = "Carga datos oficiales de la temporada F1 2026"

    def handle(self, *args, **kwargs):
        self.stdout.write("Cargando datos oficiales de la temporada 2026...")

        # ============================
        #    ESCUDERÍAS (11 Equipos)
        # ============================
        escuderias_data = [
            ("Mercedes-AMG Petronas F1 Team", "Alemania"),
            ("Oracle Red Bull Racing", "Austria"),
            ("Scuderia Ferrari HP", "Italia"),
            ("McLaren Formula 1 Team", "Reino Unido"),
            ("Aston Martin Aramco F1 Team", "Reino Unido"),
            ("BWT Alpine F1 Team", "Francia"),
            ("Williams Racing", "Reino Unido"),
            ("Audi F1 Team", "Alemania"),
            ("Haas F1 Team", "EE.UU."),
            ("Visa Cash App RB", "Italia"),
            ("Cadillac Formula 1 Team", "EE.UU."),
        ]

        esc_objs = {}
        for nombre, pais in escuderias_data:
            # Usamos update_or_create para evitar duplicados y actualizar nombres
            obj, _ = Escuderia.objects.update_or_create(
                nombre=nombre, 
                defaults={'pais': pais}
            )
            esc_objs[nombre] = obj

        # ============================
        #    PILOTOS (Parrilla Oficial 2026)
        # ============================
        pilotos_data = [
            # MERCEDES
            ("George Russell", 63, "Mercedes-AMG Petronas F1 Team", "Reino Unido"),
            ("Andrea Kimi Antonelli", 12, "Mercedes-AMG Petronas F1 Team", "Italia"),

            # RED BULL
            ("Max Verstappen", 1, "Oracle Red Bull Racing", "Países Bajos"),
            ("Isack Hadjar", 6, "Oracle Red Bull Racing", "Francia"),

            # FERRARI
            ("Charles Leclerc", 16, "Scuderia Ferrari HP", "Mónaco"),
            ("Lewis Hamilton", 44, "Scuderia Ferrari HP", "Reino Unido"),

            # MCLAREN
            ("Lando Norris", 4, "McLaren Formula 1 Team", "Reino Unido"),
            ("Oscar Piastri", 81, "McLaren Formula 1 Team", "Australia"),

            # ASTON MARTIN
            ("Fernando Alonso", 14, "Aston Martin Aramco F1 Team", "España"),
            ("Lance Stroll", 18, "Aston Martin Aramco F1 Team", "Canadá"),

            # ALPINE
            ("Pierre Gasly", 10, "BWT Alpine F1 Team", "Francia"),
            ("Franco Colapinto", 43, "BWT Alpine F1 Team", "Argentina"),

            # WILLIAMS
            ("Alex Albon", 23, "Williams Racing", "Tailandia"),
            ("Carlos Sainz", 55, "Williams Racing", "España"),

            # AUDI
            ("Nico Hülkenberg", 27, "Audi F1 Team", "Alemania"),
            ("Gabriel Bortoleto", 5, "Audi F1 Team", "Brasil"),

            # HAAS
            ("Esteban Ocon", 31, "Haas F1 Team", "Francia"),
            ("Oliver Bearman", 87, "Haas F1 Team", "Reino Unido"),

            # RB
            ("Liam Lawson", 30, "Visa Cash App RB", "Nueva Zelanda"),
            ("Arvid Lindblad", 41, "Visa Cash App RB", "Reino Unido"),

            # CADILLAC
            ("Sergio Pérez", 11, "Cadillac Formula 1 Team", "México"),
            ("Valtteri Bottas", 77, "Cadillac Formula 1 Team", "Finlandia"),
        ]

        for nombre, numero, esc_nombre, pais in pilotos_data:
            Piloto.objects.update_or_create(
                nombre=nombre,
                defaults={
                    'numero': numero,
                    'escuderia': esc_objs[esc_nombre],
                    'pais': pais
                }
            )

        # ============================
        #    CIRCUITOS (Calendario 2026)
        # ============================
        # 24 Carreras.
        
        circuitos_data = [
            ("Albert Park", "Australia", 5.278, 58, date(2026, 3, 8)),
            ("Shanghai", "China", 5.451, 56, date(2026, 3, 15)),
            ("Suzuka", "Japón", 5.807, 53, date(2026, 3, 29)),
            ("Sakhir", "Bahréin", 5.412, 57, date(2026, 4, 12)),
            ("Jeddah Corniche", "Arabia Saudí", 6.174, 50, date(2026, 4, 19)),
            ("Miami", "Estados Unidos", 5.412, 57, date(2026, 5, 3)),
            ("Gilles Villeneuve", "Canadá", 4.361, 70, date(2026, 5, 24)),
            ("Montecarlo", "Mónaco", 3.337, 78, date(2026, 6, 7)),
            ("Barcelona-Catalunya", "España", 4.657, 66, date(2026, 6, 14)),
            ("Red Bull Ring", "Austria", 4.318, 71, date(2026, 6, 28)),
            ("Silverstone", "Reino Unido", 5.891, 52, date(2026, 7, 5)),
            ("Spa-Francorchamps", "Bélgica", 7.004, 44, date(2026, 7, 19)),
            ("Hungaroring", "Hungría", 4.381, 70, date(2026, 7, 26)),
            ("Zandvoort", "Países Bajos", 4.259, 72, date(2026, 8, 23)),
            ("Monza", "Italia", 5.793, 53, date(2026, 9, 6)),
            ("Circuito IFEMA Madrid", "España", 5.474, 55, date(2026, 9, 13)),
            ("Bakú", "Azerbaiyán", 6.003, 51, date(2026, 9, 26)),
            ("Marina Bay", "Singapur", 4.940, 61, date(2026, 10, 11)),
            ("Austin", "Estados Unidos", 5.513, 56, date(2026, 10, 25)),
            ("Hermanos Rodríguez", "México", 4.304, 71, date(2026, 11, 1)),
            ("Interlagos", "Brasil", 4.309, 71, date(2026, 11, 8)),
            ("Las Vegas", "Estados Unidos", 6.201, 50, date(2026, 11, 21)),
            ("Lusail", "Qatar", 5.419, 57, date(2026, 11, 29)),
            ("Yas Marina", "Abu Dhabi", 5.281, 58, date(2026, 12, 6)),
        ]

        for nombre, pais, longitud, vueltas, fecha in circuitos_data:
            Circuito.objects.update_or_create(
                nombre=nombre,
                defaults={
                    'pais': pais,
                    'longitud_km': longitud,
                    'vueltas': vueltas,
                    'fecha': fecha
                }
            )

        self.stdout.write(self.style.SUCCESS("Datos reales de la temporada 2026 cargados."))