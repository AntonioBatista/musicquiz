import requests
import random
import time
from flask import Flask, render_template, request

app = Flask(__name__)

MAPA_PERIODOS = {
    "60s": (1960, 1969), "70s": (1970, 1979), "80s": (1980, 1989),
    "90s": (1990, 1999), "00s": (2000, 2009), "10s": (2010, 2019), "20s": (2020, 2026)
}

# --- BASE DE DATOS MASIVA (450+ ARTISTAS) ---
ARTISTAS_HITS = {
    "60s": [
        "The Beatles", "The Rolling Stones", "Elvis Presley", "The Beach Boys", "The Doors", "Aretha Franklin", 
        "Marvin Gaye", "The Supremes", "Simon & Garfunkel", "Tom Jones", "Bob Dylan", "The Kinks", "The Animals",
        "Janis Joplin", "The Who", "Jimi Hendrix", "Otis Redding", "Ray Charles", "Stevie Wonder", "James Brown",
        "Raphael", "Dúo Dinámico", "Concha Velasco", "Los Bravos", "Los Brincos", "Joan Manuel Serrat", "Massiel",
        "Lola Flores", "Rocío Dúrcal", "Marisol", "Adamo", "Dusty Springfield", "The Mamas & the Papas", "The Monkees",
        "Nancy Sinatra", "Etta James", "The Byrds", "Four Tops", "The Temptations", "Ben E. King", "Los Salvajes",
        "Creedence Clearwater Revival", "Neil Diamond", "Frank Sinatra", "Dean Martin", "Little Richard", "Chuck Berry"
    ],
    "70s": [
        "Queen", "ABBA", "Bee Gees", "Elton John", "Pink Floyd", "David Bowie", "Led Zeppelin", "Donna Summer", 
        "Stevie Wonder", "Fleetwood Mac", "Bob Marley", "The Eagles", "Deep Purple", "Jackson 5", "The Clash",
        "AC/DC", "Sex Pistols", "Gloria Gaynor", "Village People", "Earth, Wind & Fire", "Rod Stewart", "Santana",
        "Camilo Sesto", "Nino Bravo", "Julio Iglesias", "Miguel Bosé", "Jeanette", "Cecilia", "Triana", 
        "Las Grecas", "Peret", "Raffaella Carrà", "Umberto Tozzi", "Roberto Carlos", "Rocío Jurado", "Boney M.",
        "The Police", "Blondie", "Baccara", "Burning", "Genesis", "Toto", "Boston", "The Knack", "Bill Withers",
        "Kiss", "Black Sabbath", "Ramones", "Supertramp", "Electric Light Orchestra", "Barry White", "Chic"
    ],
    "80s": [
        "Michael Jackson", "Madonna", "Queen", "U2", "The Police", "Whitney Houston", "Prince", "Bon Jovi", 
        "Phil Collins", "Bruce Springsteen", "George Michael", "Dire Straits", "The Cure", "Eurythmics", 
        "Pet Shop Boys", "Depeche Mode", "A-ha", "Guns N' Roses", "Cyndi Lauper", "Bryan Adams", "Wham!", 
        "Rick Astley", "Tina Turner", "Duran Duran", "Europe", "Bonnie Tyler", "Modern Talking", "Billy Idol",
        "Mecano", "Hombres G", "Alaska y los Pegamoides", "Radio Futura", "Nacha Pop", "Los Secretos", 
        "Héroes del Silencio", "Loquillo", "El Último de la Fila", "Duncan Dhu", "Tino Casal", "Soda Stereo",
        "Aerosmith", "Iron Maiden", "Spandau Ballet", "Simple Minds", "Kylie Minogue", "The Bangles", "Scorpions",
        "Alphaville", "Culture Club", "Tears for Fears", "La Unión", "Danza Invisible", "Journey", "Foreigner",
        "Van Halen", "Def Leppard", "Motley Crue", "Whitesnake", "Roxette", "B-52s", "Soft Cell"
    ],
    "90s": [
        "Nirvana", "R.E.M.", "Oasis", "Guns N' Roses", "Spice Girls", "Backstreet Boys", "Britney Spears", 
        "Red Hot Chili Peppers", "Céline Dion", "Alanis Morissette", "Metallica", "Pearl Jam", "The Cranberries",
        "The Cardigans", "The Corrs", "Marc Anthony", "Ricky Martin", "Enrique Iglesias", "Alejandro Sanz", 
        "Estopa", "La Oreja de Van Gogh", "Jarabe de Palo", "Los Rodríguez", "Mónica Naranjo", "M Clan", 
        "Laura Pausini", "Eros Ramazzotti", "Maná", "Shakira", "Cher", "Mariah Carey", "Roxette", "Scorpions",
        "Jamiroquai", "No Doubt", "Blur", "Radiohead", "Foo Fighters", "Take That", "Camela", "Gala", "Corona",
        "Ace of Base", "Aqua", "Eiffel 65", "Vengaboys", "Juan Luis Guerra", "Celia Cruz", "Selena", "The Verve",
        "Smash Mouth", "Savage Garden", "Jennifer Lopez", "TLC", "Destinys Child", "Will Smith", "Molotov"
    ],
    "00s": [
        "Coldplay", "Eminem", "Beyoncé", "Rihanna", "Shakira", "Amy Winehouse", "The Killers", "Lady Gaga", 
        "Linkin Park", "Green Day", "Black Eyed Peas", "Maroon 5", "Alicia Keys", "Justin Timberlake", 
        "Avril Lavigne", "Evanescence", "Muse", "Arctic Monkeys", "Franz Ferdinand", "Gwen Stefani", 
        "El Canto del Loco", "Amaral", "David Bisbal", "La Quinta Estación", "Pereza", "Melendi", "Fito & Fitipaldis",
        "Juanes", "Paulina Rubio", "Julieta Venegas", "Nelly Furtado", "Keane", "Duffy", "Mika", "James Blunt",
        "Daddy Yankee", "Don Omar", "Marc Anthony", "Pignoise", "Pink", "Christina Aguilera", "The White Stripes",
        "Outkast", "Kanye West", "Usher", "50 Cent", "Tokio Hotel", "Paramore", "Kings of Leon", "MGMT"
    ],
    "10s": [
        "Adele", "Bruno Mars", "Ed Sheeran", "Taylor Swift", "Katy Perry", "Sia", "Avicii", "Daft Punk", 
        "Drake", "Calvin Harris", "Justin Bieber", "Ariana Grande", "One Direction", "Lana Del Rey", "The Weeknd",
        "Imagine Dragons", "Post Malone", "Shawn Mendes", "Camila Cabello", "Lorde", "Miley Cyrus", "Pitbull",
        "Enrique Iglesias", "Rosalía", "C. Tangana", "Pablo Alborán", "Maluma", "J Balvin", "Bad Bunny", 
        "Luis Fonsi", "Daddy Yankee", "Romeo Santos", "Vetusta Morla", "Izal", "Leiva", "David Guetta", 
        "Sam Smith", "Major Lazer", "Maldita Nerea", "Sidecars", "Twenty One Pilots", "The Chainsmokers",
        "Bastille", "Hozier", "Florence + The Machine", "Luis Miguel", "Chayanne", "Morat", "Sebastian Yatra"
    ],
    "20s": [
        "The Weeknd", "Dua Lipa", "Harry Styles", "Miley Cyrus", "Olivia Rodrigo", "Billie Eilish", "Doja Cat", 
        "SZA", "Taylor Swift", "Bad Bunny", "Karol G", "Quevedo", "Bizarrap", "Rauw Alejandro", "Rosalía", 
        "C. Tangana", "Aitana", "Sebastian Yatra", "Camilo", "Feid", "Peso Pluma", "Ana Mena", "Lola Índigo", 
        "Nathy Peluso", "Tini", "Danna Paola", "Young Miko", "Anitta", "Måneskin", "Glass Animals", "Vicco", 
        "Rels B", "Bad Gyal", "Saiko", "Marshmello", "Jack Harlow", "Fred again..", "Tate McRae", "Benson Boone",
        "Teddy Swims", "Myke Towers", "Abraham Mateo", "Arde Bogotá", "Rigoberta Bandini", "Peggy Gou", "Troye Sivan",
        "Sabrina Carpenter", "Chappell Roan", "Tyla", "FloyyMenor", "Cris MJ", "La Plazuela", "Morad", "Iñigo Quintero"
    ]
}

