---
aliases: []
tags: [work, {{work_category}}]
entity_type: WORK
confidence: 0.85
first_mentioned: 2025-06-27
last_mentioned: 2025-06-27
mention_count: 1
work_type: "{{work_type}}"
genre: "{{genre}}"
year: {{year}}
status: "{{status}}"
location: "[[{{filming_location}}]]"
relationships:
  - target: "[[]]"
    type: ""
    confidence: 0.5
sources:
  - url: ""
    title: ""
    date: 2025-06-27
    mentions: 1
---

# Final Act

> **{{work_type}}** | **{{genre}}** | **{{year}}**

## Quick Facts
- **Type**: {{work_type}}
- **Genre**: {{genre}}
- **Year**: {{year}}
- **Status**: {{status}}
- **Location**: [[{{filming_location}}]]
- **First Mentioned**: [[2025-06-27]]

## Description

{{work_description}}

## Cast & Crew

### Actors
```dataview
LIST
FROM "people"
WHERE contains(string(relationships), "Final Act") AND contains(string(relationships), "STARS_IN|APPEARS_IN|ACTS_IN")
```

### Production Team
```dataview
LIST
FROM "people"
WHERE contains(string(relationships), "Final Act") AND contains(string(relationships), "DIRECTED|PRODUCED|CREATED")
```

## Production Details

### June 2025
- **[[2025-06-27]]**: First mentioned in news article

## Related Works

```dataview
LIST
FROM "works"
WHERE contains(string(relationships), "Final Act") OR contains(genre, this.genre)
```

## Articles Mentioning

```dataview
TABLE file.ctime as "Date", title as "Article", url as "Source"
FROM "articles"
WHERE contains(content, "Final Act") OR contains(aliases, this.file.name)
SORT file.ctime DESC
LIMIT 10
```

*Last updated: 2025-06-27*