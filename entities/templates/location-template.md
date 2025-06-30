---
aliases: []
tags: [location, {{location_category}}]
entity_type: LOCATION
confidence: {{confidence_score}}
first_mentioned: {{first_mentioned_date}}
last_mentioned: {{last_mentioned_date}}
mention_count: {{mention_count}}
location_type: "{{location_type}}"
address: "{{address}}"
city: "[[Scranton]]"
county: "[[Lackawanna County]]"
state: "[[Pennsylvania]]"
geo_coordinates: [{{latitude}}, {{longitude}}]
relationships:
  - target: "[[{{relationship_target}}]]"
    type: "{{relationship_type}}"
    confidence: {{relationship_confidence}}
sources:
  - url: "{{source_url}}"
    title: "{{article_title}}"
    date: {{article_date}}
    mentions: {{article_mentions}}
---

# {{entity_name}}

> **{{location_type}}** in **[[Scranton]], [[Pennsylvania]]**

## Quick Facts
- **Type**: {{location_type}}
- **Address**: {{address}}
- **City**: [[Scranton]]
- **County**: [[Lackawanna County]]
- **First Mentioned**: [[{{first_mentioned_date}}]]

## Description

{{location_description}}

## Recent Activity

### {{current_month}} {{current_year}}
- **[[{{recent_date}}]]**: {{recent_activity_description}}

## Connected Entities

### People
```dataview
LIST
FROM "people"
WHERE contains(location, "{{entity_name}}") OR contains(string(relationships), "{{entity_name}}")
```

### Organizations
```dataview
LIST  
FROM "organizations"
WHERE contains(location, "{{entity_name}}") OR contains(string(relationships), "{{entity_name}}")
```

### Events
```dataview
LIST
FROM "events"
WHERE contains(location, "{{entity_name}}") OR contains(string(relationships), "{{entity_name}}")
```

## Articles Mentioning

```dataview
TABLE file.ctime as "Date", title as "Article", url as "Source"
FROM "articles"
WHERE contains(content, "{{entity_name}}") OR contains(aliases, this.file.name)
SORT file.ctime DESC
LIMIT 10
```

*Last updated: {{last_updated_date}}*