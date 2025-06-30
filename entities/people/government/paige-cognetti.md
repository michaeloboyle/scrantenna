---
aliases: ["Mayor Cognetti", "Paige Cognetti", "Mayor Paige Cognetti", "Paige Gebhardt Cognetti"]
tags: [person, government, mayor, scranton]
entity_type: PERSON
confidence: 1.0
first_mentioned: 2025-06-25
last_mentioned: 2025-06-27
mention_count: 15
official_title: "Mayor of Scranton"
location: "[[Scranton]]"
organization: "[[City of Scranton]]"
bio: "Current Mayor of Scranton, Pennsylvania, focusing on infrastructure and community development"
search_patterns:
  - "Mayor Cognetti"
  - "Paige.*Cognetti"
  - "Mayor.*Cognetti"
  - "Cognetti"
relationships:
  - target: "[[Scranton]]"
    type: "MAYOR_OF"
    confidence: 0.98
  - target: "[[City of Scranton]]"
    type: "LEADS"
    confidence: 0.95
  - target: "[[Department of Public Works]]"
    type: "OVERSEES"
    confidence: 0.85
sources:
  - url: "https://www.thetimes-tribune.com/2025/06/25/scranton-cuts-the-ribbon-on-new-weston-field-pool-complex/"
    title: "Scranton cuts ribbon on new Weston Field pool complex"
    date: 2025-06-25
    mentions: 5
---

# Paige Gebhardt Cognetti

> **Mayor of [[Scranton]], [[Pennsylvania]]**

## Quick Facts
- **Full Name**: Paige Gebhardt Cognetti
- **Position**: Mayor
- **Location**: [[City Hall]], [[Scranton]]
- **Organization**: [[City of Scranton]]
- **First Mentioned**: [[2025-06-25]]

## Recent Activity

### June 2025
- **[[2025-06-25]]**: Cut ribbon at [[Weston Field Pool Complex]] on [[Providence Road]]
- Announced $2 million infrastructure improvement project

## Key Relationships

- **Leads**: [[City of Scranton]]
- **Oversees**: [[Department of Public Works]]
- **Works with**: [[Commissioner Bill Gaughan|Bill Gaughan]]
- **Location**: Based in [[Scranton]], [[Pennsylvania]]

## Projects & Initiatives

- [[Weston Field Pool Complex]] - New swimming facility offering greater accessibility
- [[Providence Road Infrastructure Project]] - $2 million improvement project

## Articles Mentioning

```dataview
TABLE file.ctime as "Date", title as "Article", url as "Source"
FROM "articles"
WHERE contains(content, "Cognetti") OR contains(content, "Mayor") OR contains(aliases, this.file.name)
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