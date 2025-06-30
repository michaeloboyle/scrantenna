# Entity & Relationship Extraction Patterns

## Core Principle: Subject-Verb-Object Triples

**Goal**: Extract clean entities and connect them with verb-based relationships, not create malformed concatenated entities.

## What We Want vs What We're Getting

### ❌ Current Problems

**Input**: "Mayor Cognetti announces new infrastructure project"
**Bad Output**:
```json
{
  "entities": [
    {"name": "Cognetti Announces New Infrastructure Project", "type": "PERSON"}
  ]
}
```

### ✅ Desired Output

**Input**: "Mayor Cognetti announces new infrastructure project"  
**Good Output**:
```json
{
  "entities": [
    {"name": "Paige Cognetti", "type": "PERSON"},
    {"name": "infrastructure project", "type": "WORK"}
  ],
  "relationships": [
    {"from": "Paige Cognetti", "to": "infrastructure project", "type": "ANNOUNCED", "verb": "announces"}
  ]
}
```

## Entity Extraction Rules

### PERSON Entities
- ✅ **Extract**: First Last names, titled persons
- ❌ **Never**: Headlines, action phrases, job descriptions alone

**Examples**:
```
✅ "Paige Cognetti" (from "Mayor Paige Cognetti announces...")  
✅ "Hannah Fierman" (from "actress Hannah Fierman")
✅ "Douglas Tait" (from "Douglas Tait (Teen Wolf)")
❌ "Cognetti Announces Project"
❌ "Producer Underway With Avaryana Rose"  
❌ "Vincent M. Ward Actress"
```

**Patterns**:
```regex
# Full names (2-3 words, proper case)
\b[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b

# Titled persons (extract name after title)
(?:Mayor|Judge|Commissioner|Rep\.|Dr\.)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)
```

### WORK Entities  
- ✅ **Extract**: Movies, TV shows, books, projects (especially quoted)
- ❌ **Never**: Generic project references

**Examples**:
```
✅ "Final Act" (from "'Final Act': Paranormal Horror...")
✅ "V/H/S" (from "Hannah Fierman (V/H/S)")  
✅ "Teen Wolf" (from "Douglas Tait (Teen Wolf)")
✅ "The Walking Dead" (from "Vincent M. Ward (The Walking Dead)")
❌ "Paranormal Horror From"
❌ "Producer Underway"
```

**Patterns**:
```regex
# Quoted works
['"]([^'"]+)['"]

# Parenthetical references (shows/movies)
\(([A-Z][^)]+)\)

# Proper work titles
\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b(?=\s*:|\s*-|\s*is\s+filming)
```

### LOCATION Entities
- ✅ **Extract**: Venues, addresses, cities, theaters
- ❌ **Never**: Abstract concepts

**Examples**:
```
✅ "Ritz Theater" (from "filming at the Ritz Theater")
✅ "Scranton" (from "locations in Scranton")  
✅ "Providence Road" (from "targeting Providence Road")
❌ "Infrastructure Project"
❌ "Meeting Location"
```

### ORGANIZATION Entities
- ✅ **Extract**: Companies, agencies, departments
- ❌ **Never**: Generic references

**Examples**:
```
✅ "Department of Public Works"
✅ "Scranton Police Department"  
❌ "The Department"
❌ "Local Authority"
```

## Relationship Extraction Rules

### Verb-Based Relationships

**Core Pattern**: Find Entity1 + Verb + Entity2, create edge with verb as relationship type

**Examples**:

```
Input: "Mayor Cognetti announced the project"
→ ("Paige Cognetti") -[ANNOUNCED]-> ("infrastructure project")

Input: "Hannah Fierman joined the cast"  
→ ("Hannah Fierman") -[JOINED]-> ("Final Act")

Input: "filming at the Ritz Theater"
→ ("Final Act") -[FILMED_AT]-> ("Ritz Theater")

Input: "Douglas Tait (Teen Wolf)"
→ ("Douglas Tait") -[APPEARED_IN]-> ("Teen Wolf")
```

