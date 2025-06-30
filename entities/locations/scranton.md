---
aliases: ["Scranton, PA", "Scranton, Pennsylvania", "City of Scranton", "Electric City"]
tags: [location, city, pennsylvania]
entity_type: LOCATION
confidence: 1.0
first_mentioned: 2025-06-25
last_mentioned: 2025-06-27
mention_count: 45
location_type: "City"
county: "[[Lackawanna County]]"
state: "[[Pennsylvania]]"
nickname: "Electric City"
population: 76328
geo_coordinates: [41.4090, -75.6624]
search_patterns:
  - "Scranton"
  - "Scranton,\\s*(PA|Pennsylvania)"
  - "Electric City"
relationships:
  - target: "[[Lackawanna County]]"
    type: "LOCATED_IN"
    confidence: 1.0
  - target: "[[Pennsylvania]]"
    type: "LOCATED_IN"
    confidence: 1.0
sources:
  - url: "https://www.thetimes-tribune.com/2025/06/25/scranton-cuts-the-ribbon-on-new-weston-field-pool-complex/"
    title: "Scranton cuts ribbon on new Weston Field pool complex"
    date: 2025-06-25
    mentions: 5
---

# Scranton

> **Electric City** | **[[Lackawanna County]], [[Pennsylvania]]**

## Quick Facts
- **Type**: City
- **County**: [[Lackawanna County]]
- **State**: [[Pennsylvania]]
- **Nickname**: Electric City
- **Population**: 76,328
- **Coordinates**: 41.4090, -75.6624
- **First Mentioned**: [[2025-06-25]]

## Description

Scranton is the largest city in Lackawanna County, Pennsylvania, known as "Electric City" for its early adoption of electric streetcars. Home to various government offices, cultural venues, and the fictional setting of the TV show [[The Office]].

## Government

- **Mayor**: [[Paige Gebhardt Cognetti|Paige Cognetti]]
- **Location**: [[City Hall]]

## Key Locations

### Venues
- [[Ritz Theater]] - Entertainment venue hosting film productions
- [[City Hall]] - Government center
- [[Weston Field]] - Recreation facility with new pool complex

### Infrastructure
- [[Providence Road]] - Major street with ongoing infrastructure improvements

### Neighborhoods
- [[Hill Section]] - Residential area

## Recent Activity

### June 2025
- **[[2025-06-25]]**: Ribbon cutting ceremony for [[Weston Field Pool Complex]]
- **[[2025-06-01]]**: Pride Month flag raising at [[City Hall]]

## Connected Entities

### Government Officials
```dataview
LIST
FROM "people/government"
WHERE contains(location, "Scranton") OR contains(string(relationships), "Scranton")
```

### Organizations
```dataview
LIST  
FROM "organizations"
WHERE contains(location, "Scranton") OR contains(string(relationships), "Scranton")
```

### Cultural References
- [[The Office]] - NBC TV show set in Scranton
- [[Dunder Mifflin]] - Fictional paper company from The Office

## Articles Mentioning

```dataview
TABLE file.ctime as "Date", title as "Article", url as "Source"
FROM "articles"
WHERE contains(content, "Scranton") OR contains(aliases, this.file.name)
SORT file.ctime DESC
LIMIT 15
```

*Last updated: 2025-06-27*