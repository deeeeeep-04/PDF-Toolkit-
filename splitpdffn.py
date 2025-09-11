from pypdf import PdfReader, PdfWriter

def parse_ranges(ranges, total_pages):
    # Accept None, empty, list of tuples, or string like "1-3,5,7-"
    if ranges in (None, (), [], ''):
        return [(0, total_pages)]

    if isinstance(ranges, str):
        parts = [p.strip() for p in ranges.split(',') if p.strip()]
        norm = []
        for part in parts:
            if '-' in part:
                a, b = part.split('-', 1)
                a = a.strip()
                b = b.strip()
                start = int(a) if a else 1
                end = int(b) if b else total_pages
            else:
                start = int(part)
                end = start
            s0 = max(0, start - 1)           # inclusive 1-based -> 0-based
            e0 = min(total_pages, end)       # inclusive end -> exclusive
            if s0 >= e0:
                raise ValueError(f"Invalid range segment: {part}")
            norm.append((s0, e0))
        return norm

    # assume iterable of (start, end)
    norm = []
    for pair in ranges:
        if pair is None or len(pair) != 2:
            raise ValueError("Each range must be a (start, end) tuple")
        start, end = pair
        s0 = 0 if start is None else max(0, start - 1 if start > 0 else start)
        e0 = total_pages if end is None else min(total_pages, end if end >= 0 else total_pages + end)
        if s0 >= e0:
            raise ValueError(f"Invalid tuple range: {pair}")
        norm.append((s0, e0))
    return norm

def split_by_range(pdf_path, output_template=None, ranges=None):
    reader = PdfReader(pdf_path)
    n = len(reader.pages)
    spans = parse_ranges(ranges, n)

    if output_template is None:
        output_template = "split_{i}_{start}-{end}.pdf"

    out_paths = []
    for i, (s0, e0) in enumerate(spans, start=1):
        writer = PdfWriter()
        for p in range(s0, e0):
            writer.add_page(reader.pages[p])
        out_path = output_template.format(i=i, start=s0 + 1, end=e0)
        with open(out_path, mode='wb') as fh:
            writer.write(fh)
        out_paths.append(out_path)
    return out_paths
