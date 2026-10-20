# Start Here: Adding 2 Electrical Sheets to an Existing Revit Drawing Set

## First, a vocabulary fix (it will save you confusion)

There is no product called "AutoCAD Revit". These are **two separate programs**:

| Program | What it is | Role in your task |
|---|---|---|
| **Revit** | 3D "BIM" model + the drawing set (sheets) generated from it | Holds the structure model and the **existing drawing set**. You add a sheet here and show the wiring route on a view of the structure. |
| **AutoCAD Electrical** (ACADE) | AutoCAD with electrical schematic/panel tools, project manager, wire numbering, reports | Produces the **electrical diagram sheet** (source in the building -> up the structure -> load/equipment). |

They do **not** talk to each other automatically. You bring ACADE output into the Revit sheet set by one of the methods in `04_Combining_Into_The_Set.md`.

## Your setup: Revit 2025 + AutoCAD Electrical 2025

Good news: the versions are matched, and the DWG hand-off works cleanly (both use the 2018 DWG format).

**Check these on day one:**

1. **Full Revit or LT?** Look at the Revit title bar / `File > Help > About`. "Revit LT 2025" has no conduit/cable tray and cannot link Revit models; "Autodesk Revit 2025" does. This decides whether you model conduit or use detail lines.
2. **Version of the model file.** Revit 2025 opens files from 2025 and earlier (and upgrades them on save, one-way). It **cannot open a model saved in 2026 or newer**. Check `File > Open > Project` (the file's version shows in the open dialog) before you start. If the model comes from someone on an older version, always work on a copy: once upgraded, they can't open your copy.
3. **MEP content present?** In Revit 2025 the **Systems** tab holds Conduit, Cable Tray and Electrical Equipment. If those tools are greyed out, you started from an architecture/structure template. Create a new project from the *Electrical* or *Systems* template and link the structure in, or ask for the firm's electrical template.
4. **Required Revit 2025 features I rely on:** `Insert > Link CAD`, `Insert > PDF`, `File > Export > PDF`, View References, and the `VG` shortcut. All are present.
5. **ACADE 2025:** open projects through Project Manager (`AEPROJECT`). If the project was made in an older ACADE, it prompts to upgrade drawings. Do that on a copy.

## The two deliverables

1. **Sheet A (Revit):** A new sheet in the existing set showing a view of the structure (plan / elevation / 3D) with the **new wiring route** drawn on it.
2. **Sheet B (ACADE):** A sheet showing the electrical connection from the building source to the load/equipment (one-line, riser, or wiring diagram).

## Recommended approach (my opinion)

**Do the Revit sheet natively in Revit. Do the electrical diagram in ACADE. Merge them by placing the ACADE DWG onto a Revit sheet via a Drafting View.** Reasons:

- The existing set is Revit-based, so title block, sheet numbering, sheet index, revisions and print settings all stay consistent when both sheets are *real Revit sheets*.
- Linking the DWG (not importing) means that if the diagram changes in ACADE you reload the link and the sheet updates.
- Fallback if the client only wants a PDF set: plot both to PDF with matching title blocks and merge. (See file 04.)

**Don't modify the structural model more than needed.** Best practice is to keep electrical work in its own Revit file linked to the structure (or in its own workset if you must be in the same file), and only show the structure as a background on your view. Ask who owns the model (file 01).

## Suggested order of work

```
1. Ask the questions in 01  (30 min, prevents days of rework)
2. Get/confirm the software + files + standards (01, 06)
3. Revit: duplicate a view, create the new sheet, match the set (02)
4. Revit: draw the wiring route (conduit / cable tray / lines) + tag + notes (02)
5. ACADE: create project + drawing from the right template and build the diagram (03)
6. Bring the ACADE drawing onto a Revit sheet (04)
7. Engineering sanity checks for an outdoor run (05)
8. QC checklist, then issue (06)
```

## Files in this folder

| File | Purpose |
|---|---|
| `00_START_HERE_Overview.md` | This file |
| `01_Questions_To_Ask_First.md` | The questions you said you didn't know to ask |
| `02_Revit_Walkthrough.md` | Step-by-step: view, sheet, wiring route, annotation |
| `03_AutoCAD_Electrical_Walkthrough.md` | Step-by-step: project, drawing, diagram |
| `04_Combining_Into_The_Set.md` | Getting the ACADE sheet into the Revit set (and PDF fallback) |
| `05_Outdoor_Electrical_Design_Considerations.md` | Technical items to check for an outdoor structure run |
| `06_QC_Checklist_and_Glossary.md` | Pre-issue checklist, glossary, troubleshooting |

## Is it "pretty easy"?

Mechanically, yes: a sheet is a few clicks and a wiring route can be a handful of lines. The real effort is **matching the existing set's standards** and **getting the engineering right**, and neither is visible until you ask the right questions. Menu names below are based on current Revit / AutoCAD Electrical versions; they shift slightly between releases (2022-2025+), so use the ribbon search (Revit) or the `Ctrl+F`-style command search if a name differs.

> Note: this is a drafting/engineering-workflow guide, not a code-compliance sign-off. Final design and stamping belong to a licensed engineer / authority having jurisdiction.
