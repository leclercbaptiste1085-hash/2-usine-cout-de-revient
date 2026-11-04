-- Coût réel (variable) par pièce bonne, Carter moteur, par mois
SELECT mois,
       ROUND((kg_reel * prix_matiere_reel
            + h_mo_reelles * taux_horaire_reel
            + kwh_reel * prix_elec_reel / 1000) / quantite_bonne, 2) AS cout_reel_piece
FROM production
WHERE produit = 'Carter moteur'
ORDER BY mois;
