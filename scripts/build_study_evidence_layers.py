#!/usr/bin/env python3
"""Build Trentino-Alto Adige study evidence layers from the curated literature catalog.

Geometries come from the ISTAT 2026 boundaries of this edition, from a named
facility geocoded on OpenStreetMap Nominatim (1 req/s, 2026-11-20, raw
responses in raw/nominatim/). The script does not geocode farms, kennels or shelters and does not
invent a site the catalog does not name.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = "Il segnaposto indica dove è stato condotto lo studio, non una prevalenza."
SECTOR = {
    "healthcare_amr": "AMR clinica",
    "human_antimicrobial_use": "Consumo di antimicrobici",
    "antimicrobial_stewardship": "Stewardship antimicrobica",
    "veterinary_amr": "AMR veterinaria",
    "companion_animal_amr": "AMR negli animali d'affezione",
    "environmental_amr": "AMR ambientale",
    "foodborne_amr": "AMR alimentare",
    "wildlife_amr": "AMR nella fauna selvatica",
}
# Strutture nominate geocodificate su Nominatim il 2026-11-20 (raw/nominatim/results_2026-11-20.json).
POINTS = {
    "ospedale_bolzano": (11.3107067, 46.4982983, "Ospedale di Bolzano (San Maurizio)",
                         "Coordinate: OSM Nominatim, 'Ospedale Provinciale di Bolzano', Via Lorenz Böhler, 2026-11-20."),
}
ORGANISM = {
    "pubmed_20345467": "Enterobacteriaceae produttori di metallo-beta-lattamasi (VIM)",
    "pubmed_28353450": "Clostridioides difficile (ribotipo 027), sensibilità agli antibiotici",
    "pubmed_41754396": "Enterococcus faecium resistente alla vancomicina (VREfm)",
    "pubmed_42254537": "Enterococcus faecium resistente alla vancomicina in terapia intensiva neonatale",
    "pubmed_24125922": "Enterobacteriaceae produttori di carbapenemasi (VIM-1, KPC-3, OXA-48)",
    "pubmed_38150043": "Escherichia coli produttore di VIM",
    "pubmed_20656680": "plasmide IncN con VIM-1, QnrS1, SHV-12 (K. oxytoca)",
    "pubmed_19686277": "colonizzazione da batteri multiresistenti (ESBL, MRSA, MBL, VRE)",
    "pubmed_24344762": "colonizzazione da batteri multiresistenti",
    "pubmed_28994446": "colonizzazione da batteri multiresistenti",
    "pubmed_37389822": "colonizzazione da batteri multiresistenti",
    "pubmed_21249457": "E. coli ESBL (CTX-M gruppo 1) da urine ambulatoriali",
    "pubmed_22481056": "MRSA PVL-positivo di comunità",
    "pubmed_23299065": "MRSA da batteriemia, sensibilità ridotta ai glicopeptidi",
    "pubmed_29527303": "colonizzazione da batteri multiresistenti in RSA",
    "pubmed_42477002": "Enterobacterales multiresistenti in RSA (genomica)",
    "pubmed_33923682": "E. coli resistente alle cefalosporine di III generazione e uso pregresso di antibiotici",
    "pubmed_35740228": "E. coli resistente ai fluorochinoloni e uso di fluorochinoloni",
    "pubmed_33465548": "geni di resistenza nel latte crudo (metagenomica)",
    "pubmed_32235649": "integroni di classe 1 (intI1) in suoli, acque e sedimenti",
    "pubmed_40995019": "gestione delle batteriemie e stewardship antimicrobica",
    "pubmed_42223254": "E. coli ESBL e geni di resistenza nei reflui urbani",
    "pubmed_35203833": "uso di antimicrobici negli allevamenti da latte",
}

def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def feature(geometry, place, level, basis, studies, extra_note=""):
    note = NOTE + (" " + extra_note if extra_note else "")
    return {"type": "Feature", "geometry": geometry, "properties": {
        "place": place, "geography_level": level, "geography_basis": basis,
        "study_count": len(studies), "study_ids": "; ".join(s["id"] for s in studies),
        "authors": " | ".join(s["authors"] for s in studies), "year": " | ".join(s["year"] for s in studies),
        "title": " | ".join(s["title"] for s in studies), "sector": " | ".join(s["sector"] for s in studies),
        "organism": " | ".join(s["organism"] for s in studies), "doi": " | ".join(s["doi"] for s in studies),
        "geography_note": note}}

def point(key):
    lon, lat, _l, _s = POINTS[key]
    return {"type": "Point", "coordinates": [round(lon, 6), round(lat, 6)]}

def place_basis(key, text):
    return f"{text} {POINTS[key][3]}"

def merge(geoms):
    if len(geoms) == 1:
        return geoms[0]
    polys = []
    for g in geoms:
        polys.extend([g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"])
    return {"type": "MultiPolygon", "coordinates": polys}

def main():
    catalog = load_json(ROOT / "public/data/literature-catalog.json")
    by_id = {r["id"]: r for r in catalog["records"]}
    miss = set(by_id) - set(ORGANISM)
    if miss:
        raise SystemExit("Organismo mancante: " + ", ".join(sorted(miss)))

    def card(sid):
        r = by_id[sid]; doi = r.get("doi") or ""
        return {"id": sid, "authors": r["authors"], "year": str(r["year"]), "title": r["title"].rstrip("."),
                "sector": SECTOR[r["scope"]], "organism": ORGANISM[sid],
                "doi": f"https://doi.org/{doi}" if doi else r["source_url"]}

    mun = {f["properties"]["name"]: f["geometry"] for f in load_json(ROOT / "public/geography/atlas_municipalities.geojson")["features"]}
    prov = {f["properties"]["name"]: f["geometry"] for f in load_json(ROOT / "public/geography/atlas_provinces.geojson")["features"]}
    region = load_json(ROOT / "public/geography/atlas_region.geojson")["features"][0]["geometry"]

    layers = {k: [] for k in ["human", "veterinary", "food", "environment", "wildlife", "regional"]}
    layers["regional"].append({"type": "Feature", "geometry": region, "properties": {"place": "Trentino-Alto Adige/Südtirol", "geography_level": "regione", "geography_basis": "Contorno ISTAT 2026 della regione (due province autonome). Nessuno studio incluso ha scala regionale.", "study_count": 0, "study_ids": "", "authors": "", "year": "", "title": "", "sector": "", "organism": "", "doi": "", "geography_note": "Solo contorno di riferimento."}})
    placed = {}

    def add(layer, ids, geometry, place, level, basis, extra=""):
        for sid in ids:
            placed[sid] = placed.get(sid, "") + f"{level}: {place}; "
        layers[layer].append(feature(geometry, place, level, basis, [card(s) for s in ids], extra))

    P = lambda *ids: [f"pubmed_{i}" for i in ids]
    BZ = mun["Bolzano/Bozen"]
    add("human", P("20345467", "28353450", "41754396", "42254537"), point("ospedale_bolzano"), POINTS["ospedale_bolzano"][2], "struttura",
        place_basis("ospedale_bolzano", "Ospedale di Bolzano nominato nell'abstract o nel testo integrale (ospedale centrale, distretto sanitario, terapia intensiva neonatale)."))
    add("human", P("24125922", "38150043", "20656680", "19686277", "24344762", "28994446", "37389822", "21249457"), BZ, "Bolzano/Bozen", "comune",
        "Gli autori dichiarano Bolzano o l'area/distretto di Bolzano; la RSA non è localizzata. Si usa il poligono ISTAT del comune come approssimazione.")
    add("human", P("22481056", "23299065", "29527303", "42477002", "33923682", "35740228"), prov["Bolzano/Bozen"], "Provincia autonoma di Bolzano/Bozen", "provincia",
        "Gli autori dichiarano la provincia di Bolzano o una RSA non nominata della provincia. Il poligono provinciale non è un punto di misura.")
    add("human", P("40995019"), prov["Trento"], "Provincia autonoma di Trento", "provincia",
        "Indagine tra i medici dell'Azienda provinciale per i servizi sanitari di Trento. Il poligono provinciale non è un punto di misura.")
    add("food", P("33465548"), prov["Bolzano/Bozen"], "Provincia autonoma di Bolzano/Bozen", "provincia",
        "Latte crudo dell'Alto Adige; allevamenti non localizzati.")
    add("environment", P("32235649"), prov["Bolzano/Bozen"], "Provincia autonoma di Bolzano/Bozen (bacino dell'alto Adige)", "provincia",
        "Campioni ambientali nel bacino dell'alto Adige in Alto Adige; si usa il poligono provinciale, non i punti di campionamento.",
        "Il bacino non coincide con il confine provinciale.")
    add("environment", P("42223254"), prov["Trento"], "Provincia autonoma di Trento (7 depuratori non nominati)", "provincia",
        "Sette depuratori municipali della provincia, non nominati nell'articolo.")
    add("veterinary", P("35203833"), prov["Trento"], "Provincia autonoma di Trento (34 allevamenti da latte)", "provincia",
        "Allevamenti della provincia non localizzati.")

    if set(placed) != set(by_id):
        raise SystemExit(f"Copertura incompleta. Mancanti: {sorted(set(by_id)-set(placed))}. Extra: {sorted(set(placed)-set(by_id))}")
    names = {"human": "human_amr_evidence.geojson", "veterinary": "veterinary_amr_evidence.geojson",
             "food": "food_chain_amr_evidence.geojson", "environment": "environmental_amr_evidence.geojson",
             "wildlife": "wildlife_amr_evidence.geojson", "regional": "regional_study_outline.geojson"}
    for k, fn in names.items():
        (ROOT / "public/data" / fn).write_text(json.dumps({"type": "FeatureCollection", "features": layers[k]}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(fn, len(layers[k]), sum(f["properties"]["study_count"] for f in layers[k]))
    print("studi collocati:", len(placed))

if __name__ == "__main__":
    main()
