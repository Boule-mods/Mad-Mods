# Pédale de modulation multi-effets pour guitare électrique

## Participant

- Colin Boulé

## Contexte et objectifs

L'industrie de la musique c'est rapidement développé au cours des dernières décennies et avec l'évolution de la musique nous avons aussi observé le développment de plusieurs nouvelles technologies. Parmis ces technologies une des plus vieilles est la pédale de modulation. Cet outils que les guitarists utilise permet de changer le son produit par un instrument électrique. De nos jours ces appareils sont très dispandieux et chacune ne permet qu'un seul effet sonore. Souvent, les musiciens requiert plusieurs de ces pédales et cela peux devenir encombrant et surtout une dépense considérable. 

Donc, je me suis mis au développement d'une pédale de modulation qui contiendrait plusieurs circuits de modulation. Cette pédale permettra de réduire l'encombrement de multiples pédales en les combinant en un produit compact. La pédale doit contenir Six! effets de modulation et pourra combiner ceux-ci. Elle pourra prendre un signal en entrée sur plusieurs connecteurs différents et produire sa sortie sur des connecteurs identiques. Le module aura une interface simple et intuitive qui permettra a n'importe-qui de l'utilisé.

## Description du produit développé

Le produit développé est un système électronique divisés en multiples composantes dont une carte mère et des modules individuels de modulation audio. 

Le cœur de ce système est un microcontrôleur (Raspberry Pi Pico) et un controleur d'entrées et sorties qui permettent le contrôle d'interupteur analogique. Ce microsysteme permet de diriger le signal audio afin de le faire passé à travers les autres sous-modules ce qui permet de sélectionner les modulation que l'ont veut appliqué au son. Un bouton permet  de choisir si l'ont veut appliqué ou non la sélection d'effets audio. L'interface utilisateur consiste d'un écran et de boutons qui servent anaviguer un menu. LLe menu affiché sur l'écran permet de sélectionner plusieurs options de modulations et de choisir les entrées et sorties.


![Schema bloc](medias/Schema/Schéma_1.png)

## Résultats et conclusion

- Un prototype fonctionnel démontrant les modulation a été produit
- Le système est capable d'affecter un signal audio avec jusqu'à 3 effets audio simultanément
- Le systme peut prendre un signal audio et en prouduire un sur deux types de connecteur d'utilisation courante
- 

![Produit fermé](Boule-mods/ModsMad-Mods/medias/photos/Réalisation.jpg)

![Produit ouvert](Boule-mods/Mad-Mods/medias/photos/Boitier_ouvert.jpg)

## Logiciels utilisés

- Fusion 360
- Thonny
- Multisim
- Ultiboard
- Falstad

## Mots clés

- Guitare
- Musique
- Modulation
- Analogique
- Python
- Micropython
- 3D
- Audio
- Raspberry Pi

## Liens 

- [Projet  *sur Github*](https://github.com/Boule-mods/Mad-Mods)