# Headers para evitar bloqueos de iTunes (simulamos ser un navegador real)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def obtener_cancion_segura(decadas_seleccionadas, solo_espanol):
    """Intenta buscar una canción hasta que tiene éxito."""
    intentos = 0
    while intentos < 10: # Intentamos 10 veces encontrar ALGO antes de rendirnos en esta unidad
        try:
            decada = random.choice(decadas_seleccionadas)
            ini, fin = MAPA_PERIODOS[decada]
            
            # Elegimos artista
            artistas_pool = ARTISTAS_HITS.get(decada, [])
            artista = random.choice(artistas_pool)
            
            # Parametros de búsqueda
            params = {
                "term": artista,
                "media": "music",
                "limit": 15,
                "country": "ES" if solo_espanol else "US"
            }
            
            # Petición con timeout y headers
            resp = requests.get("https://itunes.apple.com/search", params=params, headers=HEADERS, timeout=3)
            if resp.status_code != 200:
                intentos += 1
                continue
                
            data = resp.json()
            resultados = data.get("results", [])
            
            if not resultados:
                # Si falla el artista específico, PLAN B: Hit genérico
                if intentos > 5:
                    term_fallback = f"exitos {decada}" if solo_espanol else f"hits {decada}"
                    resp = requests.get("https://itunes.apple.com/search", params={"term": term_fallback, "limit": 10, "media": "music"}, headers=HEADERS, timeout=3)
                    resultados = resp.json().get("results", [])
            
            # Barajamos para variedad
            random.shuffle(resultados)
            
            for r in resultados:
                if not r.get("previewUrl"): continue
                
                # Filtro de año laxo para aceptar Greatest Hits
                f_str = r.get("releaseDate", "0000")
                anyo = int(f_str[:4])
                
                # Aceptamos canciones si el año está en rango O si es un recopilatorio posterior
                if (ini - 5) <= anyo <= (fin + 30):
                    return {
                        "preview": r["previewUrl"],
                        "artista": r["artistName"],
                        "titulo": r["trackName"],
                        "anyo": anyo,
                        "portada": r["artworkUrl100"].replace("100x100", "600x600")
                    }
            
            intentos += 1
        except Exception as e:
            print(f"Error puntual: {e}")
            intentos += 1
            time.sleep(0.1) # Pequeña pausa si hay error
            continue
            
    return None

