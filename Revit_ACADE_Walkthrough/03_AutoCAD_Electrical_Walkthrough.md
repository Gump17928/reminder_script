# AutoCAD Electrical Walkthrough: The Diagram Sheet

Goal: produce one clean electrical diagram sheet (source in building -> up the structure -> load) that can be placed into the Revit set.

## What ACADE is (and isn't)

AutoCAD Electrical is AutoCAD plus an electrical toolset: **Project Manager**, symbol libraries, wire numbering, component tagging, cross-references, panel layout, and reports (BOM, wire list). It is strongest at **control schematics and panel layouts**. For a **power one-line / riser diagram** it works fine, but you may be just as well served by drawing with standard AutoCAD commands and the ACADE symbols. Use whatever matches the existing electrical drawings the client uses.

## Concepts

| Concept | Meaning |
|---|---|
| **Project (.wdp)** | A list of related drawings. ACADE tracks tags, wires, references across drawings in the project. |
| **Drawing (.dwg)** | One sheet. Belongs to a project. |
| **Project Manager** | Dockable palette listing the project's drawings. Command: `AEPROJECT` (or `Project` tab > Project Manager). |
| **Template (.dwt)** | Starting drawing with layers, title block, and standards. |
| **Ladder / Rungs** | Control schematic structure. Not needed for a one-line. |
| **Wire layers / Component tags** | ACADE assigns layer names and tags automatically; don't rename arbitrarily. |

## Step 0: Do you already have the drawing?

You said you already have an ACADE sheet. Then:

1. Get the **whole project folder** (`.wdp`, `.wd*` support files, all `.dwg`s), not just one DWG.
2. Open Project Manager -> **Open Project** (the `.wdp`). Don't open the DWG alone; ACADE may then treat tags as orphaned.
3. Run **Project > Project Properties** to see standards, drawing format, and wire numbering.
4. If you only have a PDF, the options are: (a) request the DWG, (b) redraw, or (c) treat the PDF as a raster/PDF underlay (`Insert > PDF Underlay`) - acceptable only if the client accepts a non-editable page.

## Step 1: Create or edit the drawing (if building new)

1. **Project tab > New Project** -> name, location, description; choose the same drawing standards/template as the rest of the company's electrical work. Ask for the template file if not provided.
2. **Project Manager > right-click project > New Drawing**. Choose the template (`.dwt`). Name per convention, e.g. `E-201_Power_Diagram.dwg`.
3. Set **Drawing Properties** (right-click the drawing > Properties) with description lines so the title block auto-fills.

## Step 2: Build the diagram

Typical content for a feed from the building to a load on an outdoor structure:

```
 [Building panel / breaker]  -->  [Disconnect / junction]  -->  [Conduit & wire run]  -->  [Load / equipment]
        (source)                 (outdoor, near load)            (size, type, length)        (nameplate data)
```

1. **Insert components** (`Schematic tab > Insert Component` or the Icon Menu) - breakers, disconnects, transformers, motors, junction boxes. Pick the library that matches the set (NFPA/JIC for US).
2. **Draw wires** (`Schematic tab > Insert Wire`) between devices. Use wire layers to distinguish power / control / grounding.
3. **Add wire/cable labels**: conductor count & size, conduit size/type, ground, e.g. `3#8 + 1#10 GND IN 3/4" C`. Use text or ACADE **Wire Number** tools (`Schematic > Wire Numbers`).
4. **Tag** components (`Schematic > Edit Component`, or insert with tag dialog). Use the same IDs as the Revit sheet (e.g., `DS-1`, `JB-1`, `P-101`).
5. **Annotate**: voltage/phase, breaker size, load data (HP/kW/FLA), short-circuit/AIC rating, grounding, "NOTES" block.
6. If needed, add a **panel layout / footprint** (`Panel tab`) for the physical arrangement at the building or load.
7. **Run checks**: `Project > Drawing Properties`, then `Reports` (BOM / Component / Wire From-To) to find untagged items, duplicates, orphaned references.

## Step 3: Prepare the DWG for the Revit set

The Revit side wants a **simple, clean DWG**:

1. **Draw at 1:1** in Model Space; set text and symbol heights so that at the final print scale text is **~1/8" (3 mm)** tall. If the set prints text at 1/8" and you print at 1:1, text height = 0.125" (in drawing units).
2. **Remove or turn off the ACADE title block** if the sheet will sit inside a Revit title block. (Two borders in one sheet looks wrong.) Keep a copy with the border for standalone use.
3. **Layer cleanup**: Purge, audit, and delete unused layers/blocks (`PURGE`, `AUDIT`). Avoid xrefs; or bind them (`XREF > Bind`) because Revit won't follow nested xrefs well.
4. **Units**: set `UNITS` to match Revit (inches or feet, decimal). Revit will read the DWG's `INSUNITS`; mismatches scale the link 12x or 25.4x.
5. **Colors**: fine, Revit can force black & white on import.
6. **Make a separate "Revit copy"**: ACADE drawings are mostly ordinary AutoCAD lines, text and attributed blocks, so they normally link fine. Work on a copy (`SAVEAS` or `WBLOCK` with **Entire drawing**) so the master project stays intact. If something doesn't show in Revit, check for proxy objects (`EXPLODE` them in the copy only).
7. Save the copy with `SAVEAS` as **AutoCAD 2018 DWG**. AutoCAD 2025's default DWG format is that same 2018 format, and Revit 2025 reads it, so the default is fine.
8. **PDF alternative**: `Output tab > Plot` with a PDF device (e.g., *DWG To PDF.pc3*), paper size matching the sheet, plot style matching (monochrome).

## Step 4: Hand-off

Keep the ACADE project as the **master**; the DWG used in Revit is a derived copy/link. Put it in a project folder like:

```
Project\
  Revit\            (RVT, sheets)
  ACADE\            (WDP + DWGs; master)
  Linked_CAD\       (clean DWG for Revit link)
  PDF\              (issue PDFs)
```

## Common ACADE pitfalls

| Problem | Cause / fix |
|---|---|
| Tags show `??` or missing | Opened DWG outside its project; open via `.wdp`. |
| Title block fields blank | Project/drawing properties not filled; or wrong title block attribute names. |
| Symbols wrong standard | Wrong symbol library (JIC vs IEC); set under **Project Properties > Drawing Format / Standards**. |
| Drawing is huge in Revit | Units mismatch or text height set for 1:1 vs scale; check `INSUNITS`, `DIMSCALE`, `LTSCALE`. |
| Revit link shows nothing | Layers off/frozen in DWG; or entities on a non-plottable layer; or far from origin. |
| Can't use 3-line | Choose symbols in the library for single/three-line; otherwise draw with AutoCAD and block it. |
