# Combining the Revit Sheet and the ACADE Sheet Into the Drawing Set

You have three realistic ways to get the ACADE diagram into the set. Pick by what the delivery requires.

## Decision table

| If the client wants... | Use | Why |
|---|---|---|
| A **Revit-native** set (all sheets in the RVT, matching title block) | **Method A: Link CAD into a Drafting View** (recommended) | Same title block, same sheet index, updates via reload |
| Maximum visual fidelity / non-editable diagram, **PDF output** | **Method C: Merge PDFs** | ACADE plots exactly what it looks like |
| One-off, no future changes | **Method B: Import CAD** | Simple but doesn't update |

## Method A - Link CAD into a Revit Drafting View (recommended)

1. In Revit: `View > Create > Drafting View`. Name it `E-201 Power Diagram`; set **Scale = 1:1** (full size, so DWG scale is preserved) or whatever you drew it for.
2. In the drafting view: `Insert > Link CAD`.
   - **Files of type:** DWG.
   - **Colors:** Black and White (or Preserve if the set uses colors).
   - **Layers/Levels:** All.
   - **Import units:** Auto-Detect (check result; set Inch/Foot manually if it looks 12x off).
   - **Positioning:** Auto - Center to Center (or Origin to Origin).
   - Leave **Current view only** ticked.
3. Check results: scale a known dimension; text should look the same size as in the set. If text is the wrong size, fix in ACADE (not in Revit) and reload.
4. Control layers: `VG > Imported Categories` tab. Turn off junk layers, set line weights by layer.
5. **Create a sheet** (`E-201`), place the drafting view on it. Because the drafting view is 1:1, the diagram appears at the size you drew it. If it's too big/small, change the **view scale** in Properties and the DWG scales together; text size then changes proportionally, so plan for this.
6. **Updates:** when the DWG changes, `Manage > Manage Links > CAD Formats > Reload`.
7. Gotchas:
   - Don't "Explode" the link unless you must (it bloats the model with thousands of elements).
   - The DWG's file path needs to be stable (relative paths help). Put it in a `Linked_CAD` folder.
   - Revit drops proxy/ACADE-specific objects; confirm all visible content appears.

## Method B - Import CAD (one-time)

Same as above but `Insert > Import CAD`. It's embedded, with no updates. Use only for a frozen final.

## Method C - Place as PDF or Image

1. In ACADE, plot to PDF at the final sheet size.
2. In Revit: `Insert > PDF` (current versions, 2022+) or `Insert > Image` (raster) in a drafting view / on the sheet. PDF placement is vector but not editable.
3. Good for quick reference or when the diagram must be exactly as the engineer signed.

## Method D - Merge at PDF level (when delivering a PDF set)

1. In Revit: `File > Export > PDF` (or Print > Adobe PDF) selecting your new Revit sheet(s) and the other sheets.
2. In ACADE: plot the diagram sheet with the Revit title block **or** place the diagram inside a matching border.
3. Merge/reorder with Adobe Acrobat (Organize Pages) or similar. Add bookmarks and ensure the sheet index matches page order.
4. Keep file naming the same as the set (e.g. `ProjectX_E-101.pdf`).

## Matching the title block (important)

| Situation | Do this |
|---|---|
| Diagram is placed on a Revit sheet | Use Revit's title block. Strip ACADE's border before linking. |
| Diagram is plotted from ACADE as a stand-alone sheet | Make the ACADE title block mimic the Revit one (same layout, fonts, fields); ask for the DWG version of the Revit title block, or export one: `File > Export > CAD Formats > DWG` of a blank sheet. |

## Matching other set elements

- **Sheet numbers/names:** use the same pattern; update the **Sheet List** and **cover sheet index**.
- **Revisions:** add the revision to both sheets (Revit revision schedule; ACADE title block revision block or text).
- **Cross-references:** sheet A calls out "SEE E-201"; sheet B calls out "SEE E-101". Use consistent device IDs (e.g. `DS-1`, `JB-1`).
- **Plot style:** monochrome, same line weights.
- **North arrow, scale bar, and sheet notes** per set standard.

## Single sheet vs. two sheets

You said two sheets. A recommended split:

| Sheet | Title | Content |
|---|---|---|
| `E-101` | CONDUIT ROUTE PLAN | Revit view of structure, route, tags, notes |
| `E-201` | POWER DIAGRAM | ACADE diagram via drafting view, with schedules/notes |

If the diagram is small, you can instead put both on one sheet; ask the reviewer.

## Final assembly checklist

- [ ] Both sheets exist in the Sheets list with correct numbers/names
- [ ] Sheet Index and cover sheet updated
- [ ] Title block fields complete (date, drawn/checked, revision)
- [ ] ACADE DWG linked (Method A) and loaded without errors (`Manage > Manage Links`)
- [ ] Printed/PDF'd output checked at 100% for legibility
- [ ] Both sheets refer to each other and to relevant structural sheets
