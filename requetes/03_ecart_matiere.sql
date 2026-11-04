-- Écart matière décomposé : effet quantité (kg consommés) et effet prix (€/kg), par produit sur 2025
SELECT p.produit,
       ROUND(SUM((p.kg_reel - (p.quantite_bonne + p.quantite_rebut) * s.kg_std) * s.prix_matiere_std)) AS ecart_quantite,
       ROUND(SUM((p.prix_matiere_reel - s.prix_matiere_std) * p.kg_reel))                              AS ecart_prix,
       ROUND(SUM(p.kg_reel * p.prix_matiere_reel
               - (p.quantite_bonne + p.quantite_rebut) * s.kg_std * s.prix_matiere_std))               AS ecart_total
FROM production p
JOIN standards s ON s.produit = p.produit
GROUP BY p.produit
ORDER BY p.produit;
