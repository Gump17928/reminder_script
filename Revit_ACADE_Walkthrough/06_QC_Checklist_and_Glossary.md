# QC Checklist, Troubleshooting, and Glossary

## Pre-issue QC checklist

### Set consistency
- [ ] Sheet numbers/names follow the existing set pattern
- [ ] Same title block family, size, and fields as the rest of the set
- [ ] Sheet Index / cover sheet list updated
- [ ] Revision / issue date correct; clouds and delta tags applied if required
- [ ] Scale matches the set's convention; scale shown on sheet
- [ ] North arrow/orientation consistent with the structure's other plan sheets
- [ ] Fonts, text heights, line weights, and line styles match

### Revit sheet (route plan)
- [ ] Built from a **duplicated** view, not an issued one
- [ ] Structure shown halftone/light; electrical route is clearly dominant
- [ ] Route starts at the building source and ends at the load; both are labeled
- [ ] Conduit/tray tagged (size/type); junction/pull boxes and disconnects shown
- [ ] Heights/elevations and key dimensions shown
- [ ] General notes + legend + abbreviations present
- [ ] Reference callouts to the diagram sheet (use View Reference)
- [ ] No Revit warnings caused by your elements

### ACADE sheet (diagram)
- [ ] Drawn from the master ACADE project (opened via `.wdp`)
- [ ] Tags/IDs match the Revit sheet
- [ ] Wire/cable schedule or labels complete (conductors, ground, conduit)
- [ ] Source and load ratings noted (voltage, phase, breaker, FLA, AIC)
- [ ] Clean DWG exported for Revit (units, layers, purge, no stray border)
- [ ] Text prints at the right size at final scale

### Engineering
- [ ] See `05_Outdoor_Electrical_Design_Considerations.md` sanity check
- [ ] Engineer review done; stamp as required

### Delivery
- [ ] PDF exported and visually checked page by page at 100%
- [ ] Native files saved/synced and backed up
- [ ] Change log / transmittal prepared
- [ ] Assumptions and open items listed in the email to the reviewer

## Troubleshooting quick table

| Symptom | Likely cause | Fix |
|---|---|---|
| Can't find Conduit tool | Revit LT / Architecture-only license / structure-only template | Verify license; use detail lines; or open an MEP template |
| Conduit invisible in a view | VG, View Range, or Discipline filter | Check VG, Properties > View Range |
| New sheet won't take number | Duplicate number | Choose unused number |
| DWG link is huge/tiny | Units mismatch | Re-link with explicit units, or fix `INSUNITS` in DWG |
| DWG link shows nothing | Layers frozen/off, objects far from origin | Thaw layers, `ZOOM E`, move near origin |
| Text unreadable on sheet | Text height set for wrong scale | Re-set in ACADE for final plot scale; reload |
| Link doesn't update | Reload not done / path changed | `Manage Links > CAD Formats > Reload` / `Reload From` |
| Two title blocks | ACADE border left in DWG | Remove border from the Revit-bound copy |
| Model upgrade prompt | Opened older RVT in newer Revit | Save as new file, keep original; don't mix versions in a team |
| Changes not visible to others | Workshared and not synced | `Synchronize Now` |

## Glossary

| Term | Meaning |
|---|---|
| **ACADE** | AutoCAD Electrical |
| **AHJ** | Authority Having Jurisdiction (inspector / permitting body) |
| **BIM** | Building Information Modeling (what Revit does) |
| **CAD link** | A DWG referenced by Revit; can be reloaded |
| **Drafting View** | A Revit 2D view with no model; where you place DWG/linework |
| **Detail Line** | 2D line visible only in the view it was drawn in |
| **FLA / MCA / MOCP** | Full load amps / minimum circuit ampacity / max overcurrent protection |
| **Family** | Revit content (title block, tag, equipment) |
| **LT** | Revit LT: limited version with no MEP/linking |
| **MEP** | Mechanical, Electrical, Plumbing |
| **NEC** | National Electrical Code (NFPA 70) |
| **One-line** | Simplified single-line diagram of an electrical system |
| **Sheet** | A drawing page in Revit with a title block |
| **View Template** | Saved view settings to reuse |
| **VG / VV** | Visibility/Graphics Overrides dialog (shortcut `VG` or `VV`) |
| **WDP** | ACADE project file |
| **Workset** | Partition of a shared Revit model for multi-user editing |

## What I would do first if I were you

1. Send the questions in file 01 (especially: Revit version/license, model ownership, sheet numbers, deliverable format, source/load data).
2. Open the model **in a copy**, find an existing sheet to mimic.
3. Do the Revit view + sheet with **detail lines first** (fast, low risk), then upgrade to modeled conduit if required.
4. Clean the ACADE DWG, **link** it to a drafting view, place on `E-201`.
5. Have an engineer review the outdoor design considerations before issuing.
