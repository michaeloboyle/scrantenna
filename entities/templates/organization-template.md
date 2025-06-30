---
aliases: []
tags: [organization, {{org_category}}]
entity_type: ORGANIZATION
confidence: {{confidence_score}}
first_mentioned: {{first_mentioned_date}}
last_mentioned: {{last_mentioned_date}}
mention_count: {{mention_count}}
organization_type: "{{organization_type}}"
parent_organization: "[[{{parent_organization}}]]"
location: "[[{{primary_location}}]]"
website: "{{website_url}}"
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

> **{{organization_type}}** | **[[{{primary_location}}]]**

## Quick Facts
- **Type**: {{organization_type}}
- **Location**: [[{{primary_location}}]]
- **Parent Org**: [[{{parent_organization}}]]
- **Website**: {{website_url}}
- **First Mentioned**: [[{{first_mentioned_date}}]]

## Description

{{organization_description}}

## Key Personnel

```dataview
LIST
FROM "people"
WHERE contains(organization, "{{entity_name}}") OR contains(string(relationships), "{{entity_name}}")
```

## Recent Activity

### {{current_month}} {{current_year}}
- **[[{{recent_date}}]]**: {{recent_activity_description}}

## Projects & Initiatives

- [[{{project_name}}]] - {{project_description}}

## Related Organizations

```dataview
LIST
FROM "organizations"
WHERE contains(parent_organization, "{{entity_name}}") OR contains(string(relationships), "{{entity_name}}")
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