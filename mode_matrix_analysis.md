# Scrantenna Mode Combination Matrix Analysis

## Current Mode Structure

**View Modes:** Text | Graph  
**Format Modes:** Full | Brief

## Complete Matrix (4 Combinations)

| View | Format | Status | User Experience | Issues/Dead Ends |
|------|--------|--------|-----------------|------------------|
| **Text** | **Full** | ✅ **Primary** | Read complete articles with full headlines and content | None - ideal reading experience |
| **Text** | **Brief** | ✅ **Secondary** | Read distilled/SVO versions of articles | Works if distilled content exists |
| **Graph** | **Full** | ⚠️ **Questionable** | Explore knowledge graph (format irrelevant) | **Dead end**: Format has no effect on graphs |
| **Graph** | **Brief** | ⚠️ **Questionable** | Explore knowledge graph (format irrelevant) | **Dead end**: Format has no effect on graphs |

## Dead End Analysis

### 1. **Graph + Format = Dead End**
**Problem:** When in Graph view, the Full/Brief toggle becomes meaningless
- Graph visualization doesn't use article text content
- Format buttons remain active but do nothing
- User may click Brief/Full expecting different graph views
- Confusing state where controls appear functional but aren't

### 2. **Missing Data Dead Ends**
**Problem:** Brief mode fails when distilled content is missing
- `article.title_distilled` or `description_distilled` undefined
- Falls back to "No distilled title/content" 
- User gets broken experience instead of graceful fallback

### 3. **Empty Graph Dead Ends**
**Problem:** Graph mode with no entities/relationships
- Shows "No entities found" placeholder
- No way to recover except switching back to Text
- Wasted user interaction

## Proposed Solutions

### Option A: Contextual Controls (Recommended)
Hide irrelevant controls based on current view:

```javascript
function updateControlVisibility() {
    const formatGroup = document.querySelector('.format-group');
    
    if (currentView === 'graph') {
        formatGroup.style.opacity = '0.3';
        formatGroup.style.pointerEvents = 'none';
        // Add tooltip: "Format only applies to text view"
    } else {
        formatGroup.style.opacity = '1';
        formatGroup.style.pointerEvents = 'auto';
    }
}
```

### Option B: Unified Mode Selection
Replace 2x2 matrix with 3 distinct modes:
- **Read Full** (Text + Full)
- **Read Brief** (Text + Brief) 
- **Explore** (Graph only)

### Option C: Smart Graph Formatting
Make format meaningful for graphs:
- **Full Graph**: Show all entities and relationships
- **Brief Graph**: Show only high-confidence entities, key relationships

### Option D: Progressive Disclosure
Start with just View toggle, reveal Format only in Text mode:

```
[Read] [Explore]           <- Always visible
  ↓
[Full] [Brief]            <- Only when Read is selected
```

## Cognitive Load Analysis

### Current System (2 independent toggles)
- **States:** 4 possible combinations
- **Cognitive load:** Medium (user must understand interaction)
- **Error potential:** High (dead end states)

### Option B (3 modes)
- **States:** 3 clear modes
- **Cognitive load:** Low (each mode is distinct)
- **Error potential:** Low (no invalid combinations)

### Option D (Progressive)
- **States:** 3 effective modes
- **Cognitive load:** Lowest (hierarchical revelation)
- **Error potential:** Minimal (guided interaction)

## Recommendation: Option D + Smart Fallbacks

1. **Implement Progressive Disclosure**
   - Primary: [📄 Read] [🕸️ Explore] 
   - Secondary (only when Read active): [Full] [Brief]

2. **Add Smart Fallbacks**
   - Brief mode with missing data → Auto-fallback to Full
   - Empty graphs → Show "Generate graph" suggestion

3. **Contextual Feedback**
   - Brief button disabled if no distilled content available
   - Graph button shows entity count preview: "Explore (5 entities)"

This eliminates dead ends while maintaining the clean Rams-inspired aesthetic.