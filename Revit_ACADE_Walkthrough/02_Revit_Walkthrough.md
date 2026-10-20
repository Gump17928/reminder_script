# Revit Walkthrough: New Sheet + Wiring Route

Goal: add **one new sheet** to the existing set, containing a view of the outdoor structure with the new electrical route drawn on it.

## Revit concepts you need (5 minutes)

| Concept | Plain meaning |
|---|---|
| **Project Browser** | The tree on the left: Views, Sheets, Schedules, Families, Links. Everything lives here. |
| **View** | A "camera" on the model (plan, elevation, section, 3D). Sheets don't contain model geometry; they contain *views* placed on them. |
| **Sheet** | A drawing page with a title block. You drag views onto it. |
| **View Template** | Saved view settings (scale, visible categories, line weights). Apply the same one used in the set. |
| **Family / Type** | Content: title blocks, conduit fittings, tags, equipment. |
| **Link** | A separate Revit file displayed in your project (e.g. structure linked into an electrical file). |
| **Workset** | Layer-like partition of a shared model for multi-user editing. |
| **Detail lines / Model lines** | 2D annotation lines (view-specific) vs 3D lines (appear in all views). |

## Step 0: Open the model safely

1. Make a backup copy of the file first (or work in a copy until told otherwise).
2. If it is **workshared**: `File > Open`, tick **Create New Local**, open, and **Synchronize with Central** only when you want to publish. Never edit the central file directly.
3. Open with **Audit** only if instructed. If prompted about missing links / fonts, note them but don't dismiss without recording what was missing.
4. Check Revit version (`File > Open` warns on upgrade). Confirm **Manage > Project Information** and **Manage > Project Units** so units match the set.

## Step 1: Study the existing set before touching anything

1. In Project Browser, expand **Sheets (all)**. Note numbering pattern, naming, and which title block each uses.
2. Open one existing sheet that is a good analog (same discipline/size). Click a placed view, look at **Properties**: *View Template*, *Scale*, *Detail Level*, *Discipline*, *Phase*. Copy these.
3. Note how the sheet's title block fields are filled (project name, drawn by, date, sheet number, revision).
4. Look for an existing **Sheet List** schedule (Project Browser > Schedules). New sheets appear in it automatically.

## Step 2: Create the view for your sheet

Never edit a view that is already placed on an issued sheet. Duplicate it.

1. In Project Browser, find the plan/elevation/3D that best shows the structure.
2. Right-click the view > **Duplicate View**:
   - **Duplicate** - geometry only, no annotations.
   - **Duplicate with Detailing** - copies existing annotations too (usually what you want for a base).
   - **Duplicate as Dependent** - stays tied to parent's crop/scale; useful for enlarged areas, but changes to the parent propagate.
   - For routing you typically choose **Duplicate with Detailing**.
3. Rename it clearly, e.g. `ELECTRICAL - Conduit Route - Plan`. (Right-click > **Rename** or select and press **F2**.)
4. In **Properties** of the new view:
   - **View Template**: set the electrical template if one exists; otherwise match the structural one.
   - **Scale**: set to what you'll print (and what the set uses).
   - **Discipline**: Electrical (or Coordination).
   - **Crop Region / Scope Box**: turn **Crop View** and **Show Crop Region** on and crop to just the area of interest.
5. Use **Visibility/Graphics (VV or VG)** to dial back clutter: turn off irrelevant categories (furniture, rooms, tags, etc.), set structure to **halftone** so your electrical route stands out.

> If the structure is a **linked** Revit model in your file: VG > **Revit Links** tab > Display Settings > "By Linked View" or "Custom", and turn on only needed categories.

For a 3D view: View tab > **3D View > Default 3D View**, then duplicate and use **Section Box** (Properties > Extents) to isolate the structure.

## Step 3: Draw the wiring route

Pick the approach based on what the client expects. Order is easiest to hardest.

### Option 1 - 2D "route lines" (diagrammatic route)
Use for a conceptual or preliminary drawing, or if you have Revit LT.
- **Annotate > Detail Line** (view-only) on a dedicated line style, e.g. thick dashed "Electrical Route".
- Add **Text** and **Tags** with `Annotate > Text` and `Tag`.
- Pros: fast, no MEP content needed. Cons: not coordinated, not scheduled, doesn't show up in other views.

