---
title: "Decision 049: The Device-Emulation Obstacle Is Scale and Life-Critical Safety, Not Dead Versus Live Servers"
document_type: "decision"
status: "active"
authority: "governance"
summary: "Corrects a technically false framing: redirecting a device's resolution to a local emulator makes upstream liveness irrelevant, so a live-but-refusing manufacturer is no different from a dead one. The real obstacle is threefold: labor per device, scale across every orphaned device, and life-critical medical-correctness safety that cannot be hand-forged in time."
tags: ["decision", "technology", "infrastructure", "act-1", "morrow", "continuity"]
related:
  - "../../../20-canon/technology/infrastructure/cloud-dependency.md"
  - "../../../20-canon/characters/profiles/eli-rook.md"
  - "../index.md"
source_documents:
  - "docs/30-plot/book-1/act-1-revision-morrow-origin.md"
---

## Decision 049: The Device-Emulation Obstacle Is Scale and Life-Critical Safety, Not Dead Versus Live Servers

**Status:** Locked for Current Draft
**Category:** Technology

### Decision

The obstacle to keeping abandoned smart devices working is not whether their upstream servers are dead or alive. Redirecting a device's resolution to a local emulation server makes the upstream server's liveness irrelevant. A live but refusing manufacturer is no different from a dead one: if a device demands a signature only the manufacturer's key can produce, a live manufacturer that refuses and a dead manufacturer that no longer exists both leave the device in the same state, and the fix is identical.

The real obstacle is threefold, and it is the seed of the whole arc:

1. **Labor per device.** Reverse-engineering one device's API shape and standing up an emulator for it takes hours to days.
2. **Scale.** It is not one device. Every device is orphaned. One person with a screwdriver cannot keep them all alive by hand.
3. **Life-critical safety.** Faking "authorized = yes" is the easy part. What cannot be hand-forged in time is the medical correctness the authorization gated: the calibration, the dosing envelope, the safety record. A doorbell that runs wrong rings at the wrong time; a respiratory controller on a hand-forged "yes," stripped of that correctness, kills the man it keeps alive, slowly, correctly, while reporting that everything is fine.

### Previous or Alternative Direction

Earlier framing described the problem as needing to "emulate dead servers" and to bypass "dead authentication services," implying that a server being dead was the load-bearing difficulty. That distinction is technically false and is removed.

### Reason

The dead-versus-alive distinction does not survive scrutiny and would undercut the story's credibility for technical readers. Grounding the obstacle in labor, scale, and irreplaceable safety correctness is both accurate and dramatically stronger: it makes the problem something genius alone cannot brute-force by hand, which is exactly what forces Eli toward a system that can hold the whole city's devices at once, and it makes the lethal stakes concrete and quiet rather than abstract.

### Consequences

- Canon and prose that say "emulate dead servers" or "bypass dead authentication services" are reframed to scale plus life-critical safety.
- The Chapter 1 obstacle is reframed as the impossibility of correctness and scale, not the deadness of a server. Chapter 1 still seeds this without naming the full solution.
- The respiratory-controller line ("kills the man it keeps alive, slowly, correctly, while reporting that everything is fine") is preserved verbatim as canon-gold.
- This sets up the eventual scale solution: Morrow on the local hub emulating every server the city's devices need (recorded in Decision 052).

### Affected Documents

- `docs/20-canon/technology/infrastructure/cloud-dependency.md`
- `docs/20-canon/characters/profiles/eli-rook.md`
- `docs/40-blueprints/book-1/chapter-01-no-signal/blueprint.md`
- `docs/50-manuscript/book-1/chapter-01-no-signal.md`
- `docs/60-continuity/technology-state/infrastructure.md`

### Reconsider Only If

A grounded technical reason is found that makes upstream server liveness genuinely change the fix, in which case the correction itself would need deliberate revision.
