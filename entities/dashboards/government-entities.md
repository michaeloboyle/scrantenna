# Government Entities Dashboard

## Scranton Government

### Mayor
```dataview
TABLE official_title as "Title", location as "Location", mention_count as "Mentions"
FROM "people/government"
WHERE contains(official_title, "Mayor")
```

### Commissioners
```dataview
TABLE official_title as "Title", organization as "Organization", mention_count as "Mentions"
FROM "people/government"
WHERE contains(official_title, "Commissioner")
```

## Government Organizations

```dataview
TABLE organization_type as "Type", location as "Location", mention_count as "Mentions"
FROM "organizations/government"
```

## Recent Government Activity

```dataview
TABLE file.ctime as "Date", file.name as "Entity", mention_count as "Total Mentions"
FROM "people/government" OR "organizations/government"
SORT file.ctime DESC
LIMIT 10
```

## Government Relationships

```dataview
TABLE relationships.target as "Connected To", relationships.type as "Relationship"
FROM "people/government"
FLATTEN relationships
WHERE relationships.type = "MAYOR_OF" OR relationships.type = "COMMISSIONER_OF" OR relationships.type = "OVERSEES"
```

## Most Mentioned Government Figures

```dataview
TABLE mention_count as "Mentions", official_title as "Title", last_mentioned as "Last Seen"
FROM "people/government"
SORT mention_count DESC
```