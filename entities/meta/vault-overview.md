# Scrantenna Entity Vault Overview

## Entity Statistics

### By Type
```dataview
TABLE length(rows) as "Count"
FROM ""
GROUP BY entity_type
SORT length(rows) DESC
```

### By Confidence Score
```dataview
TABLE length(rows) as "Count"
FROM ""
WHERE confidence >= 0.9
GROUP BY "High Confidence (≥0.9)"
```

```dataview
TABLE length(rows) as "Count"
FROM ""
WHERE confidence >= 0.7 AND confidence < 0.9
GROUP BY "Medium Confidence (0.7-0.9)"
```

```dataview
TABLE length(rows) as "Count"
FROM ""
WHERE confidence < 0.7
GROUP BY "Low Confidence (<0.7)"
```

## Most Mentioned Entities

```dataview
TABLE mention_count as "Mentions", entity_type as "Type", last_mentioned as "Last Seen"
FROM ""
SORT mention_count DESC
LIMIT 15
```

## Recent Activity

### Newly Added Entities (Last 7 Days)
```dataview
TABLE entity_type as "Type", first_mentioned as "First Seen", mention_count as "Mentions"
FROM ""
WHERE date(first_mentioned) >= date(today) - dur(7 days)
SORT first_mentioned DESC
```

### Recently Updated Entities
```dataview
TABLE entity_type as "Type", last_mentioned as "Last Updated", mention_count as "Total Mentions"
FROM ""
SORT last_mentioned DESC
LIMIT 10
```

## Entity Relationships

### Most Connected Entities
```dataview
TABLE length(relationships) as "Connections", entity_type as "Type"
FROM ""
SORT length(relationships) DESC
LIMIT 10
```

### Relationship Types
```dataview
TABLE relationships.type as "Relationship Type", length(rows.relationships) as "Count"
FROM ""
FLATTEN relationships
GROUP BY relationships.type
SORT length(rows.relationships) DESC
```

## Quality Metrics

### Entities Needing Review (Low Confidence)
```dataview
LIST
FROM ""
WHERE confidence < 0.7
```

### Single-Source Entities (Needs Verification)
```dataview
LIST
FROM ""
WHERE length(sources) = 1
```

### Entities with No Relationships
```dataview
LIST
FROM ""
WHERE !relationships OR length(relationships) = 0
```

## Vault Health

- **Total Entities**: `$= dv.pages().length`
- **Average Confidence**: `$= dv.pages().where(p => p.confidence).map(p => p.confidence).array().reduce((a, b) => a + b, 0) / dv.pages().where(p => p.confidence).length`
- **Total Relationships**: `$= dv.pages().where(p => p.relationships).map(p => p.relationships?.length || 0).array().reduce((a, b) => a + b, 0)`

*Last updated: 2025-06-27*