Feature: Shorts Generation
  As a content consumer
  I want news articles transformed into TikTok-style shorts
  So that I can quickly consume local news in an engaging format

  Background:
    Given processed news articles exist in the daily data directory
    And the shorts generation system is initialized
    And the output directory for shorts is available

  @critical
  Scenario: Generate shorts from processed news
    Given I have 15 processed news articles
    When I run the shorts generation process
    Then I should get exactly 15 shorts
    And each short should have an original and distilled version
    And each short should have a unique background gradient
    And the shorts should be ordered by publication date
    And the total duration should be calculated correctly

  @entity-extraction
  Scenario: Entity extraction with free LLM
    Given I have a news article about local politics
    And the Ollama service is available
    When I extract entities from the article
    Then I should identify person entities like "Mayor Cognetti"
    And location entities like "Scranton" and "Pennsylvania"
    And organization entities like "City Hall"
    And the entities should have confidence scores
    And the extraction method should be recorded

  @entity-extraction @fallback
  Scenario: Entity extraction fallback chain
    Given I have a news article for entity extraction
    And Ollama is not available
    And HuggingFace transformers is not available
    When I run entity extraction
    Then the system should use rule-based extraction
    And still identify basic entities
    And mark the method as "rule_based"
    And not fail the shorts generation process

  @graph-generation
  Scenario: Knowledge graph generation
    Given I have extracted entities and relationships
    When I generate the knowledge graph
    Then I should get a valid SVG representation
    And the SVG should contain circle elements for entities
    And the SVG should contain line elements for relationships
    And entity colors should correspond to their types
    And the graph should be properly sized for display

  @visual-design
  Scenario: Shorts visual design
    Given I have news articles for shorts generation
    When I create the shorts
    Then each short should have a unique gradient background
    And the gradients should cycle through the color palette
    And text should be properly sized for mobile viewing
    And animations should be properly timed
    And the design should be responsive

  @data-structure
  Scenario: Shorts JSON structure validation
    Given I generate shorts from news articles
    When I examine the output JSON structure
    Then it should contain metadata about generation time
    And it should include the source file reference
    And it should have the correct total count
    And each short should have all required fields
    And the JSON should be valid and parseable

  @performance
  Scenario: Shorts generation performance
    Given I have 50 news articles to process
    When I run shorts generation
    Then the process should complete in under 2 minutes
    And memory usage should remain under 1GB
    And the output files should be properly closed
    And no temporary files should be left behind

  @caching
  Scenario: Shorts generation caching
    Given I have already generated shorts today
    When I run shorts generation again without new articles
    Then the system should detect that shorts are current
    And skip regeneration to save processing time
    And use the existing shorts data
    And only regenerate if forced with --force flag

  @content-quality
  Scenario: Content quality validation
    Given I have articles with varying content quality
    When I filter articles for shorts generation
    Then articles without titles should be excluded
    And articles without descriptions should be excluded
    And articles with very short content should be excluded
    And only high-quality articles should become shorts

  @multi-format
  Scenario: Multiple content format support
    Given I have processed news articles
    When I generate shorts
    Then each short should include the original text
    And each short should include the distilled version
    And each short should include an embedded knowledge graph
    And users should be able to toggle between formats
    And all formats should be generated simultaneously

  @integration
  Scenario: Integration with web viewer
    Given I have generated shorts data
    When the web viewer loads the shorts
    Then it should parse the JSON successfully
    And display the correct number of shorts
    And allow navigation between shorts
    And support format toggling
    And render knowledge graphs properly

  @error-recovery
  Scenario: Error recovery during generation
    Given I have some corrupted articles in the dataset
    When I run shorts generation
    Then the system should skip corrupted articles
    And log appropriate error messages
    And continue processing valid articles
    And produce shorts for all valid articles
    And not crash the entire process