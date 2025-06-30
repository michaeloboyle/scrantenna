---
aliases: []
tags: [person, {{entity_category}}]
entity_type: PERSON
confidence: {{confidence_score}}
first_mentioned: {{first_mentioned_date}}
last_mentioned: {{last_mentioned_date}}
mention_count: {{mention_count}}
official_title: "{{official_title}}"
location: "[[{{primary_location}}]]"
organization: "[[{{primary_organization}}]]"
bio: "{{bio_summary}}"
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

> **{{official_title}}** | **{{primary_location}}**

## Quick Facts
- **Full Name**: {{entity_name}}
- **Position**: {{official_title}}
- **Location**: [[{{primary_location}}]]
- **Organization**: [[{{primary_organization}}]]
- **First Mentioned**: [[{{first_mentioned_date}}]]

## Recent Activity

### {{current_month}} {{current_year}}
- **[[{{recent_date}}]]**: {{recent_activity_description}}

## Key Relationships

- **{{relationship_type}}**: [[{{relationship_target}}]]

## Projects & Initiatives

- [[{{project_name}}]] - {{project_description}}

## Articles Mentioning

```dataview
TABLE file.ctime as "Date", title as "Article", url as "Source"
FROM "articles"
WHERE contains(content, "{{entity_name}}") OR contains(aliases, this.file.name)
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

*Last updated: {{last_updated_date}}*