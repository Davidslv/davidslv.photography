# davidslv.photography

David Silva's photography site. One page for now: *From last light to last train* (proposal F, locked 10 Oct 2026).

## Build

Needs the NAS mounted (`/Volumes/David Photography`) for the full-resolution photos.

    tools/run.sh          # export images (AVIF + JPEG, 640/1200/2400 px), embed copyright, write site/
    tools/run.sh --html   # rewrite the HTML only

Then commit `site/` and push to `main`. GitHub Actions checks every referenced image exists and deploys `site/` to Pages.

## What's in site/

- `index.html`: static HTML. JSON-LD has Person, WebSite, CollectionPage and an ImageGallery of ImageObjects with creator, credit and copyright.
- `img/`: AVIF with JPEG fallback. JPEGs carry IPTC/XMP creator, credit and copyright.
- `fonts/`: Newsreader and Public Sans (latin, self-hosted, SIL Open Font License).
- `sitemap.xml` with image entries, `robots.txt`, `CNAME`, icons, `og.jpg`, `404.html`.

## Adding a story

Edit `SRC` and `SEQUENCE` in `tools/build.py`. Rules: real order, real times, 10 to 12 photos per part, a person in most frames, full-resolution sources only.

Photographs © David Silva. All rights reserved. Code: the build script may be reused, the photographs may not.
