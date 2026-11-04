-- Projet 2 : crée les tables de la base `usine` et charge les CSV de donnees/.
-- Lancement (depuis ce dossier) :
--   createdb -U postgres usine
--   psql -U postgres -d usine -f charger_base.sql

DROP TABLE IF EXISTS production, standards, charges_fixes, prix_spot;

CREATE TABLE standards (
    produit           text PRIMARY KEY,
    kg_std            numeric,  -- kg de matière par pièce
    prix_matiere_std  numeric,  -- €/kg
    h_mo_std          numeric,  -- heures de main-d'œuvre par pièce
    taux_horaire_std  numeric,  -- €/h
    kwh_std           numeric,  -- kWh par pièce
    prix_elec_std     numeric,  -- €/MWh (budget)
    cadence_pieces_h  numeric,
    prix_vente        numeric   -- € par pièce
);

CREATE TABLE production (
    mois               date,
    produit            text REFERENCES standards,
    quantite_bonne     integer,
    quantite_rebut     integer,
    kg_reel            numeric,
    prix_matiere_reel  numeric,
    h_mo_reelles       numeric,
    taux_horaire_reel  numeric,
    kwh_reel           numeric,
    prix_elec_reel     numeric,  -- €/MWh, prix spot France réel du mois
    heures_ouverture   integer,
    PRIMARY KEY (mois, produit)
);

CREATE TABLE charges_fixes (
    mois     date,
    poste    text,
    montant  numeric,
    PRIMARY KEY (mois, poste)
);

CREATE TABLE prix_spot (
    mois              date PRIMARY KEY,
    prix_spot_eur_mwh numeric
);

\copy standards     FROM 'donnees/standards.csv'         CSV HEADER
\copy production    FROM 'donnees/production.csv'        CSV HEADER
\copy charges_fixes FROM 'donnees/charges_fixes.csv'     CSV HEADER
\copy prix_spot     FROM 'donnees/prix_spot_mensuel.csv' CSV HEADER

SELECT 'production' AS table_, count(*) FROM production
UNION ALL SELECT 'standards', count(*) FROM standards
UNION ALL SELECT 'charges_fixes', count(*) FROM charges_fixes
UNION ALL SELECT 'prix_spot', count(*) FROM prix_spot;
