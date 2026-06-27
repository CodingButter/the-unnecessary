---
title: "Family Tree"
document_type: "generated-diagram"
status: "generated"
authority: "character-canon"
summary: "Generated family structure for The Unnecessary. Parent/child is derived from the stored father/mother edges; spouse and sibling are symmetric."
tags:
  - character
  - relationships
  - generated
related:
  - "../profile-spec.md"
source_documents: []
---

# Family Tree

> DO NOT EDIT - generated from profiles by scripts/build-relationship-graph.py

```mermaid
%% DO NOT EDIT - generated from profiles by scripts/build-relationship-graph.py
graph TD
    n_bell_nora["Nora Bell"]
    n_kade_adrian["Adrian Kade"]
    n_kade_alexandra["Alexandra Kade"]
    n_mercer_amelia["Amelia Mercer"]
    n_mercer_celeste["Celeste Mercer"]
    n_mercer_elaine["Elaine Mercer"]
    n_mercer_jonah["Jonah Mercer"]
    n_mercer_julian["Julian Mercer"]
    n_mercer_malcolm["Malcolm Mercer"]
    n_okafor_amara["Amara Okafor"]
    n_okafor_lena["Dr. Lena Okafor"]
    n_park_daniel["Daniel Park"]
    n_park_june["June Park"]
    n_park_soojin["Soo-jin Park"]
    n_rook_daniel["Daniel Rook"]
    n_rook_eli["Elias “Eli” Rook"]
    n_rook_ruth["Ruth Rook"]
    n_vance_marcus["Marcus Vance"]
    n_vance_mason["Mason Vance"]
    n_voss_evan["Evan Voss"]
    n_voss_mara["Mara Voss"]
    n_kade_adrian -->|"father"| n_kade_alexandra
    n_mercer_celeste -->|"mother"| n_mercer_amelia
    n_mercer_celeste -->|"mother"| n_mercer_julian
    n_mercer_elaine -->|"mother"| n_mercer_jonah
    n_mercer_jonah -->|"father"| n_mercer_amelia
    n_mercer_jonah -->|"father"| n_mercer_julian
    n_mercer_malcolm -->|"father"| n_mercer_jonah
    n_okafor_amara -->|"mother"| n_okafor_lena
    n_park_daniel -->|"father"| n_park_june
    n_park_soojin -->|"mother"| n_park_june
    n_rook_daniel -->|"father"| n_rook_eli
    n_rook_ruth -->|"mother"| n_rook_eli
    n_vance_marcus -->|"father"| n_vance_mason
    n_voss_mara -->|"mother"| n_voss_evan
    n_bell_nora ---|"former-spouse"| n_rook_eli
    n_mercer_amelia ---|"sibling"| n_mercer_julian
    n_mercer_celeste ---|"spouse"| n_mercer_jonah
    n_mercer_elaine ---|"spouse"| n_mercer_malcolm
    n_park_daniel ---|"spouse"| n_park_soojin
    n_rook_daniel ---|"spouse"| n_rook_ruth
```
