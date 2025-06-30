---
aliases: ["Hannah Fierman"]
tags: [person, entertainment, actress, horror]
entity_type: PERSON
confidence: 1.0
first_mentioned: 2025-06-24
last_mentioned: 2025-06-25
mention_count: 3
official_title: "Actress"
bio: "Actress known for horror films, particularly V/H/S"
search_patterns:
  - "Hannah Fierman"
relationships:
  - target: "[[V/H/S]]"
    type: "APPEARED_IN"
    confidence: 0.95
  - target: "[[Final Act]]"
    type: "STARS_IN"
    confidence: 0.95
sources:
  - url: "http://deadline.com/2025/06/avaryana-rose-hannah-fierman-horror-movie-final-act-1236441042/"
    title: "'Final Act': Paranormal Horror Film"
    date: 2025-06-24
    mentions: 3
---

# Hannah Fierman

> **Actress** | **Horror Film Specialist**

## Quick Facts
- **Full Name**: Hannah Fierman
- **Profession**: Actress
- **Known For**: Horror films, particularly [[V/H/S]]
- **Current Project**: [[Final Act]]
- **First Mentioned**: [[2025-06-24]]

## Filmography

### Known Works
- [[V/H/S]] - Horror anthology film
- [[Final Act]] - Current horror-thriller project (2025)

## Current Projects

### June 2025
- **[[2025-06-24]]**: Filming [[Final Act]] at [[Ritz Theater]] in [[Scranton]]

## Co-Stars

### Final Act Cast
- [[Avaryana Rose]]
- [[Douglas Tait]]
- [[Vincent M. Ward]]

## Related Works

```dataview
LIST
FROM "works"
WHERE contains(string(relationships), "Hannah Fierman")
```

## Articles Mentioning

```dataview
TABLE file.ctime as "Date", title as "Article", url as "Source"
FROM "articles"
WHERE contains(content, "Hannah Fierman") OR contains(aliases, this.file.name)
SORT file.ctime DESC
LIMIT 10
```

*Last updated: 2025-06-27*