---
aliases: []
tags: [location, {{location_category}}]
entity_type: LOCATION
confidence: 0.8
first_mentioned: 2025-06-27
last_mentioned: 2025-06-27
mention_count: 1
location_type: "{{location_type}}"
address: "{{address}}"
city: "[[Scranton]]"
county: "[[Lackawanna County]]"
state: "[[Pennsylvania]]"
geo_coordinates: [{{latitude}}, {{longitude}}]
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

# Ritz Theater

> **{{location_type}}** in **[[Scranton]], [[Pennsylvania]]**

## Quick Facts
- **Type**: {{location_type}}
- **Address**: {{address}}
- **City**: [[Scranton]]
- **County**: [[Lackawanna County]]
- **First Mentioned**: [[2025-06-27]]

## Description

{{location_description}}

## Recent Activity

### June 2025
- **[[2025-06-27]]**: First mentioned in news article

## Connected Entities

### People
```dataview
LIST
FROM "people"
WHERE contains(location, "Ritz Theater") OR contains(string(relationships), "Ritz Theater")
```

### Organizations
```dataview
LIST  
FROM "organizations"
WHERE contains(location, "Ritz Theater") OR contains(string(relationships), "Ritz Theater")
```

### Events
```dataview
LIST
FROM "events"
WHERE contains(location, "Ritz Theater") OR contains(string(relationships), "Ritz Theater")
```

## Articles Mentioning

```dataview
TABLE file.ctime as "Date", title as "Article", url as "Source"
FROM "articles"
WHERE contains(content, "Ritz Theater") OR contains(aliases, this.file.name)
SORT file.ctime DESC
LIMIT 10
```

*Last updated: 2025-06-27*