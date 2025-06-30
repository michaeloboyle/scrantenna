---
aliases: []
tags: [person, person]
entity_type: PERSON
confidence: 0.9
first_mentioned: 2025-06-27
last_mentioned: 2025-06-27
mention_count: 1
official_title: ""
location: "[[Scranton]]"
organization: "[[]]"
bio: ""
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

# Mayor Cognetti

> **** | **Scranton**

## Quick Facts
- **Full Name**: Mayor Cognetti
- **Position**: 
- **Location**: [[Scranton]]
- **Organization**: [[]]
- **First Mentioned**: [[2025-06-27]]

## Recent Activity

### June 2025
- **[[2025-06-27]]**: First mentioned in news article

## Key Relationships

- ****: [[]]

## Projects & Initiatives

- [[]] - 

## Articles Mentioning

```dataview
TABLE file.ctime as "Date", title as "Article", url as "Source"
FROM "articles"
WHERE contains(content, "Mayor Cognetti") OR contains(aliases, this.file.name)
SORT file.ctime DESC
LIMIT 10
```

## Relationship Network

```dataview
TABLE relationships.target as "Connected To", relationships.type as "Relationship", relationships.confidence as "Confidence"
FROM ""
WHERE file = this.file
FLATTEN relationships
```

*Last updated: 2025-06-27*