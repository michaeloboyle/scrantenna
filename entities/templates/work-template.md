---
aliases: []
tags: [work, {{work_category}}]
entity_type: WORK
confidence: {{confidence_score}}
first_mentioned: {{first_mentioned_date}}
last_mentioned: {{last_mentioned_date}}
mention_count: {{mention_count}}
work_type: "{{work_type}}"
genre: "{{genre}}"
year: {{year}}
status: "{{status}}"
location: "[[{{filming_location}}]]"
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

> **{{work_type}}** | **{{genre}}** | **{{year}}**

## Quick Facts
- **Type**: {{work_type}}
- **Genre**: {{genre}}
- **Year**: {{year}}
- **Status**: {{status}}
- **Location**: [[{{filming_location}}]]
- **First Mentioned**: [[{{first_mentioned_date}}]]

## Description

{{work_description}}

## Cast & Crew

### Actors
```dataview
LIST
FROM "people"
WHERE contains(string(relationships), "{{entity_name}}") AND contains(string(relationships), "STARS_IN|APPEARS_IN|ACTS_IN")
```

### Production Team
```dataview
LIST
FROM "people"
WHERE contains(string(relationships), "{{entity_name}}") AND contains(string(relationships), "DIRECTED|PRODUCED|CREATED")
```

## Production Details

### {{current_month}} {{current_year}}
- **[[{{recent_date}}]]**: {{recent_activity_description}}

## Related Works

```dataview
LIST
FROM "works"
WHERE contains(string(relationships), "{{entity_name}}") OR contains(genre, this.genre)
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