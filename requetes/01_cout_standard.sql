-- Coût standard d'une pièce et marge unitaire, par produit
SELECT produit,
       ROUND(kg_std * prix_matiere_std, 2)                    AS matiere,
       ROUND(h_mo_std * taux_horaire_std, 2)                  AS main_oeuvre,
       ROUND(kwh_std * prix_elec_std / 1000, 2)               AS energie,
       ROUND(kg_std * prix_matiere_std
           + h_mo_std * taux_horaire_std
           + kwh_std * prix_elec_std / 1000, 2)               AS cout_standard,
       ROUND(prix_vente - (kg_std * prix_matiere_std
           + h_mo_std * taux_horaire_std
           + kwh_std * prix_elec_std / 1000), 2)              AS marge_unitaire
FROM standards;
