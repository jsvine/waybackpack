from .session import Session

SEARCH_URL = "https://web.archive.org/cdx/search/cdx"

def search(url,
    from_date=None,
    to_date=None,
    uniques_only=False,
    collapse=None,
    session=None):

    session = session or Session()
    cdx = session.get(SEARCH_URL, params={
        "url": url,
        "from": from_date,
        "to": to_date,
        "showDupeCount": "true",
        "output": "json",
        "collapse": collapse
    }).json()
    if len(cdx) < 2: return []
    fields = cdx[0]
    snapshots = [ dict(zip(fields, row)) for row in cdx[1:] ]
    if uniques_only:
        return [ s for s in snapshots if int(s["dupecount"]) == 0 ]
    else:
        return snapshots
