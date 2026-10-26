# Show HN 文案（Hacker News）

**Title**: Show HN: chinese-history – Open structured database of Chinese history (266 emperors, 154 events, CC0 artifacts)

**Text**:

I spent a few evenings building what [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) (53k★, the de-facto open database of classical Chinese poetry) did for poetry — but for history, which is much harder due to disputed dates, era-name calendars, and provenance.

**What's in it (v1.4.0, all verifiable)**:

- 370 historical figures: every emperor from Qin Shi Huang (221 BC) to Puyi's abdication (1912) — including Sixteen Kingdoms, Ten Kingdoms, Western Xia, Dali — plus 82 ministers/generals/poets
- 154 major events with citations to primary sources (Records of the Grand Historian, Book of Han, etc., with volume references)
- 551 era-name → Gregorian mappings (the reign-era calendar table)
- 62 artifacts from the Met, Smithsonian NMAA, Cleveland, British Museum — CC0 images directly usable, NC-licensed ones link-only
- 94% of figures linked to Wikidata QIDs

**Design decisions that differ from the poetry repo** (learned from its 10 years of pain):

- Sources are mandatory — CI rejects records without citations
- Disputed facts stored as multiple values, each with its own source (never voted away)
- Dual-track time: original Chinese era notation + normalized Gregorian (negative = BC)
- Zero-dependency validator: `python3 tools/validate.py`
- Tag-triggered CI builds a single-file SQLite DB + JSON snapshot into GitHub Releases

Data is JSON-sharded (≤1000 records/file, filename = index), so PRs are the collaboration model.

Honest caveat: records are AI-pipeline generated with partial spot-checking; none has been individually human-verified yet. `_meta` logs the model and prompt version (traceability, not a correctness guarantee). Check `sources` before citing.

Known gap: `disputed[]` competing-value markup exists in the schema but currently covers only 9 of 370 figures.

Repo: https://github.com/anthonyhann/chinese-history
