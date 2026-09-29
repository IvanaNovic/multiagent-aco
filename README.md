# Multi-Agent ACO sistem

Projektni zadatak iz predmeta "Uvod u vještačku inteligenciju" - implementacija više kolonija mrava (Ant Colony Optimization) koje sarađuju ili konkurišu pri rješavanju problema trgovačkog putnika (TSP).

## Struktura projekta
- `src/ant.py` - klasa Ant (mrav): stanje jedne ture (posjećeni gradovi, dužina)
- `src/colony.py` - klasa Colony: parametri (alpha, beta, rho), feromoni, ACO logika
- `src/graph.py` - klasa Graph: učitavanje gradova i računanje distanci
- `src/simulation.py` - klasa Simulation: koordinacija više kolonija (nezavisno/saradnja/konkurencija)
- `src/visualize.py` - grafik konvergencije, statična i animirana vizualizacija feromona
- `src/analysis.py` - analiza stabilnosti kroz višestruka pokretanja
- `main.py` - glavna ulazna tačka (CLI)

## Instalacija

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Pokretanje

Osnovno pokretanje (3 kolonije, konkurentni režim, 40 iteracija):

    python3 main.py

Sa prilagođenim parametrima:

    python3 main.py --mode cooperative --iterations 60
    python3 main.py --mode independent --iterations 40 --stability-runs 10
    python3 main.py --mode competitive --iterations 40 --animate

Dostupni argumenti:
- `--cities` - putanja do fajla sa gradovima (podrazumijevano `data/cities.txt`)
- `--iterations` - broj iteracija ACO algoritma (podrazumijevano 40)
- `--mode` - `independent`, `cooperative` ili `competitive` (podrazumijevano `competitive`)
- `--stability-runs` - ako je veće od 0, pokreće analizu stabilnosti sa N ponavljanja
- `--animate` - generiše animaciju (GIF) širenja feromona kroz iteracije

## Parametri kolonija

Svaka kolonija ima nezavisne parametre (alpha - uticaj feromona, beta - uticaj
heuristike, rho - stopa isparavanja feromona), podešeni u `main.py` u listi `configs`.

## Režimi rada

- **independent** - kolonije rade potpuno nezavisno, bez interakcije
- **cooperative** - kolonije periodično razmjenjuju feromone (najbolja kolonija dijeli sa ostalima)
- **competitive** - kolonije rade nezavisno, na kraju se eksplicitno poredi pobjednik

## Rezultati

Nakon pokretanja, u `results/` se čuvaju:
- `convergence.png` - kriva konvergencije (najbolja dužina ture kroz iteracije) po koloniji
- `pheromones.png` - vizuelizacija intenziteta feromona na kraju simulacije
- `pheromone_animation.gif` - animacija širenja feromona kroz iteracije (uz `--animate`)

## Analiza stabilnosti

Sa `--stability-runs N`, cijela simulacija se pokreće N puta i za svaku koloniju se računa prosjek i standardna devijacija najbolje pronađene dužine ture, radi provjere koliko je algoritam osjetljiv na slučajnost.