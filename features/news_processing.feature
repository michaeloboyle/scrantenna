Feature: News Processing Pipeline
  As a Scrantenna user
  I want to automatically process news articles about Scranton
  So that I can consume local news in multiple engaging formats

  Background:
    Given the news processing system is initialized
    And the NewsAPI key is configured
    And the output directories exist

  @critical
  Scenario: Successful news ingestion from API
    Given the NewsAPI is responding with valid data
    When I fetch news articles for "Scranton"
    Then I should receive at least 5 articles
    And each article should have a title, description, and publishedAt date
    And the articles should be saved to the daily data directory
    And the JSON structure should be valid

  @error-handling
  Scenario: API failure during news fetching
    Given the NewsAPI is not responding
    When I attempt to fetch news articles
    Then the system should handle the API failure gracefully
    And an error message should be logged
    And the system should not crash
    And previous data should remain intact

  @data-quality
  Scenario: Invalid API response handling
    Given the NewsAPI returns malformed JSON
    When I process the API response
    Then the system should detect the invalid format
    And log an appropriate error message
    And continue processing with available data
    And not corrupt existing data files

  @distillation
  Scenario: Text distillation with LLM
    Given I have a news article with title and description
    And the OpenAI API is available
    When I process the article for distillation
    Then the distilled title should be shorter than the original
    And the distilled content should maintain key facts
    And the distillation method should be recorded
    And the confidence score should be calculated

  @distillation @fallback
  Scenario: Text distillation fallback when LLM unavailable
    Given I have a news article with title and description
    And the OpenAI API is not available
    When I process the article for distillation
    Then the system should use the fallback distillation method
    And still produce a distilled version
    And mark the method as "fallback"
    And maintain processing continuity

  @caching
  Scenario: Efficient data caching
    Given I have processed news articles today
    When I run the news fetching process again
    Then the system should check if data is current
    And avoid redundant API calls if data is fresh
    And only fetch new articles if needed
    And preserve existing processed data

  @validation
  Scenario: Article data validation
    Given I receive articles from the news API
    When I validate each article
    Then articles without titles should be filtered out
    And articles without descriptions should be filtered out
    And articles with very short content should be flagged
    And only valid articles should proceed to processing

  @sentiment
  Scenario: Sentiment analysis processing
    Given I have news articles with content
    When I run sentiment analysis
    Then each article should receive sentiment scores
    And the scores should be between -1 and 1
    And the sentiment data should be saved per article
    And the overall sentiment trend should be calculated

  @rate-limiting
  Scenario: API rate limiting compliance
    Given the NewsAPI has rate limits
    When I make multiple API requests
    Then the system should respect rate limits
    And add appropriate delays between requests
    And not exceed the allowed request frequency
    And handle rate limit responses gracefully

  @data-persistence
  Scenario: Data persistence across runs
    Given I have processed news articles
    When I restart the processing system
    Then previously processed data should be accessible
    And data integrity should be maintained
    And processing should continue from the last state
    And no data should be lost or corrupted