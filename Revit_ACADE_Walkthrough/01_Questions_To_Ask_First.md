# Questions To Ask Before You Start

Send these to whoever gave you the task (PM / lead engineer / BIM coordinator). Tick them off and write the answers beside each one.

## A. The Revit model and ownership

- [ ] **What Revit version is the model?** (You must open it in the same or a newer version; Revit upgrades files one-way and you can't go back.)
- [ ] **Do I have Revit (full), or only Revit LT?** LT cannot do MEP (conduit, cable tray, electrical systems) and can't link Revit files. You'd draw routes with plain lines.
- [ ] **Is the model a central/workshared model (BIM 360 / Autodesk Docs / network) or a standalone file?** If workshared, you need to "Create Local" and sync, not edit the file directly.
- [ ] **Who owns the model and am I allowed to add sheets/views to it?** Or should I make a separate electrical Revit file that links the structure?
- [ ] **Is there a BIM Execution Plan / CAD standard / template** I must follow?
- [ ] **Is the model complete enough to route against?** (steel/framing, platforms, ladders, equipment pad, building wall where the conduit leaves.) Is it surveyed, and how accurate is it?
- [ ] **Is the structure in the model tied to real coordinates / true north?** (Matters for plan orientation and north arrow.)

## B. The existing drawing set

- [ ] **Which title block, sheet size and scale?** (e.g. ARCH D 24x36, 1/4"=1'-0")
- [ ] **What sheet number should the new sheets take?** (e.g. `E-101`, `E-201`; check the sheet index. Does the set already have an `E` discipline or do we add one?)
- [ ] **Where in the set do they go, and do I update the sheet index / cover sheet list?**
- [ ] **Is there a revision in progress** (Rev A / Rev 1, delta clouds, revision schedule)?
- [ ] **Which existing sheets are a good style reference?** Ask for a PDF of one or two.
- [ ] **Drawing standard:** line weights, fonts, text height, symbols legend (does the set already have one for electrical?).
- [ ] **Deliverable format:** native Revit, PDF set, DWG, or all three?
- [ ] **Which view of the structure do they want?** Plan, elevation, 3D, or section? Is there already a view I should copy?

## C. The electrical scope

- [ ] **Source:** Where does power start? (Which panel/switchgear, breaker/disconnect size, building location.)
- [ ] **Load:** What is the equipment? Voltage, phase, HP/kW/FLA/MCA/MOCP (nameplate or vendor data).
- [ ] **Voltage/system:** e.g. 480Y/277 V 3-ph 4-wire, 208Y/120, 120/240 V 1-ph.
- [ ] **Run length and route:** Is there a preferred route? Any no-go zones (walkways, crane paths, equipment)?
- [ ] **Raceway type:** conduit (RMC/IMC/EMT/PVC/LFMC), cable tray, direct-buried, armored cable? Is there a spec or "standard" the owner uses?
- [ ] **Does the wiring route also go underground / through a wall / across a roof?** (Different details are needed.)
- [ ] **Other wires on the same run?** (Control, instrumentation, grounding, fiber, comms.)
- [ ] **Design criteria:** Voltage drop limit, NEC edition, local amendments, owner standards, AHJ.
- [ ] **Hazardous area classification** (Class/Div/Zone) or corrosive environment (marine, chemical)?
- [ ] **Is calculation/engineering done already, or do I need to size wire/conduit/breakers?** (If you're not the engineer, you draw what the engineer specified.)

## D. The AutoCAD Electrical sheet

- [ ] **Do I have the source `.dwg` / `.wdp` project, or just a PDF?** (A PDF can't be edited properly; get the DWG or redraw.)
- [ ] **What ACADE version, and which standards does the project use?** (JIC / IEC / NFPA? Which symbol library?)
- [ ] **What kind of diagram is it?** One-line, three-line, schematic, wiring, riser, panel layout?
- [ ] **Should it carry the Revit set title block, or the ACADE project's?**
- [ ] **Wire numbering / tag conventions** to follow?
- [ ] **Do the two sheets need to cross-reference each other?** (e.g. "See E-201 for diagram", callouts/keynotes tied to the same IDs.)

## E. Review and issue

- [ ] **Who reviews and stamps?** Is a PE seal required?
- [ ] **What's the deadline and issue purpose?** (Preliminary, for review, for permit, for construction, as-built?)
- [ ] **Who will print/issue it and in what form?**

## "If they don't know" defaults you can propose

| Unknown | Reasonable default to propose in writing |
|---|---|
| Sheet numbers | `E-101` (route plan) and `E-201` (diagram) - get approval |
| Scale | Same as the structure's existing plan sheets |
| Delivery | Native Revit sheet containing a linked DWG; PDF export too |
| Model editing | Separate Revit file linking the structure |
| Route | Shortest accessible route attached to existing steel, flagged "route TBD by field verification" |

Always get these assumptions confirmed by email so they're documented.