### Extraction Algorithm

1. **Extract Clean Entities First**
   - Use strict patterns for each entity type
   - Validate length (2-50 characters)
   - Remove duplicates and malformed names

2. **Find Verb Connections**
   - Look for verbs between any two entities
   - Support both active and passive voice
   - Normalize verbs to relationship types

3. **Validate Relationships**
   - Both entities must exist in entity list
   - Avoid self-references  
   - Remove duplicates

## Test Cases

### Test Case 1: Movie Article
**Input**: "'Final Act': Paranormal Horror From 'Popeye' Producer. Actress Avaryana Rose joined Hannah Fierman (V/H/S) and Douglas Tait (Teen Wolf) filming at the Ritz Theater in Scranton."

**Expected Output**:
```json
{
  "entities": [
    {"name": "Final Act", "type": "WORK"},
    {"name": "Avaryana Rose", "type": "PERSON"},
    {"name": "Hannah Fierman", "type": "PERSON"},
    {"name": "Douglas Tait", "type": "PERSON"},
    {"name": "V/H/S", "type": "WORK"},
    {"name": "Teen Wolf", "type": "WORK"},
    {"name": "Ritz Theater", "type": "LOCATION"},
    {"name": "Scranton", "type": "LOCATION"}
  ],
  "relationships": [
    {"from": "Avaryana Rose", "to": "Final Act", "type": "JOINED", "verb": "joined"},
    {"from": "Hannah Fierman", "to": "V/H/S", "type": "APPEARED_IN", "verb": "appeared"},
    {"from": "Douglas Tait", "to": "Teen Wolf", "type": "APPEARED_IN", "verb": "appeared"},
    {"from": "Final Act", "to": "Ritz Theater", "type": "FILMED_AT", "verb": "filming"},
    {"from": "Ritz Theater", "to": "Scranton", "type": "LOCATED_IN", "verb": "in"}
  ]
}
```

### Test Case 2: Political Article
**Input**: "Mayor Paige Cognetti announced a $2 million infrastructure project targeting Providence Road. The Department of Public Works will manage the project."

**Expected Output**:
```json
{
  "entities": [
    {"name": "Paige Cognetti", "type": "PERSON"},
    {"name": "infrastructure project", "type": "WORK"},
    {"name": "Providence Road", "type": "LOCATION"},
    {"name": "Department of Public Works", "type": "ORGANIZATION"}
  ],
  "relationships": [
    {"from": "Paige Cognetti", "to": "infrastructure project", "type": "ANNOUNCED", "verb": "announced"},
    {"from": "infrastructure project", "to": "Providence Road", "type": "TARGETS", "verb": "targeting"},
    {"from": "Department of Public Works", "to": "infrastructure project", "type": "MANAGES", "verb": "manage"}
  ]
}
```

## Common Extraction Errors to Avoid

1. **Concatenated Headlines as Entities**:
   - ❌ "Cognetti Announces New Infrastructure Project"
   - ✅ Extract "Paige Cognetti" + relationship

2. **Malformed Person Names**:
   - ❌ "Vincent M. Ward Actress"  
   - ✅ "Vincent M. Ward"

3. **Generic Works as Persons**:
   - ❌ {"name": "Final Act", "type": "PERSON"}
   - ✅ {"name": "Final Act", "type": "WORK"}

4. **Missing Verb Relationships**:
   - ❌ Only extracting entities without connections
   - ✅ Every verb between entities becomes an edge

5. **Title Concatenation**:
   - ❌ "Mayor Paige Cognetti" as entity name
   - ✅ "Paige Cognetti" with HAS_TITLE relationship to "Mayor"

## Implementation Priority

1. **Phase 1**: Fix entity patterns to avoid malformed names
2. **Phase 2**: Implement proper verb-based relationship extraction  
3. **Phase 3**: Add validation and quality scoring
4. **Phase 4**: Test against real Scranton articles

---

*The goal is clean, structured data: proper entities connected by meaningful verb relationships, not concatenated headline garbage.*