---
aliases: ["Ritz Theater", "The Ritz Theater", "Ritz Theatre"]
tags: [location, venue, theater, entertainment]
entity_type: LOCATION
confidence: 1.0
first_mentioned: 2025-06-25
last_mentioned: 2025-06-25
mention_count: 2
location_type: "Theater"
city: "[[Scranton]]"
county: "[[Lackawanna County]]"
state: "[[Pennsylvania]]"
search_patterns:
  - "Ritz Theater"
  - "Ritz Theatre"
  - "filming at.*Ritz"
relationships:
  - target: "[[Scranton]]"
    type: "LOCATED_IN"
    confidence: 1.0
  - target: "[[Final Act]]"
    type: "FILMING_LOCATION_FOR"
    confidence: 0.95
sources:
  - url: "http://deadline.com/2025/06/avaryana-rose-hannah-fierman-horror-movie-final-act-1236441042/"
    title: "'Final Act': Paranormal Horror Film"
    date: 2025-06-24
    mentions: 1
---

# Ritz Theater

> **Historic Theater** in **[[Scranton]], [[Pennsylvania]]**

## Quick Facts
- **Type**: Theater/Entertainment Venue
- **City**: [[Scranton]]
- **County**: [[Lackawanna County]]
- **First Mentioned**: [[2025-06-25]]

## Description

Historic theater venue in Scranton that serves as a filming location for movies and entertainment productions.

## Recent Activity

### June 2025
- **[[2025-06-24]]**: Filming location for horror-thriller [[Final Act]]

## Productions

### Current
- [[Final Act]] - Horror-thriller starring [[Hannah Fierman]], [[Douglas Tait]], and [[Avaryana Rose]]

## Connected Entities

### Films Shot Here
```dataview
LIST
FROM "works/movies"
WHERE contains(location, "Ritz Theater") OR contains(string(relationships), "Ritz Theater")
```

### Cast & Crew
```dataview
LIST
FROM "people/entertainment"
WHERE contains(string(relationships), "Ritz Theater") OR contains(location, "Ritz Theater")
```

## Articles Mentioning

```dataview
TABLE file.ctime as "Date", title as "Article", url as "Source"
FROM "articles"
WHERE contains(content, "Ritz Theater") OR contains(content, "Ritz Theatre") OR contains(aliases, this.file.name)
SORT file.ctime DESC
LIMIT 10
```

*Last updated: 2025-06-27*