# Outdoor Electrical Design Considerations (for a wiring run up a structure)

> This is a checklist of topics to raise with the responsible engineer. It is **not** a design or code-compliance determination. Confirm against the adopted NEC edition (or applicable local code / IEC), owner standards, and the AHJ. Section numbers below refer to the US NEC (NFPA 70) and may differ by edition.

## 1. Basis of design (get these numbers first)

- Voltage, phase, frequency, grounding system
- Load: FLA / MCA / MOCP from the nameplate; continuous vs. non-continuous
- Available fault current at source and equipment SCCR/AIC ratings
- Run length (route length including vertical rise) -> **voltage drop** (common targets 3% branch / 5% total; confirm owner standard)
- Ambient temperature and sun exposure (rooftop/outdoor raceway can run hot -> **ampacity derating** and conductor temp ratings)
- Number of current-carrying conductors in the raceway (derating)

## 2. Raceway and wire selection

| Topic | Consider |
|---|---|
| Raceway type | RMC / IMC (steel, durable), EMT (outdoor allowed w/ proper fittings in many cases, not for severe physical damage), PVC (needs expansion, supports, UV rating, physical damage rules), LFMC (flexible connection to equipment) |
| Corrosion | Galvanized vs. PVC-coated vs. stainless; coastal/chemical environments |
| Wet location | Wire must be rated for wet locations (e.g. THWN-2), raceway fittings listed for wet (rain-tight, compression) |
| Physical damage | Lower portion of runs near ground/vehicle traffic may need heavier raceway |
| Cable tray | If used outdoors, rated for the environment; cable types allowed in tray (e.g. TC-ER) |
| Sizing | Conduit fill (NEC Ch. 9 tables), pull box sizing, bend limits (max 360 degrees between pull points) |
| Grounding | Equipment grounding conductor sized to OCPD; bonding of metallic raceways, structural steel bonding if specified |

## 3. Routing and mounting on the structure

- **Structural attachment:** Who approves attaching to the structure? Clamps, unistrut, beam clamps (avoid drilling/welding structural members without engineering approval).
- **Support spacing** per code and raceway type.
- **Expansion/deflection fittings** for PVC and long runs, and where the run crosses structural expansion joints or dissimilar structures.
- **Wind/vibration/seismic** loads on the raceway and supports.
- **Clearance from hazards:** hot piping, moving equipment, walkways, crane paths, maintenance access, ladders/cages, fall-arrest points.
- **Working space and accessibility** of disconnects, pull boxes, junction boxes.
- **Height/elevation:** exposed runs near personnel; elevated runs are usually safer from damage, but need access.
- **Vertical runs:** support the weight of conductors in long vertical raceways (cable supports per NEC 300.19).
- **Drainage:** avoid trapping water; use drains/breather fittings where condensation is likely.

## 4. Building-side and equipment-side details

- **Source:** breaker size and available space; labeling; lockout provisions.
- **Disconnect:** within sight of equipment? (NEC 430.102 for motors, 440 for HVAC; local rules vary) Location, NEMA rating (e.g. 3R, 4, 4X).
- **Wall/penetrations:** firestopping and weather sealing through the building envelope; sleeves, sealing fittings, drip loops.
- **Underground portions:** burial depth (NEC Table 300.5), warning tape, trench details, conduit type.
- **Equipment termination:** conductor termination temperature rating, lug size, conduit hub type.
- **Labeling:** arc-flash label (when required), equipment ID tags matching drawings.

## 5. Lightning, grounding and surge

- Lightning protection if the structure is tall or isolated.
- Grounding electrode system connection / ground ring. Equipotential bonding between the structure and equipment.
- Surge protection on feeders/instruments if specified.

## 6. Drawing-quality considerations that affect the engineering

- State the route is **diagrammatic** vs. **to scale**; call out "field verify".
- Show **conduit size, type, conductor schedule** on the diagram.
- Show **pull/junction boxes** with locations and sizes.
- Show **elevations** (heights) and **dimensions** of key points.
- Include a **legend**, **abbreviations**, and **general notes** (code references, specification sections).
- Call out **existing vs. new** work using line style or a prefix (e.g. (E), (N)).
- Record **assumptions** on the sheet if info is missing (e.g. "Voltage drop to be verified by engineer").

## 7. Information you may still need from others

| From | Need |
|---|---|
| Structural engineer | OK to attach to steel; allowable loads; no-attachment zones |
| Equipment vendor | Nameplate data, termination details, enclosure rating |
| Owner / facility | Standards, outage constraints, existing conduit/trench maps |
| AHJ / inspector | Permit requirements, stamped drawings, special inspections |
| Safety | Lockout/tagout, work-at-height restrictions, hot work |

## Quick sanity check before issue

- [ ] Wire and conduit sized by an engineer or by documented calc
- [ ] Voltage drop checked for the full route length
- [ ] Wet/outdoor-rated products specified
- [ ] Support/attachment method accepted by structural
- [ ] Disconnect and grounding shown
- [ ] Sheets stamped / reviewed as required
