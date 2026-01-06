# Lindas Lustfyllda Bud & Åkeri – Optimeringsalgoritm

Detta projekt löser en “lastbils-knapsack” för Lindas Lustfyllda Bud & Åkeri med hjälp av en genetisk algoritm. Programmet väljer automatiskt vilka paket som ska lastas på 10 budbilar så att vinsten maximeras och straffavgifter minimeras.

## Funktioner

- Läser daglig lagerfil (`CSV`) med vikt, volym, vinstkategori och deadlines.
- Optimerar lastning via genetisk algoritm:
  - Permutationsrepresentation av paketlistan.
  - Tournament Selection + elitism.
  - Partially Matched Crossover (PMX-liknande).
  - Mutation med små swappar (~1 % av listan).
- Dynamisk “triage”-fitness:
  - Riktig vinst per paket (`profit − penalty` om sent).
  - Extra bonus motsvarande straffkostnaden som undviks genom att lasta paketet idag.
  - Straff för sena paket som lämnas kvar i lagret.
- Resultatrapport:
  - Vinster och fyllnadsgrad per lastbil.
  - Histogram + statistik (medel, varians, standardavvikelse) för levererade respektive kvarvarande paket.
  - Total straffavgift och missad vinst i lagret.
- Exporter:
  - `Data/Lastningsplan.csv` (vilket paket hamnar i vilken bil).
  - `Data/Statistics.csv` (fitnessförbättringar över generationerna).
  - Graf över bästa fitness per generation.

## Krav

- Python 3.11+
- Beroenden: `numpy`, `matplotlib` m.fl. (se `requirements.txt`)

Installera:

```bash
python -m venv venv
venv\Scripts\activate        # PowerShell/cmd på Windows
pip install -r requirements.txt
```

## Körning

1. Placera dagens lagerfil i `data/` (exempel: `TestData1.csv`).
2. Kör huvudprogrammet:

```bash
python main.py
```

3. Programmet skriver ut:
   - Bästa fitness, vinst per bil och slutresultat för dagen.
   - Analys av levererade paket och de som blev kvar.
4. Se genererade filer i `Data/`.

## Struktur

| Fil                | Innehåll                                                                           |
|--------------------|-------------------------------------------------------------------------------------|
| `main.py`          | Kopplar ihop allt: laddar data, kör GA, skriver rapport, sparar filer.             |
| `ga.py`            | GA-komponenter (fitness, population, selektion, crossover, mutation, loop).        |
| `models.py`        | `Package` och `Truck` med kapacitetslogik.                                         |
| `analysis.py`      | Statistik, histogram, slutrapport, CSV-export.                                    |
| `requirements.txt` | Python-beroenden.                                                                  |

## Motivering av GA-val

- **Elitism:** Garanti att bästa lösningen överlever varje generation – vi tappar aldrig en “bra lastplan”.
- **Tournament Selection:** Ger balanserat selektionstryck: bra individer vinner oftare men även svagare får chansen, vilket ger variation.
- **Mutation via små swappar:** Förhindrar att populationen stagnerar men förstör inte bra lösningar helt (viktigt när listorna är stora).
- **Triage-bonus:** Bonusen motsvarar exakt den straffavgift som skulle tillkomma imorgon, vilket gör att algoritmen prioriterar paket med potentiellt explosiv kostnad utan hårdkodade poäng.

## Begränsningar / Vidare arbete

- Input-filen kan vara mycket större än vad 10 bilar klarar på en dag, vilket innebär att totalresultatet ofta blir negativt p.g.a. lagrets straffavgifter. Detta speglar affärsregeln snarare än en algoritm-bugg och kan beskrivas i rapporten.
- För fler-dagssimuleringar behöver `deadline` och lagrets innehåll uppdateras mellan körningarna.
- Möjliga förbättringar: filtrera fram “dagens planeringspool” (t.ex. topp 2 000 paket), testa annan crossover eller adaptiv mutation.

## Licens / Författare

- Kurs: Applicerad AI
- Student: Andreas Hagen
- Programmet utvecklat som inlämningsuppgift vid Teknikhögskolan.
