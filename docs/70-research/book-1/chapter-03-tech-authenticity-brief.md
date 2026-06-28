---
title: "Chapter 3 Technical-Authenticity Research Brief"
document_type: "research"
status: "reference"
authority: "research-grounding"
summary: "Real-world technical grounding for Chapter 3 (Eli's hacker/engineer work), produced by the research-consultant. Real-world fact for the drafter to ADAPT into the 2053 setting; NOT canon. Canon (cloud-dependency.md, foundational-rules.md) controls capability; nothing here grants Morrow/Crown or any device a new power."
source: "research-consultant (WebSearch/WebFetch + Context7); cited inline"
related:
  - "../../40-blueprints/book-1/chapter-03-borrowed-time/blueprint.md"
  - "../../20-canon/technology/infrastructure/cloud-dependency.md"
  - "../../20-canon/technology/foundational-rules.md"
---

# Chapter 3 Technical-Authenticity Research Brief

> Real-world grounding for the drafter to ADAPT. Canon controls capability; nothing here grants Morrow/Crown or any device a new power. The good news: reality and canon agree hard. The un-forgeable-correctness wall is not a contrivance; it is how this actually works.

## Methods in scope -> story effect
Stand-up local stand-in auth server, DNS redirect, MITM/sniffing, firmware reflash, and the medical-correctness wall. Each must read as authentic to a practitioner AND make a technical reader conclude unaided: "one man, one box, one night, three orphaned devices: no chance."

## How it actually works (real sequence, real tools)
1. **Redirect the phone-home (easy, fast).** A local resolver (`dnsmasq` with `address=/api.vendor.com/10.0.0.x`, or a Pi-hole-style sinkhole) so the device resolves its cloud endpoint to Eli's box. Minutes. [confirmed]
2. **See what it says (partly easy).** Box inline as a transparent proxy/gateway, or ARP-spoof the device, run `mitmproxy --mode transparent`. To read TLS, mitmproxy is its own CA and forges per-host certs on the fly, but the device must trust that CA. [confirmed]
3. **The trust wall (the real one).** A medical device worth its certification does **certificate pinning**: it trusts only the manufacturer's baked-in cert/public key, not any CA you install. You cannot side-load trust. Pinning is bypassed only by **patching the firmware itself**, which loops you into the reflash job. [confirmed]
4. **The challenge-response wall (un-passable, not just slow).** The device sends a nonce and expects a signature only the manufacturer's **private key** can produce. A local box has the public key, never the private one, so it **cannot mint a valid answer**; it can only stop the device from asking, by reflashing. [confirmed / device-specific inferred]
5. **Reflash by hand.** Find the debug port (UART/JTAG/SWD); dump with `flashrom` + a Bus Pirate or chip-off SPI read; unpack with `binwalk`; disassemble in `Ghidra`/`IDA`, optionally emulate in `QEMU`; locate and NOP-out the remote-check; rewrite. [confirmed]
6. **Secure boot blocks the rewrite.** Signed-firmware device verifies the image signature in ROM at boot; a patched image fails and **won't boot, bricked**. No private key to re-sign; you must find/defeat the verifier (bootloader bug, voltage-glitch fault injection), which is research, not a procedure. [confirmed / inferred]

## The "can't finish" math
RE of ONE device's protocol or firmware credibly is **hours to days** (canon agrees; web corroborates). Reflash adds dump + RE + patch + secure-boot defeat + write + verify, each with **bricking risk on the one machine a life depends on**. Three devices, one underpowered low-tier box, one set of hands, ~8 hours to midnight. Hours-each x three, serialized, no margin for a single brick: **it does not close, and a technical reader does that arithmetic themselves.** [confirmed]

## What makes it credible (the tells)
Right tool names in the right order (dnsmasq -> mitmproxy transparent -> binwalk -> Ghidra -> flashrom -> JTAG/DFU); knowing DNS+MITM is the *cheap* part; hitting **pinning**, then **the private-key signature**, then **secure boot** as three separate walls; treating a failed write as a brick, not a retry; verifying after writing. An expert's signal is fluency about what he *can't* do.

## The un-forgeable wall (the true limiter)
Forgeable by midnight: `authorized = yes`. Un-forgeable at any hour: the **calibration, dosing/pressure envelope, and accumulated safety record** the yes vouched for. Not bytes in the protocol he can replay; the manufacturer's traceable physical calibration and lifecycle-verification regime (the world IEC 62304 governs). A signature only *points at* that correctness; reflashing restores *running*, never the correctness. A respirator made to run is one he cannot vouch for, confidently/lethally wrong while reporting fine. Real. [confirmed regime / inferred-sound application]

## Story-mapping (2053, deliberate density)
- **Show:** the DNS-redirect + capture working fast (false hope), then the three walls landing in sequence (pinning, the key, secure boot). The *sequence of walls* is the dread engine.
- **Compress:** the reflash inner loop, authentic nouns, don't tutorialize.
- **Keep off the page:** any successful forge of the controller's yes; any hint a local box could mint the manufacturer's signature (canon wall).
- **Translate to 2053:** present-day names fine as texture/lightly futured; keep the *mechanism* identical (withdrawn cloud, pinned trust, manufacturer-key signature, secure boot).
- **Lena beats carry stakes, not mechanics:** "I can make it stop asking the company; I can't make it tell you the truth."

## Drafting caution (not a canon change)
On a *fully* secure-booted, pinned device the firmware path can be flatly **impossible**, not merely slow, which could over-harden past the beat's need for Eli to get *almost* there. Render the devices as **defeatable-in-principle-but-not-in-time** (a found bootloader weakness exploitable with days, not hours) so the limiter stays **scale + clock + un-forgeable correctness**, per cloud-dependency.md, rather than a clean cryptographic "can't even start." Route any device-hardening spec to continuity if a bible pins it down.

## Sources
- mitmproxy: How it works / Certificates / pinning (docs.mitmproxy.org)
- DNS spoofing/sinkholing with dnsmasq (blog.heckel.io; huntress.com)
- IoT firmware RE; dumping firmware over UART (apriorit.com; cyberark.com; jcjc-dev.com)
- IEC 62304 medical-device software lifecycle (jamasoftware.com)
