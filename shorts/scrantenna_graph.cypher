// Scrantenna Knowledge Graph Import
// Generated on 2025-06-26T16:56:17.261689

// Clear existing data (CAUTION: This will delete all data!)
// MATCH (n) DETACH DELETE n;

// Create constraints (run these first)
CREATE CONSTRAINT entity_name IF NOT EXISTS FOR (e:Entity) REQUIRE e.name IS UNIQUE;
CREATE CONSTRAINT article_id IF NOT EXISTS FOR (a:Article) REQUIRE a.id IS UNIQUE;

// Create Entity Nodes
// Person entities
MERGE (e:Entity:Person {name: 'Act'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Bill'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Bob'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Bolus'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Branch'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Cafes'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Commissioner'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Didnt'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Discussed'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Domhnall'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Federal'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Field'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Final'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Flash'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Flood'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Forgione'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Four'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Friday'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'From'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Gaughan'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Gebhardt'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Giardina'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Gleeson'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Grants'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Harveys'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Health'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Hill'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Horror'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'John'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Judge'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'K9s'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Krasinski'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'LaCoe'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Lackawanna'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Ledger'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Mayor'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Memory'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Month'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Northeastern'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Paige'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Paranormal'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Popeye'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Power'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Pride'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Prison'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Raising'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Rep'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Republican'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Riversides'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Rob'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Role'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Rutgers'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Says'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Section'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Serve'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Shrink'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Tavian'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'The'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Warning'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Weston'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Woman'}) SET e.type = 'Person', e.created_at = datetime();
MERGE (e:Entity:Person {name: 'Years'}) SET e.type = 'Person', e.created_at = datetime();

// Location entities
MERGE (e:Entity:Location {name: 'County'}) SET e.type = 'Location', e.created_at = datetime();
MERGE (e:Entity:Location {name: 'Lake'}) SET e.type = 'Location', e.created_at = datetime();
MERGE (e:Entity:Location {name: 'Pennsylvania'}) SET e.type = 'Location', e.created_at = datetime();
MERGE (e:Entity:Location {name: 'SCRANTON'}) SET e.type = 'Location', e.created_at = datetime();
MERGE (e:Entity:Location {name: 'Scranton'}) SET e.type = 'Location', e.created_at = datetime();

// Organization entities
MERGE (e:Entity:Organization {name: 'BASEBALL'}) SET e.type = 'Organization', e.created_at = datetime();
MERGE (e:Entity:Organization {name: 'FOOTBALL'}) SET e.type = 'Organization', e.created_at = datetime();
MERGE (e:Entity:Organization {name: 'LACKAWANNA'}) SET e.type = 'Organization', e.created_at = datetime();
MERGE (e:Entity:Organization {name: 'NWS'}) SET e.type = 'Organization', e.created_at = datetime();
MERGE (e:Entity:Organization {name: 'PPL'}) SET e.type = 'Organization', e.created_at = datetime();
MERGE (e:Entity:Organization {name: 'Police'}) SET e.type = 'Organization', e.created_at = datetime();
MERGE (e:Entity:Organization {name: 'TAYLOR'}) SET e.type = 'Organization', e.created_at = datetime();
MERGE (e:Entity:Organization {name: 'WBREWYOU'}) SET e.type = 'Organization', e.created_at = datetime();

// Create Article Nodes
CREATE (a:Article {id: 'short_0', title: '‘Final Act’: Paranormal Horror From ‘Popeye The Slayer Man’ Producer Underway With Avaryana Rose, Hannah Fierman, Douglas Tait & Vincent M. Ward', source: 'Deadline', published_at: '2025-06-24T15:23:19Z', url: 'http://deadline.com/2025/06/avaryana-rose-hannah-fierman-horror-movie-final-act-1236441042/'});
CREATE (a:Article {id: 'short_1', title: 'Woman To Serve Four Years in Prison for Role in $800,000 Business Email Hack That Tricked Victims Into Sending Fraudulent Bank Wires', source: 'The Daily Hodl', published_at: '2025-06-15T18:45:42Z', url: 'https://dailyhodl.com/2025/06/15/woman-to-serve-four-years-in-prison-for-role-in-800000-business-email-hack-that-tricked-victims-into-sending-fraudulent-bank-wires/'});
CREATE (a:Article {id: 'short_2', title: 'John Krasinski Says Domhnall Gleeson Discussed Taking Role in THE OFFICE Spinoff Series THE PAPER With Him', source: 'GeekTyrant', published_at: '2025-05-28T20:30:00Z', url: 'https://geektyrant.com/news/john-krasinski-says-domhnall-gleeson-discussed-taking-role-in-the-office-spinoff-series-the-paper-with-him'});
CREATE (a:Article {id: 'short_3', title: 'NWS issues Flash Flood Warning', source: '2822news.com', published_at: '2025-06-22T15:26:54Z', url: 'https://www.2822news.com/news/nws-issues-flash-flood-warning/'});
CREATE (a:Article {id: 'short_4', title: 'Lackawanna County mails property valuations, posts reassessment database', source: 'Thetimes-tribune.com', published_at: '2025-06-20T19:06:00Z', url: 'https://www.thetimes-tribune.com/2025/06/20/lackawanna-county-mails-property-valuations-posts-reassessment-database/'});
CREATE (a:Article {id: 'short_5', title: 'HS FOOTBALL: Riverside’s Branch chooses Rutgers', source: 'Thetimes-tribune.com', published_at: '2025-06-11T19:07:00Z', url: 'https://www.thetimes-tribune.com/2025/06/11/hs-football-riversides-branch-chooses-to-attend-rutgers/'});
CREATE (a:Article {id: 'short_6', title: 'Raising the flag in Scranton to mark start of Pride Month', source: 'Pahomepage.com', published_at: '2025-06-01T23:35:16Z', url: 'https://www.pahomepage.com/news/raising-the-flag-in-scranton-to-mark-start-of-pride-month/'});
CREATE (a:Article {id: 'short_7', title: 'As Federal Health Grants Shrink, Memory Cafes Help Dementia Patients and Their Caregivers', source: 'Kffhealthnews.org', published_at: '2025-06-10T09:00:00Z', url: 'https://kffhealthnews.org/news/article/memory-cafe-federal-health-grants-dementia-caregiver-wisconsin-pennsylvania/'});
CREATE (a:Article {id: 'short_8', title: 'Memory cafes offer camaraderie and fun for people with dementia — and their caregivers', source: 'NPR', published_at: '2025-05-31T09:00:00Z', url: 'https://www.npr.org/sections/shots-health-news/2025/05/31/nx-s1-5317646/memory-cafes-dementia-caregiving-respite-social-support'});
CREATE (a:Article {id: 'short_9', title: '\'Didn\'t send you there to trade\': Republican gets hammered by voter in town hall', source: 'Raw Story', published_at: '2025-06-17T18:30:59Z', url: 'https://www.rawstory.com/rob-bresnahan/'});
CREATE (a:Article {id: 'short_10', title: 'HS BASEBALL: Forgione, LaCoe, Giardina, Ledger named to all-star game', source: 'Thetimes-tribune.com', published_at: '2025-06-09T19:02:00Z', url: 'https://www.thetimes-tribune.com/2025/06/09/hs-baseball-forgione-lacoe-named-to-all-star-game/'});
CREATE (a:Article {id: 'short_11', title: 'Scranton cuts ribbon on new Weston Field pool complex', source: 'Times Tribune', published_at: '2025-06-25T19:25:02', url: 'https://www.thetimes-tribune.com/2025/06/25/scranton-cuts-the-ribbon-on-new-weston-field-pool-complex/'});
CREATE (a:Article {id: 'short_12', title: 'Judge likely to dismiss Bob Bolus lawsuit against Commissioner Bill Gaughan', source: 'Times Tribune', published_at: '2025-06-25T17:39:24', url: 'https://www.thetimes-tribune.com/2025/06/25/judge-likely-to-dismiss-bob-bolus-lawsuit-against-commissioner-bill-gaughan/'});
CREATE (a:Article {id: 'short_13', title: 'Power restored in part of Lackawanna County after weather-related outage', source: 'Wnep', published_at: '2025-06-25T00:49:08', url: 'https://www.wnep.com/article/news/local/lackawanna-county/over-300-ppl-customers-without-power-in-part-of-lackawanna-county-scranton-dunmore/523-9e24c63d-ba98-4942-be14-88e1981d3c7a'});
CREATE (a:Article {id: 'short_14', title: 'Police K-9s beat the heat and train in the water at Harveys Lake', source: 'Wnep', published_at: '2025-06-24T21:13:58', url: 'https://www.wnep.com/article/news/local/luzerne-county/luzerne-county-harveys-lake-k9-training-wilkes-barre-police/523-2e3cd41f-b94d-4e20-b0cc-b93f071b9940'});

// Create Relationships
// LOCATED_AT relationships
MATCH (from:Entity {name: 'Years'}), (to:Entity {name: 'Prison'}) CREATE (from)-[r:LOCATED_AT {article_id: 'short_1', source: 'The Daily Hodl'}]->(to);

// Article-Entity relationships
MATCH (a:Article {id: 'short_0'}), (e:Entity {name: 'Final'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_0'}), (e:Entity {name: 'Act'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_0'}), (e:Entity {name: 'Paranormal'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_0'}), (e:Entity {name: 'Horror'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_0'}), (e:Entity {name: 'From'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_0'}), (e:Entity {name: 'Popeye'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_1'}), (e:Entity {name: 'Woman'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_1'}), (e:Entity {name: 'Serve'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_1'}), (e:Entity {name: 'Four'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_1'}), (e:Entity {name: 'Years'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_1'}), (e:Entity {name: 'Prison'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_1'}), (e:Entity {name: 'Role'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_2'}), (e:Entity {name: 'John'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_2'}), (e:Entity {name: 'Krasinski'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_2'}), (e:Entity {name: 'Says'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_2'}), (e:Entity {name: 'Domhnall'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_2'}), (e:Entity {name: 'Gleeson'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_2'}), (e:Entity {name: 'Discussed'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_3'}), (e:Entity {name: 'NWS'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_3'}), (e:Entity {name: 'Flash'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_3'}), (e:Entity {name: 'Flood'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_3'}), (e:Entity {name: 'Warning'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_3'}), (e:Entity {name: 'WBREWYOU'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_3'}), (e:Entity {name: 'The'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_4'}), (e:Entity {name: 'Lackawanna'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_4'}), (e:Entity {name: 'County'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_4'}), (e:Entity {name: 'Friday'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_5'}), (e:Entity {name: 'FOOTBALL'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_5'}), (e:Entity {name: 'Riversides'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_5'}), (e:Entity {name: 'Branch'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_5'}), (e:Entity {name: 'Rutgers'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_5'}), (e:Entity {name: 'TAYLOR'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_5'}), (e:Entity {name: 'Tavian'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_6'}), (e:Entity {name: 'Raising'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_6'}), (e:Entity {name: 'Scranton'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_6'}), (e:Entity {name: 'Pride'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_6'}), (e:Entity {name: 'Month'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_6'}), (e:Entity {name: 'SCRANTON'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_6'}), (e:Entity {name: 'LACKAWANNA'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_7'}), (e:Entity {name: 'Federal'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_7'}), (e:Entity {name: 'Health'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_7'}), (e:Entity {name: 'Grants'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_7'}), (e:Entity {name: 'Shrink'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_7'}), (e:Entity {name: 'Memory'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_7'}), (e:Entity {name: 'Cafes'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_8'}), (e:Entity {name: 'Memory'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_9'}), (e:Entity {name: 'Didnt'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_9'}), (e:Entity {name: 'Republican'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_9'}), (e:Entity {name: 'Northeastern'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_9'}), (e:Entity {name: 'Pennsylvania'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_9'}), (e:Entity {name: 'Rep'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_9'}), (e:Entity {name: 'Rob'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_10'}), (e:Entity {name: 'BASEBALL'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_10'}), (e:Entity {name: 'Forgione'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_10'}), (e:Entity {name: 'LaCoe'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_10'}), (e:Entity {name: 'Giardina'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_10'}), (e:Entity {name: 'Ledger'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_10'}), (e:Entity {name: 'Four'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_11'}), (e:Entity {name: 'Scranton'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_11'}), (e:Entity {name: 'Weston'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_11'}), (e:Entity {name: 'Field'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_11'}), (e:Entity {name: 'Mayor'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_11'}), (e:Entity {name: 'Paige'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_11'}), (e:Entity {name: 'Gebhardt'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_12'}), (e:Entity {name: 'Judge'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_12'}), (e:Entity {name: 'Bob'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_12'}), (e:Entity {name: 'Bolus'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_12'}), (e:Entity {name: 'Commissioner'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_12'}), (e:Entity {name: 'Bill'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_12'}), (e:Entity {name: 'Gaughan'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_13'}), (e:Entity {name: 'Power'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_13'}), (e:Entity {name: 'Lackawanna'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_13'}), (e:Entity {name: 'County'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_13'}), (e:Entity {name: 'PPL'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_13'}), (e:Entity {name: 'Hill'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_13'}), (e:Entity {name: 'Section'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_14'}), (e:Entity {name: 'Police'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_14'}), (e:Entity {name: 'K9s'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_14'}), (e:Entity {name: 'Harveys'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_14'}), (e:Entity {name: 'Lake'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);
MATCH (a:Article {id: 'short_14'}), (e:Entity {name: 'Pennsylvania'}) CREATE (a)-[:MENTIONS {confidence: 0.5}]->(e);

// Create Indices for Performance
CREATE INDEX entity_type_idx IF NOT EXISTS FOR (e:Entity) ON (e.type);
CREATE INDEX article_source_idx IF NOT EXISTS FOR (a:Article) ON (a.source);
CREATE INDEX article_published_idx IF NOT EXISTS FOR (a:Article) ON (a.published_at);