### Option 2 - Modeled conduit / cable tray (full Revit MEP)
Use for coordinated work or when quantities (lengths, fitting counts) matter. Requires full Revit with the Systems tab.
1. **Systems > Conduit** (or **Cable Tray**). Shortcut: `CN` for conduit.
2. In the Type Selector (Properties), pick the type: *Conduit with Fittings* vs *Conduit without Fittings*. Match the spec (RMC, EMT, PVC, etc.). If you don't see types, you need the electrical template or to load them via **Manage > MEP Settings > Electrical Settings > Conduit Settings**.
3. In the Modify | Place Conduit tab set **Diameter** (trade size) and **Middle Elevation** (height off the level). Check **Offset** relative to the level.
4. Click start and end points. Use **Change Elevation** or **Apply** for vertical runs up the structure. Use **Modify > Join** / drag grips to connect elbows.
5. For exposed runs on steel, route along columns/beams with an offset so you do not collide with the structural elements (use **Interference Check**, `Collaborate > Interference Check`).
6. Place **Conduit Fittings** (`Systems > Conduit Fitting`) for pull boxes/junctions/condulets and **Electrical Equipment/Devices** for disconnects, junction boxes, the load.

### Option 3 - Hybrid
Model the primary conduit or tray, and use detail lines + notes where the route is indicative only. This is the most common approach for an "add this to an existing set" job.

## Step 4: Annotate so a contractor can read it

1. **Tags**: `Annotate > Tag by Category` (conduit tag shows size/type; use a Conduit Tag family, load via `Insert > Load Family`).
2. **Keynotes or notes**: `Annotate > Text` (or Keynote Legend if the set uses keynotes). Typical notes:
   - "Conduit and wire per specification Section ___."
   - "Field verify all routing prior to installation."
   - "Provide expansion fittings at ___."
   - "Route shown is diagrammatic."
3. **Dimensions**: `Annotate > Aligned` to dimension from structure gridlines to the route; show heights as elevation callouts (`Annotate > Spot Elevation`).
4. **Callouts to the diagram**: text like "REFER TO E-201 FOR ELECTRICAL DIAGRAM". Better: **View Reference** (`Annotate > View Reference`) which auto-updates with sheet number.
5. **Legend** (`View > Legend`): symbol/line-style legend for your route lines, equipment symbols, abbreviations.
6. **Revision clouds**: if the set is under revision, `Annotate > Revision Cloud` then assign to the active revision (`View > Sheet Issues/Revisions`).

## Step 5: Create the sheet

1. `View > Sheet Composition > Sheet` (or right-click **Sheets** in browser > **New Sheet**).
2. In the dialog choose the **same title block** as the existing set (e.g., `E1 30x42 Horizontal`). If missing, click **Load** and find it in the Revit library or ask for the family (`.rfa`).
3. Fill in **Properties** for the sheet:
   - **Sheet Number** (e.g. `E-101`), **Sheet Name** (e.g. `ELECTRICAL CONDUIT ROUTE - PLAN`).
   - **Drawn By**, **Checked By**, **Approved By**, **Sheet Issue Date**, and any custom parameters matching the other sheets.
   - **Appears In Sheet List**: on.
4. Drag the view from the Project Browser onto the sheet. Check its **scale** and **viewport type** (Properties > Viewport type) so the viewport title looks like the others.
5. Add a **Legend** and any **schedules** (conduit schedule, panel schedule) by dragging them on as well.
6. Reserve a space for the ACADE diagram if both items will live on the same sheet (see file 04) or create a second sheet (`E-201`).

## Step 6: Quality check inside Revit

- Set **Detail Level** to Fine for conduit and verify linework looks like the set at print scale.
- Zoom the sheet 1:1 and check text overlaps. Use `Manage > Inquiry > Warnings` and fix warnings you created.
- Verify visible conduit lengths with a **Conduit Schedule** (`View > Schedules > Schedule/Quantities`, category *Conduits*, fields: Type, Size, Length, Comments).
- `View > Sheet Composition > Sheet Index` (or the set's existing sheet list) should now contain both new sheets.
- Print Preview: `File > Print > Print Preview`, or export **PDF** (`File > Export > PDF`) and inspect.

## Step 7: Save and share

- **Standalone:** `Save As` with a new revision name if you aren't told otherwise.
- **Workshared:** `Collaborate > Synchronize Now`, with comment, relinquish worksets.
- Keep a short change log: what sheets/views you added and why.

## Common Revit pitfalls

| Problem | Cause / fix |
|---|---|
| "I can't see my conduit" | View range, discipline, or VG filter hides Conduits category; check `VG > Model Categories > Conduits` and view's **View Range** (Properties). |
| Structure looks too heavy | Set structure categories to Halftone in VG; or use a view template. |
| Sheet number refused | Duplicate numbers aren't allowed; pick unused one. |
| Scale looks wrong | View scale (Properties) vs. viewport; one view = one scale. Don't resize a view with the sheet. |
| Lines appear in all views | You used **Model Line** instead of **Detail Line**. |
| Title block fields blank | Fill the sheet's **Properties**, not the title block directly; some are project info (`Manage > Project Information`). |
| Can't edit an element | Owned by another user (workshared): request via **Editing Requests**. |
