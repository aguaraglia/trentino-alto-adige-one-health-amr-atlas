# Trentino-Alto Adige One Health AMR Atlas

Edizione regionale `taa_amr_atlas`, pubblicata da Codex Vitae ETS sulla stessa
base delle edizioni Liguria e Piemonte.

## Stato

La regione ha due province autonome, Bolzano/Bozen e Trento. La letteratura è
sbilanciata: 20 dei 23 studi inclusi riguardano l'Alto Adige, quasi tutti dal
Laboratorio aziendale di microbiologia di Bolzano; il Trentino ha 3 studi.
La mappa mostra i contorni di entrambe le province.

Letteratura scientifica del 20 novembre 2026: 23 studi con collegamento
territoriale esplicito, in sei layer (AMR umana, veterinaria, alimentare,
ambientale, fauna selvatica, contorno regionale). Il layer umano ha 4 elementi
e 19 studi. Il veterinario ha 1 elemento (Trento), l'alimentare 1 (Bolzano),
l'ambientale 2 (Bolzano e Trento). Il layer della fauna selvatica è vuoto e il
contorno regionale non raccoglie studi: l'area senza segnaposto è nessuna
evidenza pubblicata, non resistenza zero. Ogni popup cita lo studio e il DOI
(o il record PubMed se il DOI non è assegnato) e ricorda che il segnaposto è
il luogo dello studio, non una prevalenza.

Fonti istituzionali pubbliche: AR-ISS 2024 per provincia (CC BY 4.0; copertura
100% a Bolzano e 85,6% a Trento) e AIFA Open Data 2024, antibatterici J01 per
provincia (CC BY 4.0). Il rapporto ASUIT 2025 sul consumo territoriale di
antibatterici è una scheda senza mappa (CC BY 4.0), con attribuzione
obbligatoria: «Fonte: sito dell'Azienda sanitaria universitaria integrata del
Trentino - Provincia autonoma di Trento». Confini ISTAT 2026 (282 comuni,
2 province autonome, regione 04), letti in UTF-8. Una struttura nominata
© OpenStreetMap contributors, ODbL. Le fonti escluse sono in
`metadata/EXCLUDED_SOURCES.md`.

Il conteggio in homepage e in pubblicazioni legge
`public/data/literature-catalog.json` (23).

## Pagine

Sorgente su `main`. Il sito statico è pubblicato dal branch `gh-pages`
(GitHub Pages, cartella `/`). Nessun file `CNAME`. Analitica: GoatCounter
`https://atlanteamr.goatcounter.com/count`, come le edizioni Liguria e Piemonte.

## Build locale

```bash
python3 -m http.server 8000
```

Aprire `http://localhost:8000/`.

Per rigenerare i dati pubblici servono gli input in `raw/` e, per i confini,
l'archivio ISTAT indicato in `metadata/SNAPSHOTS.tsv`:

```bash
pip install -r requirements-geodata.txt
python3 scripts/build_istat_geography.py --source-root <Limiti01012026_g> --output-root public/geography
python3 scripts/build_literature_catalog.py
python3 scripts/build_study_evidence_layers.py
```

## Directory

- `public/`: dati e asset approvati per il sito;
- `metadata/`: fonti, snapshot, ambito pubblico e fonti escluse;
- `raw/`: curatela, esummary e risposte Nominatim;
- `scripts/`: ricostruzione del catalogo e dei layer;
- `private/`: nessun dato riservato in questa edizione.
