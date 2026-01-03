

# Lindas Lustfyllda Bud & Åkeri - Optimeringsalgoritm

Detta projekt implementerar en genetisk algoritm (Genetic Algorithm) för att optimera lastningen av budbilar. Målet är att maximera vinsten genom att välja rätt paket för leverans, samtidigt som man tar hänsyn till begränsningar i vikt, volym och deadlines.

## Projektbeskrivning

Programmet läser in en lista med paket från en CSV-fil (`lagerstatus.csv` eller liknande) och använder en evolutionär algoritm för att hitta den bästa kombinationen av paket att lasta på 10 lastbilar.

### Begränsningar och Regler
*   **Antal bilar:** 10 st
*   **Maxvikt per bil:** 800 kg
*   **Maxvolym per bil:** 1000 m³ (enligt uppdaterade krav)
*   **Vinst:** Varje paket har ett vinstvärde.
*   **Straffavgift:** Paket som levereras efter deadline ger en straffavgift.

## Installation

1.  Klona detta repository.
2.  Skapa en virtuell miljö (rekommenderas):
    ```bash
    python -m venv venv
    source venv/bin/activate  # På Windows: venv\Scripts\activate
    ```
3.  Installera beroenden:
    ```bash
    pip install -r requirements.txt
    ```

## Användning

Kör huvudprogrammet med:

```bash
python main.py
```

Programmet kommer att:
1.  Läsa in data.
2.  Köra den genetiska algoritmen över ett antal generationer.
3.  Visa en graf över förbättringen av "fitness" (vinst).
4.  Skriva ut detaljerad statistik för varje lastbil.
5.  Visa statistik för levererade paket och kvarvarande paket i lager.

## Filstruktur

*   `main.py`: Huvudprogrammet som knyter ihop allt.
*   `ga.py`: Innehåller logiken för den genetiska algoritmen (population, selektion, crossover, mutation).
*   `models.py`: Datamodeller för `Package` och `Truck`.
*   `analysis.py`: Funktioner för att analysera och visualisera resultat.
*   `data/`: Mapp för indata (CSV-filer).

## Algoritm

Lösningen använder en genetisk algoritm med följande egenskaper:
*   **Representation:** En lista av paket som permuteras.
*   **Fitness-funktion:** Total vinst för alla lastade paket minus eventuella straffavgifter.
*   **Selektion:** Tournament Selection för att välja föräldrar.
*   **Elitism:** Den bästa lösningen från varje generation bevaras alltid.
*   **Crossover & Mutation:** Skapar variation för att hitta nya, bättre lösningar.

## Författare
Andreas Hagen
