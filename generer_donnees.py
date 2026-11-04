"""Projet 2 - Genere les donnees de l'usine fictive dans le dossier donnees/.

Prix de l'electricite : reels (moyennes mensuelles France publiees par Ember, source ENTSO-E).
Production et couts : simules avec une graine fixe, donc identiques a chaque execution.
"""
import csv
import io
import random
import urllib.request
from pathlib import Path

URL_PRIX = ("https://files.ember-energy.org/public-downloads/price/outputs/"
            "european_wholesale_electricity_price_data_monthly.csv")
DOSSIER = Path(__file__).parent / "donnees"
DOSSIER.mkdir(exist_ok=True)
random.seed(42)

# produit : kg de matiere, EUR/kg, heures de main-d'oeuvre, EUR/h, kWh, pieces/h, prix de vente EUR, volume pour 21 jours
STANDARDS = {
    "Carter moteur":        (4.2, 2.40, 0.25, 38.0, 18.0, 40, 38.0, 9000),
    "Support batterie":     (2.1, 2.40, 0.15, 38.0,  9.5, 60, 19.0, 14000),
    "Boitier electronique": (0.9, 2.40, 0.10, 38.0,  4.5, 90, 10.0, 20000),
}
PRIX_ELEC_BUDGET = 80.0  # EUR/MWh retenu au budget 2025
JOURS_OUVRES = [21, 20, 21, 22, 19, 21, 22, 10, 22, 23, 20, 20]  # aout : fermeture de 2 semaines
CHARGES_FIXES = {"Amortissements": 90000, "Maintenance": 45000,
                 "Encadrement production": 45000, "Structure et administration": 70000}


def ecrire(nom, entetes, lignes):
    with open(DOSSIER / nom, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(entetes)
        w.writerows(lignes)


# 1. Prix spot reels, France, 2022 a 2025
with urllib.request.urlopen(URL_PRIX) as reponse:
    lignes = csv.DictReader(io.TextIOWrapper(reponse, encoding="utf-8"))
    prix = {l["Date"]: float(l["Price (EUR/MWhe)"]) for l in lignes
            if l["Country"] == "France" and "2022" <= l["Date"][:4] <= "2025"}
ecrire("prix_spot_mensuel.csv", ["mois", "prix_spot_eur_mwh"], sorted(prix.items()))

# 2. Couts standards par produit
ecrire("standards.csv",
       ["produit", "kg_std", "prix_matiere_std", "h_mo_std", "taux_horaire_std",
        "kwh_std", "prix_elec_std", "cadence_pieces_h", "prix_vente"],
       [[p, *s[:5], PRIX_ELEC_BUDGET, s[5], s[6]] for p, s in STANDARDS.items()])

# 3. Production reelle 2025, une ligne par mois et par produit
production = []
for m in range(12):
    mois = f"2025-{m + 1:02d}-01"
    for p, (kg, pmat, h, taux, kwh, cadence, pv, vol) in STANDARDS.items():
        fabrique = round(vol * JOURS_OUVRES[m] / 21 * random.gauss(1, 0.06))
        rebut = round(fabrique * random.uniform(0.02, 0.06))
        production.append([
            mois, p, fabrique - rebut, rebut,
            round(fabrique * kg * random.uniform(1.00, 1.04), 1),
            round(pmat * random.gauss(1, 0.05), 3),
            round(fabrique * h * random.uniform(0.97, 1.08), 1),
            round(taux * random.uniform(1.00, 1.03), 2),
            round(fabrique * kwh * random.uniform(0.98, 1.06)),
            prix[mois],
            JOURS_OUVRES[m] * 16,  # 2 equipes de 8 heures
        ])
ecrire("production.csv",
       ["mois", "produit", "quantite_bonne", "quantite_rebut", "kg_reel", "prix_matiere_reel",
        "h_mo_reelles", "taux_horaire_reel", "kwh_reel", "prix_elec_reel", "heures_ouverture"],
       production)

# 4. Charges fixes mensuelles
charges = []
for m in range(12):
    for poste, montant in CHARGES_FIXES.items():
        alea = 1 if poste == "Amortissements" else random.gauss(1, 0.05)
        charges.append([f"2025-{m + 1:02d}-01", poste, round(montant * alea)])
ecrire("charges_fixes.csv", ["mois", "poste", "montant"], charges)

print("4 fichiers ecrits dans", DOSSIER)
