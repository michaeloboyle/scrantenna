Feature: Graph Visualization
  As a data analyst
  I want to visualize knowledge graphs extracted from news
  So that I can understand relationships and patterns in local news

  Background:
    Given the graph visualization system is loaded
    And sample news data with entities and relationships exists
    And the graph controls interface is initialized

  @visualization
  Scenario: Basic graph rendering
    Given I have entities and relationships from news articles
    When I render the knowledge graph
    Then I should see circular nodes for each entity
    And nodes should be colored by entity type
    And I should see lines connecting related entities
    And entity names should be displayed as labels
    And the graph should fit within the viewport

  @filtering
  Scenario: Entity type filtering
    Given I have a knowledge graph with multiple entity types
    When I toggle off "PERSON" entities in the filter panel
    Then person nodes should become semi-transparent
    And person-related edges should be hidden
    And the node count should update in statistics
    And I can toggle them back on to restore visibility

  @filtering
  Scenario: Relationship type filtering
    Given I have a graph with various relationship types
    When I disable "LOCATED_IN" relationships
    Then those relationship edges should be hidden
    And the relationship count should update
    And related nodes should remain visible
    And other relationship types should stay active

  @search
  Scenario: Entity search and highlighting
    Given I have a populated knowledge graph
    When I search for "Scranton" in the search box
    Then matching entities should be highlighted
    And the search results should list relevant entities
    And clicking a result should focus on that entity
    And the highlight should be visually distinct

  @timeline
  Scenario: Timeline filtering with histogram
    Given I have news data spanning multiple days
    When I view the timeline histogram
    Then I should see bars representing article counts per day
    And I can drag the range selectors to filter dates
    And the graph should update to show only entities from selected dates
    And the statistics should reflect the filtered data

  @layout
  Scenario: Graph layout algorithms
    Given I have a complex knowledge graph loaded
    When I switch to "Circular" layout
    Then nodes should be arranged in a circular pattern
    And when I switch to "Hierarchical" layout
    Then nodes should be arranged in a tree structure
    And transitions should be smooth and animated

  @zoom
  Scenario: Graph zoom and pan controls
    Given I have a knowledge graph displayed
    When I click the zoom in button
    Then the graph should scale up proportionally
    And when I click zoom out
    Then the graph should scale down
    And when I click reset zoom
    Then the graph should return to original scale

  @fullscreen
  Scenario: Fullscreen graph exploration
    Given I am viewing a knowledge graph
    When I enter fullscreen mode
    Then the graph should expand to fill the screen
    And the control panel should remain accessible
    And all functionality should work in fullscreen
    And I can exit fullscreen to return to normal view

  @statistics
  Scenario: Real-time graph statistics
    Given I have a knowledge graph with filters applied
    When I toggle entity or relationship filters
    Then the statistics overlay should update immediately
    And show the current count of visible nodes
    And show the current count of visible edges
    And display the timespan of visible articles

  @interaction
  Scenario: Node and edge interaction
    Given I have a rendered knowledge graph
    When I hover over a node
    Then it should highlight with a glow effect
    And show a tooltip with entity information
    And when I click on a node
    Then it should become selected with visual feedback
    And related nodes should be emphasized

  @responsive
  Scenario: Mobile responsive design
    Given I am viewing the graph on a mobile device
    When I open the control panel
    Then it should overlay the full screen
    And touch gestures should work for pan and zoom
    And the interface should remain usable
    And text should be appropriately sized

  @performance
  Scenario: Large graph performance
    Given I have a knowledge graph with 100+ entities
    When I apply filters and layout changes
    Then the interface should remain responsive
    And updates should complete within 2 seconds
    And smooth animations should be maintained
    And memory usage should stay reasonable

  @export
  Scenario: Graph data export
    Given I have a filtered knowledge graph view
    When I request to export the current view
    Then I should be able to save as PNG image
    And export the visible data as JSON
    And generate a Neo4j Cypher file
    And maintain the current filter state

  @persistence
  Scenario: View state persistence
    Given I have configured filters and layout settings
    When I refresh the page or navigate away
    Then my filter preferences should be saved
    And the layout choice should be remembered
    And zoom level should be preserved
    And I can return to my configured view state

  @accessibility
  Scenario: Accessibility features
    Given I am using assistive technology
    When I navigate the graph interface
    Then all controls should be keyboard accessible
    And screen readers should announce graph changes
    And color coding should have alternative indicators
    And zoom levels should be announced