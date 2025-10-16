import requests
import urllib.parse
import json
import sys

class SistemaGeolocalizacionBiblioteca:
    def __init__(self):
        self.api_key = "10bc194f-054c-4e74-bf15-bc7490aa6765"  # Configurar con API key real
        self.base_url = "https://graphhopper.com/api/1/route"
        self.biblioteca_nacional = {
            'nombre': "Biblioteca Nacional de Chile",
            'direccion': "Av. Libertador Bernardo O'Higgins 651, Santiago, Chile",
            'lat': -33.442500,
            'lng': -70.644200
        }
    
    def mostrar_banner(self):
        """Muestra el banner oficial del sistema"""
        print("\n" + "="*70)
        print("🏛️  SISTEMA DE GEOLOCALIZACIÓN - BIBLIOTECA NACIONAL DE CHILE")
        print("="*70)
        print("📍 Dirección: Av. Libertador Bernardo O'Higgins 651, Santiago")
        print("🔧 Desarrollado por: API Ltda.")
        print("="*70)
    
    def obtener_coordenadas_desde_direccion(self, direccion):
        """
        Convierte una dirección en coordenadas usando Graphhopper Geocoding
        """
        url = "https://graphhopper.com/api/1/geocode"
        params = {
            'q': direccion + ", Chile",  # Aseguramos que busque en Chile
            'key': self.api_key,
            'limit': 1,
            'locale': 'es',
            'country': 'cl'  # Especificamos Chile
        }
        
        try:
            respuesta = requests.get(url, params=params, timeout=10)
            respuesta.raise_for_status()
            datos = respuesta.json()
            
            if datos['hits']:
                lat = datos['hits'][0]['point']['lat']
                lng = datos['hits'][0]['point']['lng']
                nombre_lugar = datos['hits'][0].get('name', 'Ubicación no especificada')
                return lat, lng, nombre_lugar
            else:
                return None, None, None
                
        except requests.exceptions.RequestException as error:
            print(f"❌ Error de conexión: {error}")
            return None, None, None
    
    def calcular_ruta_optimizada(self, origen_lat, origen_lng, medio_transporte="car"):
        """
        Calcula la ruta optimizada desde el origen hasta la Biblioteca Nacional de Chile
        """
        parametros = {
            'point': [f"{origen_lat},{origen_lng}", f"{self.biblioteca_nacional['lat']},{self.biblioteca_nacional['lng']}"],
            'vehicle': medio_transporte,
            'key': self.api_key,
            'instructions': True,
            'locale': 'es',
            'calc_points': True,
            'elevation': False
        }
        
        try:
            respuesta = requests.get(self.base_url, params=parametros, timeout=15)
            respuesta.raise_for_status()
            return respuesta.json()
        except requests.exceptions.RequestException as error:
            print(f"❌ Error al calcular la ruta: {error}")
            return None
    
    def formatear_distancia(self, metros):
        """
        Convierte metros a kilómetros con 2 decimales
        """
        if metros >= 1000:
            return f"{metros / 1000:.2f} km"
        else:
            return f"{metros:.2f} m"
    
    def formatear_tiempo(self, milisegundos):
        """
        Convierte milisegundos a formato legible
        """
        segundos = milisegundos / 1000
        if segundos >= 3600:
            horas = int(segundos // 3600)
            minutos = int((segundos % 3600) // 60)
            return f"{horas}h {minutos:02d}min"
        else:
            minutos = int(segundos // 60)
            return f"{minutos} min"
    
    def mostrar_instrucciones_navegacion(self, instrucciones):
        """
        Muestra las instrucciones de navegación paso a paso en español
        """
        print("\n" + "🧭 INSTRUCCIONES DETALLADAS DEL RECORRIDO")
        print("="*60)
        
        for numero, instruccion in enumerate(instrucciones, 1):
            distancia = self.formatear_distancia(instruccion.get('distance', 0))
            texto_instruccion = instruccion.get('text', 'Continuar recto')
            
            print(f"\nPaso {numero}:")
            print(f"  📍 {texto_instruccion}")
            print(f"  📏 Avanzar: {distancia}")
    
    def mostrar_resumen_ruta(self, datos_ruta, origen_nombre, medio_transporte):
        """
        Muestra un resumen completo de la ruta calculada
        """
        if not datos_ruta or 'paths' not in datos_ruta or not datos_ruta['paths']:
            print("❌ No se pudo calcular la ruta. Verifique las direcciones.")
            return False
        
        ruta = datos_ruta['paths'][0]
        
        print("\n" + "="*60)
        print("📊 RESUMEN DE LA RUTA CALCULADA")
        print("="*60)
        
        distancia_total = ruta.get('distance', 0)
        tiempo_total = ruta.get('time', 0)
        
        print(f"📍 Desde: {origen_nombre}")
        print(f"🏛️  Hasta: {self.biblioteca_nacional['nombre']}")
        print(f"🚗 Medio de transporte: {self.obtener_nombre_medio_transporte(medio_transporte)}")
        print(f"📏 Distancia total: {self.formatear_distancia(distancia_total)}")
        print(f"⏱️  Tiempo estimado: {self.formatear_tiempo(tiempo_total)}")
        print(f"🎯 Dirección destino: {self.biblioteca_nacional['direccion']}")
        
        # Mostrar información adicional relevante para Chile
        if distancia_total > 50000:  # Más de 50 km
            print("\n💡 Recomendación: Considere transporte público o automóvil")
        elif distancia_total < 2000:  # Menos de 2 km
            print("\n💡 Recomendación: Ideal para caminar o andar en bicicleta")
        
        return True
    
    def obtener_nombre_medio_transporte(self, codigo):
        """Convierte el código del medio de transporte a nombre legible"""
        transportes = {
            'car': '🚗 Automóvil',
            'bike': '🚴 Bicicleta',
            'foot': '🚶 Caminando'
        }
        return transportes.get(codigo, '🚗 Automóvil')
    
    def seleccionar_medio_transporte(self):
        """
        Permite al usuario seleccionar el medio de transporte
        """
        print("\n🚦 SELECCIONE SU MEDIO DE TRANSPORTE:")
        print("1 - 🚗 Automóvil (recomendado para distancias largas)")
        print("2 - 🚴 Bicicleta (ideal para distancias medias en Santiago)")
        print("3 - 🚶 Caminando (perfecto para distancias cortas)")
        print("4 - 🚇 Transporte público (próximamente)")
        
        while True:
            opcion = input("\nIngrese el número de su opción (1-3): ").strip()
            
            if opcion == '1':
                return 'car'
            elif opcion == '2':
                return 'bike'
            elif opcion == '3':
                return 'foot'
            elif opcion == '4':
                print("⚠️  Función en desarrollo - Por ahora seleccione otra opción")
                continue
            elif opcion.lower() in ['s', 'salir']:
                return 'salir'
            else:
                print("❌ Opción no válida. Por favor, ingrese 1, 2 o 3.")
    
    def mostrar_ubicaciones_comunes(self):
        """
        Muestra ubicaciones comunes en Santiago para facilitar la prueba
        """
        print("\n📍 UBICACIONES COMUNES EN SANTIAGO PARA PROBAR:")
        print("   - Plaza de Armas, Santiago")
        print("   - Estación Central, Santiago")
        print("   - Providencia, Santiago")
        print("   - Las Condes, Santiago")
        print("   - Universidad de Chile, Santiago")
        print("   - Parque O'Higgins, Santiago")
    
    def ejecutar_sistema(self):
        """
        Función principal que ejecuta el sistema de geolocalización
        """
        self.mostrar_banner()
        
        while True:
            print("\n--- NUEVA CONSULTA DE RUTA ---")
            print("💡 Tip: Escriba 'salir' o 's' en cualquier momento para terminar")
            
            # Mostrar ubicaciones comunes para facilitar pruebas
            self.mostrar_ubicaciones_comunes()
            
            # Solicitar ubicación de origen
            origen_input = input("\n📍 ¿Desde dónde viene? (dirección, comuna o punto de referencia): ").strip()
            
            if origen_input.lower() in ['salir', 's']:
                self.cerrar_sistema()
                break
            
            # Seleccionar medio de transporte
            medio_transporte = self.seleccionar_medio_transporte()
            if medio_transporte == 'salir':
                self.cerrar_sistema()
                break
            
            print("\n🔄 Calculando la mejor ruta...")
            
            # Obtener coordenadas del origen
            origen_lat, origen_lng, origen_nombre = self.obtener_coordenadas_desde_direccion(origen_input)
            
            if origen_lat is None:
                print("❌ No se pudo encontrar la ubicación ingresada.")
                print("💡 Por favor, verifique la dirección e intente nuevamente.")
                print("💡 Ejemplo: 'Providencia, Santiago' o 'Plaza de Armas'")
                continue
            
            print(f"✅ Ubicación encontrada: {origen_nombre}")
            
            # Calcular ruta optimizada
            datos_ruta = self.calcular_ruta_optimizada(origen_lat, origen_lng, medio_transporte)
            
            # Mostrar resultados
            if self.mostrar_resumen_ruta(datos_ruta, origen_nombre, medio_transporte):
                # Mostrar instrucciones detalladas si están disponibles
                if datos_ruta and 'paths' in datos_ruta and datos_ruta['paths']:
                    instrucciones = datos_ruta['paths'][0].get('instructions', [])
                    if instrucciones:
                        self.mostrar_instrucciones_navegacion(instrucciones)
                    else:
                        print("\n⚠️  No hay instrucciones detalladas disponibles para esta ruta.")
            
            # Preguntar si desea otra consulta
            if not self.preguntar_otra_consulta():
                break
    
    def preguntar_otra_consulta(self):
        """Pregunta al usuario si desea realizar otra consulta"""
        while True:
            respuesta = input("\n¿Desea calcular otra ruta? (s/n): ").strip().lower()
            
            if respuesta in ['s', 'si', 'sí', 'yes']:
                return True
            elif respuesta in ['n', 'no', 'salir']:
                self.cerrar_sistema()
                return False
            else:
                print("❌ Por favor, responda 's' para sí o 'n' para no.")
    
    def cerrar_sistema(self):
        """Mensaje de despedida del sistema"""
        print("\n" + "="*70)
        print("¡Gracias por usar el Sistema de Geolocalización!")
        print("Esperamos verlo pronto en la Biblioteca Nacional de Chile")
        print("📚 ¡Que tenga un excelente día!")
        print("="*70)

def main():
    """
    Función principal de ejecución del programa
    """
    # Verificar configuración de API key
    sistema = SistemaGeolocalizacionBiblioteca()
    
    if sistema.api_key == "TU_API_KEY_GRAPHHOPPER_AQUI":
        print("❌ CONFIGURACIÓN REQUERIDA")
        print("="*50)
        print("Para usar el sistema, debe configurar su API key de Graphhopper:")
        print("1. Obtenga una API key gratuita en: https://www.graphhopper.com/dev/")
        print("2. Reemplace 'TU_API_KEY_GRAPHHOPPER_AQUI' en el código")
        print("3. Guarde los cambios y ejecute nuevamente")
        print("\n💡 API key actual: NO CONFIGURADA")
        sys.exit(1)
    
    try:
        sistema.ejecutar_sistema()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario.")
        sistema.cerrar_sistema()
    except Exception as error:
        print(f"\n❌ Error inesperado: {error}")
        print("Por favor, contacte al equipo de soporte de API Ltda.")

if __name__ == "__main__":
    main()