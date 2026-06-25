---
title: "Infrastructure State at Story Start"
document_type: "continuity-baseline"
status: "active"
authority: "continuity"
summary: "The operational state of energy, communications, cloud dependency, and identity and access infrastructure as of time zero, recording what is up, degraded, or failed under canon failure rules and hard plot restrictions."
tags:
  - continuity
  - technology-state
  - infrastructure
  - energy
  - communications
related:
  - "crown.md"
  - "morrow.md"
source_documents:
  - "docs/20-canon/technology/infrastructure/energy.md"
  - "docs/20-canon/technology/infrastructure/communications.md"
  - "docs/20-canon/technology/infrastructure/cloud-dependency.md"
  - "docs/20-canon/technology/infrastructure/identity-and-money.md"
  - "docs/20-canon/technology/failure-rules.md"
  - "docs/20-canon/technology/hard-plot-restrictions.md"
---

> No manuscript chapters have been approved. These files contain pre-draft starting conditions only.

# Infrastructure State at Story Start

This file records the operational state of the world's core infrastructure at time zero, the opening of Book One, across four dimensions: energy, communications, cloud dependency, and identity and access. The defining condition is uneven withdrawal. Civilization has not collapsed; services have been abandoned unevenly, so the same system is reliable in protected regions and degraded or failed in unsupported ones. Authority for each dimension lives in the cited canon files; this file states only the time-zero state.

## Energy

Energy is the primary constraint in unsupported communities at time zero. Electricity matters more than money there.

Status by region at story start:

- Up in protected enclaves and prioritized recipients. The national grid still exists, and automated utilities prioritize protected enclaves, strategic industry, government facilities, transportation corridors, data centers, military systems, and paying municipalities. Reliability there comes from redundancy and maintenance, not limitless energy. Protected enclaves draw on private solar fields, wind power, advanced storage, small modular reactors, fuel reserves, corporate grid contracts, and automated demand management.
- Degraded or emergency-only in unsupported regions. Other regions receive reduced, intermittent, or emergency-only service.
- Improvised locally. Communities preserve power with microgrids that combine local generation, batteries, vehicles, and controlled demand. Available local sources at time zero include aging regional grids, residential solar, wind installations, electric-vehicle batteries, industrial battery banks, natural-gas generators, hydroelectric sources, salvaged fuel cells, and local microgrids.

Failure mode in effect at time zero: microgrids are difficult to manage because equipment from different manufacturers was never designed to cooperate. Communities cannot power everything simultaneously, so load shedding is a standing condition, and the choices it forces are political as well as technical. Coordinated microgrid management is named in canon as one of Morrow's first important uses, but at story start Morrow is dormant and not running (per the origin revision it exists, finished but powered down on a hidden drive, rather than not existing at all), so that coordination is not yet in effect. The unmanaged, mismatched state of community power is the time-zero baseline.

## Communications

The global internet still exists at time zero but is fragmented by service quality, ownership, and access.

Status by region at story start:

- Up in protected regions, which experience fast and reliable connectivity.
- Degraded in unsupported regions, which experience intermittent access, bandwidth limits, unreliable routing, authentication failures, missing cloud services, regional shutdowns, high latency, and corporate blocking.

Local networking at time zero: communities build local networks from abandoned fiber, Wi-Fi relays, mesh radios, cellular equipment, rooftop links, repurposed satellite terminals, and wired neighborhood connections. These can support local communication even without the global internet. Many cellular towers remain physically intact, but a tower needs power, backhaul connectivity, spectrum authorization, control software, maintenance, and compatible subscriber systems to function. Communities can repurpose towers for local service, but national roaming and commercial identity systems may not work.

Satellites at time zero: satellite communication remains available but controlled. Asterion and other companies restrict access through authentication, pricing, geographic limits, bandwidth allocation, and terminal certification. Illegal or modified terminals exist and are detectable when transmitting.

Earth to Mars at time zero: communications between Earth and Mars experience unavoidable delays based on orbital distance, with one-way delays from several minutes to more than twenty minutes. There is no real-time conversation between Earth and Mars, so Martian systems must operate autonomously. This is a permanent physical condition, not a failure, and it holds from the first page.

## Cloud Dependency

At time zero many devices still physically work but depend on remote services for login, licenses, safety checks, updates, identity, payment, coordination, data storage, and diagnostics. When companies withdraw those services, devices become partially or completely unusable. This stranding is a standing condition at story start, not an event.

Corporate locks in effect at time zero include encrypted firmware, expired certificates, proprietary connectors, remote-disable systems, subscription requirements, locked replacement parts, centralized scheduling platforms, and mandatory cloud verification.

Eli's specialty, removing these dependencies, is an established starting capability of his at time zero. He may replace firmware, stand up local emulation servers that redirect a device's resolution away from the manufacturer, generate local certificates, translate protocols, bypass remote checks, create local identity systems, isolate dangerous features, and build replacement control software.

Per the Act One revision, the obstacle is not that a manufacturer's server is dead rather than alive. Once a device's resolution is redirected to a local emulator, the upstream server's liveness is irrelevant: a live-but-refusing manufacturer is no different from a dead one, because if a device demands a signature only the manufacturer's key can produce, a dead manufacturer cannot produce it either, and the local fix is identical in both cases. The real obstacle is threefold: the labor of reverse-engineering and emulating each device, which takes hours to days; the scale, since every orphaned device needs this and one technician with a screwdriver cannot keep them all alive by hand; and life-critical safety. The canon failure rule applies from the start: bypassing a system may reduce safety, so every repair can create a new risk. Faking "authorized = yes" is the easy part. What cannot be hand-forged in time is the medical correctness the authorization had gated, the calibration, dosing envelope, and safety record. Removing a medical-device authentication lock may also disable automatic calibration records; a respiratory controller left on a hand-forged "yes," stripped of that gating, kills the person it keeps alive slowly while reporting that everything is fine.

## Identity and Access

At time zero most protected services require verified digital identity. Identity systems connect financial accounts, housing access, healthcare, education, travel, employment history, service eligibility, and enclave permissions. People outside supported systems may retain legal citizenship while losing practical access to institutions. This split between legal status and practical access is a defining starting condition.

Money at time zero: traditional national currencies still exist, and digital payment remains dominant inside protected systems. Outside them, people use government currency, local digital credits, barter, labor exchange, energy credits, physical goods, community ledgers, and corporate tokens. No single alternative currency replaces national money.

Access over wealth at time zero: a person may hold nominal financial assets yet be unable to access medical systems, transportation, protected housing, advanced AI, corporate supply chains, or launch infrastructure. Ownership is increasingly dependent on recognition by the systems enforcing it. This is the baseline condition of the story world and is true from the opening.

## Notes on Scope

No planned outage, upgrade, or repair is recorded here as having occurred. The states above describe standing conditions at time zero. Any change to this infrastructure driven by Eli's work or by Morrow's resumption is a Book One development and is not recorded here as already true.

Per the Act One revision, the "borrowed uptime" mechanic is a clarification of the cloud-dependency rules already stated above, not a new time-zero condition: a stranded device whose authorization or coordination has lapsed may keep working until it is next restarted, then fail to come back, so it lives on the uptime it already had. This is consistent with the standing cloud-dependency and load-shedding conditions but is dramatized as an early Book One event (the clinic night of October 3, where equipment survives past midnight but only until the next power interruption), not asserted here as a time-zero fact.
