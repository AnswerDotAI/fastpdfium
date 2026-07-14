"""Read, search, preview, and edit PDFs with fastpdfium (an ergonomic, Apache-licensed layer over pypdfium2/PDFium). Use this when a task needs PDF contents: text extraction first, rendered previews when layout, tables, stamps, signatures, or scan quality matter.

Core idioms (`from fastpdfium.core import *` provides `pdfium` and patches these onto pypdfium2 objects):

- `pdf = pdfium.PdfDocument(path_or_bytes)`; `len(pdf)` pages; `pdf[0]` is a `PdfPage` that knows its `number`.
- `pdf.text(pages=None)` -- plain text with `--- page N ---` markers. Start here: it answers most questions without spending image tokens.
- `pdf.search(q)` / `pg.search(q)` -- a list of `Match`es. Search is content-based: `m.text` is the matched text, `m.ctx(chars=40)` returns it marked with `**` inside its surrounding text (an LLM-ready snippet), and the list repr shows one context line per hit. Options: `match_case`, `match_whole_word`, `consecutive`.
- `pg.preview()` / `pg.preview(q)` / `pg.preview(q, crop=True)` -- render to a PIL image, with `q`'s matches outlined in red; `crop=True` cuts to just the matched region plus `margin` points of context. Default `dpi=150`; lower for thumbnails, higher for fine print. End the cell with the bare call to display.
- A bare `pg` expression displays the page (via `_repr_png_`).

Editing and authoring (positions in points from the page's top-left, like a rendered image):

- `pdfium.PdfDocument.new()` and `pdf.new_page()` (A4 default) start a document from nothing.
- `pg.insert_text(text, x, y, size=12, font='Helvetica')` -- newlines start new lines.
- `pg.draw_rect(x0, y0, x1, y1, stroke=(255,0,0,255), fill=None, width=1)` -- RGBA 0-255.
- `pg.insert_image(img, x, y, w=None, h=None)` -- a PIL image or path; stored as JPEG.
- `pdf.tobytes()` serializes; `pdf.save(path_or_buffer)` writes. Page shuffling comes with pypdfium2: `del pdf[i]`, `pdf.import_pages(other, [0, 2])`.

Prefer `preview(q, crop=True)` crops over whole-page renders: cheaper and easier to read. For scanned/image-only PDFs `text()` returns little -- go straight to previews. PDFium has no redaction or HTML layout; for those, use a different tool.
"""
from fastpdfium.core import *
