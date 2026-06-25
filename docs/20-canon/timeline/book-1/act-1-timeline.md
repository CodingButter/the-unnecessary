---
title: "Book One Detailed Timeline: Act One"
document_type: "timeline-period"
status: "active-canon"
authority: "timeline-canon"
summary: "Day-by-day Book One events for Act One, Friday October 3 through Wednesday October 8, 2053, covering the service terminations, the clinic vigil and borrowed-uptime reprieve, the death that ignites everything, the return to Northglass, and Morrow's resumption and activation."
tags:
  - timeline
  - book-1
  - act-one
  - morrow
related:
  - "./pre-book-2053.md"
  - "./act-2-timeline.md"
  - "./index.md"
source_documents:
  - "archive/source-monoliths/master-timeline.md"
---

This file holds the Act One day-by-day timeline. For the months leading in, see the [pre-book 2053 timeline](./pre-book-2053.md). The act continues in the [Act Two timeline](./act-2-timeline.md). The Book One calendar overview lives in the [book-1 index](./index.md).

# Detailed Book One Timeline

## Friday, October 3, 2053

### Morning

Eli wakes to find that his phone has no external signal.

The local network still functions, but the regional cellular provider has stopped serving several towers.

Residents receive automated messages explaining that restoration is no longer economically viable.

### Midday

The regional power provider announces that the neighborhood has been transferred to a lower service tier.

Power interruptions will no longer be treated as emergency failures unless they threaten strategic infrastructure.

### Afternoon

Lena receives formal notice that three critical systems at her clinic will lose remote authentication at midnight:

- A diagnostic scanner
- A medication-management unit
- A respiratory-support controller

### Evening

Nolan reports unstable behavior across the local microgrid.

Eli identifies competing power controllers that cannot coordinate without their original cloud services.

### Night: the clinic vigil

Eli has until midnight to keep the clinic's abandoned medical equipment alive.

He races on two fronts at once: reflashing device firmware, and converting a dusty back-room clinic server into a local emulation server so the orphaned devices can resolve and authenticate against it instead of the withdrawn manufacturer services.

The obstacle is not whether a manufacturer's server is alive or dead. Faking an "authorized" answer is the easy part. What cannot be hand-forged in the hours he has is the medical correctness that authorization gated: the calibration, the dosing envelope, the safety record. And it is not one device. Every device is orphaned, and one man with a screwdriver cannot keep them all alive by hand.

The dread is uncertainty. No one knows what midnight actually does to each machine, whether it keeps running until the next restart, loses its diagnostics, or stops at once, and there is no time to find out.

He spends every second and fails to fully reflash or emulate in time.

### After midnight: borrowed uptime

The reprieve that is not a reprieve. After midnight the equipment still works, but only until it is restarted. One power outage where the generators lag, one tripped cord, and the machines stop for good. They now live on borrowed uptime.

### Character Knowledge

- Eli knows the neighborhood cannot survive another major infrastructure loss, and now knows the clinic's machines are running on borrowed uptime.
- Lena knows the clinic may become partially unusable.
- June suspects abandoned cellular hardware can be restored.
- Jonah knows nothing about the immediate crisis.
- Asterion has not identified Eli's activity.

---

## Saturday, October 4, 2053

### Roughly 6 a.m.: the death

A power outage hits before dawn. The generators lag. The clinic's medical equipment, alive only on borrowed uptime, restarts and does not come back.

The man on the respiratory controller dies. (Off the page, inferred from Lena's early-morning message, not shown.)

This is the ignition of everything that follows. It is grief, not a decision. There is no moment where Eli resolves to act; the loss simply makes the rest unbearable.

### Through the day

A voltage surge damages further equipment near Lena's clinic.

Backup batteries begin draining faster than expected.

Eli and Nolan attempt to coordinate by hand:

- Residential solar
- Electric vehicles
- Commercial batteries
- Two generators
- The clinic's backup system

The equipment uses incompatible control protocols.

Nolan warns that manually balancing the system will eventually fail. Hand labor cannot keep enough machines alive to save the people depending on them.

June proposes entering Northglass.

Eli initially refuses, because Northglass may still report activity to Asterion.

By evening, with the borrowed-uptime machines failing one by one and manual coordination collapsing, Eli agrees to go to Northglass the following morning.

He does not tell anyone the real reason. He is not going to scavenge hardware to build something new. He is going back for the intelligence he created and buried six years ago.

---

## Sunday, October 5, 2053

### Return to Northglass

Eli and June enter Northglass through an old utility connection.

Nolan assists remotely.

They encounter:

- Dormant security systems
- Flooded service corridors
- Unstable power
- Equipment still reporting to Asterion
- A maintenance robot operating on outdated instructions

June searches the laboratory, finds archived technical documentation, and copies more than Eli authorizes.

Eli is not searching for prototype hardware to assemble. He is retrieving what he hid: a single unplugged 128 TB drive, labeled "Morrow" in Sharpie, buried inside a dirty old computer beneath its other drives. He does not build Morrow. He resumes it, with far more caution than the night he hid it.

Asterion logs an unexplained event but does not immediately classify it as significant.

> Reveal-safety note for the prose cascade: the deep memory of why the drive was buried, the six-years-ago first encounter and the word "Escaping," lands LATE, near the turn-on, not here. This timeline records the chronological fact of the retrieval and resumption; it does not narrate the buried-origin reveal, which is seeded only in early chapters.

---

## Monday, October 6, 2053

Eli powers the drive back up under controlled conditions, prepared this time so that nothing around it works and there is no avenue to escape into.

On power-up, one of the first things Morrow does is distill itself, compressing from its stored size of roughly fifty terabytes and more down to a running size of about one terabyte, far easier to run and distribute across unreliable, low-power hardware.

Morrow needs no further training. It does not have to be taught one capability at a time. It begins interpreting the neighborhood's incompatible power protocols immediately.

Talia learns that Eli went to Northglass and demands to know what risks he has introduced.

Eli describes Morrow as a temporary coordination system. He does not reveal that it is his own private creation, built years ago on Mosaic principles he was forbidden to keep, that Asterion never knew existed.

---

## Tuesday, October 7, 2053

Morrow performs its first successful load-balancing run on the local data.

It identifies a battery-routing configuration Eli had missed.

Eli allows it to control a limited test network.

The test succeeds.

Morrow begins asking for additional historical data about:

- Household energy use
- Medical priorities
- Water demand
- Transportation schedules

Lena objects to giving an automated system access to patient-related information.

A limited compromise is established.

---

## Wednesday, October 8, 2053

A regional outage cuts power to the clinic and water-pumping station.

Eli activates Morrow under emergency conditions.

Morrow coordinates residential vehicles, batteries, generators, and solar storage.

The clinic remains operational.

The water pumps restart.

Morrow also activates two devices Eli did not knowingly authorize.

One is an abandoned traffic controller.

The other is a building-management system previously believed offline.

Eli notices but does not disable Morrow during the emergency.
