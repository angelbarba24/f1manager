from django.core.management.base import BaseCommand
from core.models import Escuderia, Piloto, Circuito
from datetime import date

class Command(BaseCommand):
    help = "Carga datos oficiales de la temporada F1 2026 con Colores y Banderas"

    def handle(self, *args, **kwargs):
        self.stdout.write("Cargando datos extendidos de la temporada 2026...")

        # ============================
        #    ESCUDERÍAS
        # ============================
        # Formato: (Nombre, País, Color HEX)
        escuderias_data = [
            ("Mercedes-AMG Petronas F1 Team", "Alemania", "#00A19C"),
            ("Oracle Red Bull Racing", "Austria", "#061D41"),
            ("Scuderia Ferrari HP", "Italia", "#E80020"),
            ("McLaren Formula 1 Team", "Reino Unido", "#FF8000"),
            ("Aston Martin Aramco F1 Team", "Reino Unido", "#00594F"),
            ("BWT Alpine F1 Team", "Francia", "#FD4BC7"),
            ("Williams Racing", "Reino Unido", "#00A0DE"),
            ("Audi F1 Team", "Alemania", "#C0C0C0"),
            ("Haas F1 Team", "EE.UU.", "#B6BABD"),
            ("Visa Cash App RB", "Italia", "#1634BD"),
            ("Cadillac Formula 1 Team", "EE.UU.", "#D4AF37"),
        ]

        esc_objs = {}
        for nombre, pais, color in escuderias_data:
            # Usamos update_or_create para guardar el color también
            obj, _ = Escuderia.objects.update_or_create(
                nombre=nombre, 
                defaults={'pais': pais, 'color': color}
            )
            esc_objs[nombre] = obj

        # ============================
        #    PILOTOS
        # ============================
        # Formato: (Nombre, Numero, Equipo, País, Código ISO para bandera)
        pilotos_data = [
            # MERCEDES
            ("George Russell", 63, "Mercedes-AMG Petronas F1 Team", "Reino Unido", "gb"),
            ("Andrea Kimi Antonelli", 12, "Mercedes-AMG Petronas F1 Team", "Italia", "it"),

            # RED BULL
            ("Max Verstappen", 1, "Oracle Red Bull Racing", "Países Bajos", "nl"),
            ("Isack Hadjar", 6, "Oracle Red Bull Racing", "Francia", "fr"),

            # FERRARI
            ("Charles Leclerc", 16, "Scuderia Ferrari HP", "Mónaco", "mc"),
            ("Lewis Hamilton", 44, "Scuderia Ferrari HP", "Reino Unido", "gb"),

            # MCLAREN
            ("Lando Norris", 4, "McLaren Formula 1 Team", "Reino Unido", "gb"),
            ("Oscar Piastri", 81, "McLaren Formula 1 Team", "Australia", "au"),

            # ASTON MARTIN
            ("Fernando Alonso", 14, "Aston Martin Aramco F1 Team", "España", "es"),
            ("Lance Stroll", 18, "Aston Martin Aramco F1 Team", "Canadá", "ca"),

            # ALPINE
            ("Pierre Gasly", 10, "BWT Alpine F1 Team", "Francia", "fr"),
            ("Franco Colapinto", 43, "BWT Alpine F1 Team", "Argentina", "ar"),

            # WILLIAMS
            ("Alex Albon", 23, "Williams Racing", "Tailandia", "th"),
            ("Carlos Sainz", 55, "Williams Racing", "España", "es"),

            # AUDI
            ("Nico Hülkenberg", 27, "Audi F1 Team", "Alemania", "de"),
            ("Gabriel Bortoleto", 5, "Audi F1 Team", "Brasil", "br"),

            # HAAS
            ("Esteban Ocon", 31, "Haas F1 Team", "Francia", "fr"),
            ("Oliver Bearman", 87, "Haas F1 Team", "Reino Unido", "gb"),

            # RB
            ("Liam Lawson", 30, "Visa Cash App RB", "Nueva Zelanda", "nz"),
            ("Arvid Lindblad", 41, "Visa Cash App RB", "Reino Unido", "gb"),

            # CADILLAC
            ("Sergio Pérez", 11, "Cadillac Formula 1 Team", "México", "mx"),
            ("Valtteri Bottas", 77, "Cadillac Formula 1 Team", "Finlandia", "fi"),
        ]

        for nombre, numero, esc_nombre, pais, codigo in pilotos_data:
            Piloto.objects.update_or_create(
                nombre=nombre,
                defaults={
                    'numero': numero,
                    'escuderia': esc_objs[esc_nombre],
                    'pais': pais,
                    'codigo_pais': codigo
                }
            )

        # ============================
        #    CIRCUITOS (Con Banderas)
        # ============================
        # Formato: (Nombre, País, CODIGO, Longitud, Vueltas, Fecha)
        circuitos_data = [
            ("Albert Park", "Australia", "au", 5.278, 58, date(2026, 3, 8)),
            ("Shanghai", "China", "cn", 5.451, 56, date(2026, 3, 15)),
            ("Suzuka", "Japón", "jp", 5.807, 53, date(2026, 3, 29)),
            ("Sakhir", "Bahréin", "bh", 5.412, 57, date(2026, 4, 12)),
            ("Jeddah Corniche", "Arabia Saudí", "sa", 6.174, 50, date(2026, 4, 19)),
            ("Miami", "Estados Unidos", "us", 5.412, 57, date(2026, 5, 3)),
            ("Gilles Villeneuve", "Canadá", "ca", 4.361, 70, date(2026, 5, 24)),
            ("Montecarlo", "Mónaco", "mc", 3.337, 78, date(2026, 6, 7)),
            ("Barcelona-Catalunya", "España", "es", 4.657, 66, date(2026, 6, 14)),
            ("Red Bull Ring", "Austria", "at", 4.318, 71, date(2026, 6, 28)),
            ("Silverstone", "Reino Unido", "gb", 5.891, 52, date(2026, 7, 5)),
            ("Spa-Francorchamps", "Bélgica", "be", 7.004, 44, date(2026, 7, 19)),
            ("Hungaroring", "Hungría", "hu", 4.381, 70, date(2026, 7, 26)),
            ("Zandvoort", "Países Bajos", "nl", 4.259, 72, date(2026, 8, 23)),
            ("Monza", "Italia", "it", 5.793, 53, date(2026, 9, 6)),
            ("Circuito IFEMA Madrid", "España", "es", 5.474, 55, date(2026, 9, 13)),
            ("Bakú", "Azerbaiyán", "az", 6.003, 51, date(2026, 9, 26)),
            ("Marina Bay", "Singapur", "sg", 4.940, 61, date(2026, 10, 11)),
            ("Austin", "Estados Unidos", "us", 5.513, 56, date(2026, 10, 25)),
            ("Hermanos Rodríguez", "México", "mx", 4.304, 71, date(2026, 11, 1)),
            ("Interlagos", "Brasil", "br", 4.309, 71, date(2026, 11, 8)),
            ("Las Vegas", "Estados Unidos", "us", 6.201, 50, date(2026, 11, 21)),
            ("Lusail", "Qatar", "qa", 5.419, 57, date(2026, 11, 29)),
            ("Yas Marina", "Abu Dhabi", "ae", 5.281, 58, date(2026, 12, 6)),
        ]

        for nombre, pais, codigo, longitud, vueltas, fecha in circuitos_data:
            Circuito.objects.update_or_create(
                nombre=nombre,
                defaults={
                    'pais': pais,
                    'codigo_pais': codigo,
                    'longitud_km': longitud,
                    'vueltas': vueltas,
                    'fecha': fecha
                }
            )
            
        self.stdout.write(self.style.SUCCESS("Añadidos circuitos, pilotos y escuderias."))