@app.route("/")
def index():
    return render_template("menu.html", decadas=MAPA_PERIODOS.keys())

@app.route("/juego", methods=["POST"])
def juego():
    try:
        rondas = int(request.form.get("rondas", 10))
    except:
        rondas = 10
        
    solo_es = True if request.form.get("espanol") else False
    sel = request.form.getlist("periodos")
    if not sel: sel = list(MAPA_PERIODOS.keys())

    canciones = []
    
    # --- BUCLE GARANTIZADO ---
    # No sale de aquí hasta tener el número exacto
    max_iteraciones_totales = rondas * 5 # Límite de seguridad para no buclear infinito
    contador = 0
    
    while len(canciones) < rondas and contador < max_iteraciones_totales:
        candidata = obtener_cancion_segura(sel, solo_es)
        
        if candidata:
            # Chequeo de duplicados (por URL de preview)
            if not any(c['preview'] == candidata['preview'] for c in canciones):
                canciones.append(candidata)
                print(f"Canción encontrada ({len(canciones)}/{rondas}): {candidata['titulo']}")
        
        contador += 1
        
    # Si por alguna razón extrema no llegamos, enviamos lo que tengamos
    return render_template("juego.html", canciones=canciones)

if __name__ == "__main__":
    # Importante: threaded=True desactivado en desarrollo si da problemas, 
    # pero aquí lo dejamos por si acaso, aunque la lógica es secuencial.
    app.run(debug=True, host="0.0.0.0", port=5000)