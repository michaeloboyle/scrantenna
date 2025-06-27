// Scrantenna Sample Neo4j Queries
// Generated on 2025-06-26T16:56:17.261962

// 1. Find most mentioned entities
MATCH (e:Entity)<-[:MENTIONS]-(a:Article)
RETURN e.name, e.type, COUNT(a) as mentions
ORDER BY mentions DESC
LIMIT 10;

// 2. Find entities connected to Scranton
MATCH (scranton:Entity {name: 'Scranton'})-[r]-(connected)
RETURN scranton.name, type(r), connected.name, connected.type;

// 3. Articles by source with entity counts
MATCH (a:Article)-[:MENTIONS]->(e:Entity)
RETURN a.source, COUNT(DISTINCT e) as entity_count, COUNT(a) as articles
ORDER BY entity_count DESC;

// 4. Find relationship paths between entities
MATCH path = (from:Entity)-[*1..3]-(to:Entity)
WHERE from.name = 'Paige Cognetti' AND to.name = 'Scranton'
RETURN path
LIMIT 5;

// 5. Timeline analysis - entities by publication date
MATCH (a:Article)-[:MENTIONS]->(e:Entity)
WHERE a.published_at IS NOT NULL
RETURN date(a.published_at) as date, COUNT(DISTINCT e) as entities
ORDER BY date DESC;

// 6. Find most influential entities (highest degree centrality)
MATCH (e:Entity)
RETURN e.name, e.type, size((e)--()) as connections
ORDER BY connections DESC
LIMIT 10;

// 7. Community detection (requires APOC or GDS library)
// CALL gds.louvain.stream('entityGraph')
// YIELD nodeId, communityId
// RETURN gds.util.asNode(nodeId).name as entity, communityId
// ORDER BY communityId;

// 8. Find articles mentioning multiple entity types
MATCH (a:Article)-[:MENTIONS]->(e:Entity)
WITH a, COLLECT(DISTINCT e.type) as types
WHERE size(types) > 2
RETURN a.title, a.source, types
ORDER BY size(types) DESC;

// 9. Recent news analysis (last 7 days)
MATCH (a:Article)-[:MENTIONS]->(e:Entity)
WHERE a.published_at >= date() - duration('P7D')
RETURN e.name, e.type, COUNT(a) as recent_mentions
ORDER BY recent_mentions DESC
LIMIT 15;

// 10. Entity co-occurrence analysis
MATCH (a:Article)-[:MENTIONS]->(e1:Entity),
      (a)-[:MENTIONS]->(e2:Entity)
WHERE e1.name < e2.name
RETURN e1.name, e2.name, COUNT(a) as co_occurrences
ORDER BY co_occurrences DESC
LIMIT 20;