---
title: "Social Web"
document_type: "generated-diagram"
status: "generated"
authority: "character-canon"
summary: "Generated overall social web: every stored, in-vocabulary relationship edge across the cast of The Unnecessary."
tags:
  - character
  - relationships
  - generated
related:
  - "../profile-spec.md"
source_documents: []
---

# Social Web

> DO NOT EDIT - generated from profiles by scripts/build-relationship-graph.py

```mermaid
%% DO NOT EDIT - generated from profiles by scripts/build-relationship-graph.py
graph LR
    n_adeyemi_bayo["Mr. Adeyemi"]
    n_avery_nolan["Nolan Avery"]
    n_bell_nora["Nora Bell"]
    n_caldwell_emma["The Caldwell Girl"]
    n_dembele_sekou["Sékou Dembélé"]
    n_diallo_aminata["Aminata Diallo"]
    n_dorsey_ray["Raymond Dorsey"]
    n_herrera_tomas["Tomas Herrera"]
    n_kade_adrian["Adrian Kade"]
    n_kade_alexandra["Alexandra Kade"]
    n_mercer_amelia["Amelia Mercer"]
    n_mercer_celeste["Celeste Mercer"]
    n_mercer_elaine["Elaine Mercer"]
    n_mercer_jonah["Jonah Mercer"]
    n_mercer_julian["Julian Mercer"]
    n_mercer_malcolm["Malcolm Mercer"]
    n_morrow["Morrow"]
    n_okafor_amara["Amara Okafor"]
    n_okafor_lena["Dr. Lena Okafor"]
    n_park_daniel["Daniel Park"]
    n_park_june["June Park"]
    n_park_soojin["Soo-jin Park"]
    n_reed_talia["Talia Reed"]
    n_reyes_hector["Hector Reyes"]
    n_rook_daniel["Daniel Rook"]
    n_rook_eli["Elias “Eli” Rook"]
    n_rook_ruth["Ruth Rook"]
    n_sharma_priya["Priya Sharma"]
    n_vale_sera["Sera Vale"]
    n_vance_marcus["Marcus Vance"]
    n_vance_mason["Mason Vance"]
    n_vega_marisol["Marisol Vega"]
    n_vesely_marek["Marek Vesely"]
    n_voss_evan["Evan Voss"]
    n_voss_mara["Mara Voss"]
    n_adeyemi_bayo -->|"patient-of"| n_herrera_tomas
    n_adeyemi_bayo -->|"patient-of"| n_okafor_lena
    n_avery_nolan ---|"colleague"| n_dorsey_ray
    n_avery_nolan ---|"colleague"| n_rook_eli
    n_bell_nora ---|"colleague"| n_kade_adrian
    n_bell_nora ---|"former-spouse"| n_rook_eli
    n_caldwell_emma -->|"patient-of"| n_okafor_lena
    n_caldwell_emma -->|"patient-of"| n_sharma_priya
    n_dembele_sekou ---|"acquaintance"| n_okafor_lena
    n_dembele_sekou ---|"colleague"| n_reed_talia
    n_dembele_sekou ---|"colleague"| n_vega_marisol
    n_diallo_aminata -->|"patient-of"| n_okafor_lena
    n_dorsey_ray ---|"neighbor"| n_rook_eli
    n_dorsey_ray ---|"neighbor"| n_vega_marisol
    n_herrera_tomas ---|"colleague"| n_sharma_priya
    n_herrera_tomas -->|"reports-to"| n_okafor_lena
    n_kade_alexandra -->|"father"| n_kade_adrian
    n_mercer_amelia ---|"sibling"| n_mercer_julian
    n_mercer_amelia -->|"father"| n_mercer_jonah
    n_mercer_amelia -->|"mother"| n_mercer_celeste
    n_mercer_celeste ---|"spouse"| n_mercer_jonah
    n_mercer_elaine ---|"spouse"| n_mercer_malcolm
    n_mercer_jonah ---|"friend"| n_rook_eli
    n_mercer_jonah -->|"father"| n_mercer_malcolm
    n_mercer_jonah -->|"mother"| n_mercer_elaine
    n_mercer_julian ---|"friend"| n_rook_eli
    n_mercer_julian -->|"father"| n_mercer_jonah
    n_mercer_julian -->|"mother"| n_mercer_celeste
    n_okafor_lena ---|"colleague"| n_rook_eli
    n_okafor_lena ---|"friend"| n_rook_eli
    n_okafor_lena -->|"mother"| n_okafor_amara
    n_park_daniel ---|"spouse"| n_park_soojin
    n_park_june ---|"acquaintance"| n_vance_mason
    n_park_june -->|"creator-of"| n_morrow
    n_park_june -->|"father"| n_park_daniel
    n_park_june -->|"mentor"| n_rook_eli
    n_park_june -->|"mother"| n_park_soojin
    n_park_soojin -->|"patient-of"| n_okafor_lena
    n_reed_talia ---|"colleague"| n_vega_marisol
    n_reed_talia ---|"rival"| n_rook_eli
    n_reyes_hector -->|"patient-of"| n_okafor_lena
    n_rook_daniel ---|"spouse"| n_rook_ruth
    n_rook_eli ---|"adversary"| n_vale_sera
    n_rook_eli ---|"neighbor"| n_vance_marcus
    n_rook_eli -->|"creator-of"| n_morrow
    n_rook_eli -->|"father"| n_rook_daniel
    n_rook_eli -->|"mentor"| n_kade_adrian
    n_rook_eli -->|"mother"| n_rook_ruth
    n_sharma_priya -->|"reports-to"| n_okafor_lena
    n_vale_sera -->|"reports-to"| n_kade_adrian
    n_vance_marcus ---|"neighbor"| n_vega_marisol
    n_vance_mason -->|"father"| n_vance_marcus
    n_vesely_marek -->|"patient-of"| n_okafor_lena
    n_voss_evan -->|"mother"| n_voss_mara
```
