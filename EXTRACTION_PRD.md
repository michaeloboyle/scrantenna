# Entity & Relationship Extraction PRD

## Product Vision
Create high-quality, accurate entity and relationship extraction from Scranton news articles to build a reliable knowledge graph foundation for future Neo4j integration.

## Problem Statement
Current extraction produces low-quality results:
- **False Entities**: Headlines become PERSON entities ("Cognetti Announces New Infrastructure Project")
- **Malformed Entities**: Concatenated text ("Scranton Scranton Mayor Paige Cognetti") 
- **Missing Entities**: Quoted works, proper locations, organizations
- **Incorrect Classification**: Movies as PERSON, locations as PERSON
- **Poor Relationships**: Duplicate edges, unclear direction, missing context

## Success Criteria

### Quality Metrics
- **Precision**: >85% of extracted entities are valid and correctly classified
- **Recall**: >80% of actual entities in text are captured
- **Relationship Accuracy**: >75% of relationships have correct direction and type
- **No Duplicates**: Each entity appears only once per article
- **Clean Names**: No malformed concatenated entity names

### Entity Requirements

#### PERSON Entities
- ✅ **Include**: Full names (First Last), titled persons (Mayor Smith)
- ❌ **Exclude**: Headlines, action phrases, job descriptions without names
- **Examples**: 
  - ✅ "Paige Cognetti", "Mayor Cognetti", "Commissioner Johnson"
  - ❌ "Cognetti Announces Project", "Woman to Serve"

#### LOCATION Entities  
- ✅ **Include**: Cities, venues, addresses, geographic features
- ❌ **Exclude**: Abstract concepts, events
- **Examples**:
  - ✅ "Ritz Theater", "Providence Road", "Scranton", "City Hall"
  - ❌ "Infrastructure Project", "Meeting Location"

#### ORGANIZATION Entities
- ✅ **Include**: Companies, government agencies, institutions
- ❌ **Exclude**: Generic department references without names
- **Examples**:
  - ✅ "Department of Public Works", "Scranton Police Department", "NBC News"
  - ❌ "The Department", "Local Authority"

#### WORK Entities
- ✅ **Include**: Movies, TV shows, books, projects (especially quoted)
- **Examples**:
  - ✅ "Final Act", "The Office", "V/H/S"
  - ❌ "Infrastructure Project" (unless proper name)

### Relationship Requirements

#### Verb-Based Relationships
- **Extract ALL verbs** between entities as potential edges
- **Proper Direction**: Subject → Verb → Object
- **Normalized Types**: ANNOUNCED, JOINED, WORKS_FOR, LIVES_IN, etc.
- **Context Preservation**: Include original verb in metadata

#### Relationship Categories
1. **Professional**: WORKS_FOR, MANAGES, LEADS, HIRED, FIRED
2. **Location**: LIVES_IN, LOCATED_IN, VISITED, MOVED_TO  
3. **Social**: MET, MARRIED, SUPPORTS, OPPOSES
4. **Creative**: CREATED, STARRED_IN, DIRECTED, PRODUCED
5. **Legal**: SUED, CHARGED, SENTENCED, ELECTED
6. **Communication**: ANNOUNCED, SAID, DECLARED, REVEALED

## Technical Implementation

### Phase 1: Enhanced Rule-Based Extraction
**Timeline**: Immediate (this session)

#### Entity Filtering
- **Blacklist patterns**: Headlines, action phrases, malformed concatenations
- **Whitelist validation**: Proper name patterns, known entity formats
- **Deduplication**: Remove exact matches and semantic duplicates
- **Length limits**: Min 2 chars, max 50 chars per entity

#### Pattern Improvements
- **Quoted content detection**: Movies, shows, projects in quotes
- **Title + Name extraction**: Separate titles from names properly
- **Address/Venue patterns**: Street names, building names
- **Organization patterns**: "Department of X", "X Company", "X Inc"

#### Relationship Enhancement
- **Bidirectional checking**: A→B and B→A patterns
- **Passive voice support**: "was announced by", "is managed by"
- **Multi-word verbs**: "signed with", "filed lawsuit against"
- **Temporal relationships**: "before", "after", "during"

### Phase 2: LLM-Enhanced Extraction  
**Timeline**: After rule-based improvements

#### Ollama Integration
- **Local Llama 3.2**: Privacy-preserving, cost-free extraction
- **Structured prompts**: JSON output with validation
- **Fallback chain**: Ollama → HuggingFace → Rules
- **Quality scoring**: Confidence metrics per extraction method

#### Training Data
- **Ground truth creation**: Manually annotate 50 Scranton articles
- **Validation set**: Test extraction accuracy against known entities
- **Iterative improvement**: Adjust prompts based on results

### Phase 3: Quality Assurance
**Timeline**: Before Neo4j integration

#### Validation Pipeline
- **Entity verification**: Check against known person/place databases
- **Relationship validation**: Verify verb-entity combinations make sense
- **Duplicate detection**: Advanced fuzzy matching (Mike vs Michael)
- **Human review interface**: Flag uncertain extractions for manual review

#### Metrics Dashboard
- **Real-time quality scores**: Precision, recall, confidence
- **Entity distribution**: Types, sources, trends over time  
- **Relationship network stats**: Density, centrality, communities
- **Error analysis**: Common failure patterns, improvement opportunities

## Success Validation

### Test Cases
1. **Movie Article**: Should extract actors (PERSON), movie (WORK), theater (LOCATION), production company (ORGANIZATION)
2. **Political Article**: Should extract officials (PERSON), offices (ORGANIZATION), locations (LOCATION), proper relationships
3. **Business Article**: Should extract executives (PERSON), companies (ORGANIZATION), actions (ANNOUNCED, HIRED)

### Quality Gates
- **No malformed entities**: Zero concatenated or headline entities
- **Correct classifications**: >90% accuracy on entity types
- **Complete relationships**: Every verb between entities becomes an edge
- **Clean deduplication**: No semantic duplicates in final output

## Future Considerations

### Neo4j Integration Prep
- **Schema design**: Optimized for graph queries and analytics
- **Batch loading**: Efficient bulk import of historical data
- **Incremental updates**: Daily addition of new entities/relationships  
- **Data lineage**: Track which articles contributed each entity/relationship

### Advanced Analytics Ready
- **Community detection**: Find entity clusters and influence networks
- **Temporal analysis**: Track relationship evolution over time
- **Centrality metrics**: Identify most important entities in Scranton news
- **Recommendation engine**: "Related entities you might be interested in"

## Next Steps
1. ✅ **Immediate**: Fix rule-based extraction patterns and filtering
2. 🔄 **Short-term**: Implement quality validation and deduplication  
3. 📋 **Medium-term**: Integrate Ollama for LLM-enhanced extraction
4. 🎯 **Long-term**: Prepare clean, high-quality data for Neo4j accumulation

---

*The goal is bulletproof extraction quality before we start building our Neo4j knowledge base. Quality over quantity - better to have 100 perfect entities than 1000 noisy ones.*