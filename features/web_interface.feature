Feature: Web Interface
  As a news reader
  I want to view Scranton news in a TikTok-style interface
  So that I can quickly consume local news on any device

  Background:
    Given the Scrantenna shorts web application is loaded
    And shorts data is available
    And the interface is responsive and ready

  @critical
  Scenario: Initial shorts loading
    Given I navigate to the shorts viewer
    When the page loads
    Then I should see the first news short displayed
    And the short should have a title and content
    And navigation controls should be visible
    And the format toggle should be available

  @navigation
  Scenario: Swipe navigation on mobile
    Given I am viewing shorts on a mobile device
    When I swipe up on the screen
    Then I should advance to the next short
    And when I swipe down
    Then I should go back to the previous short
    And the transition should be smooth and animated

  @navigation
  Scenario: Keyboard navigation
    Given I am viewing shorts on a desktop
    When I press the down arrow key
    Then I should advance to the next short
    And when I press the up arrow key
    Then I should go to the previous short
    And when I press the spacebar
    Then I should advance to the next short

  @format-toggle
  Scenario: Toggle between original and distilled content
    Given I am viewing a news short
    When I click the format toggle button
    Then the content should switch to distilled format
    And the button should show "Distilled"
    And when I click it again
    Then it should switch back to original format
    And the button should show "Original"

  @view-modes
  Scenario: Switch between text and graph views
    Given I am viewing a news short in text mode
    When I click the view toggle button
    Then I should see the knowledge graph for that article
    And the graph should show entities and relationships
    And when I click the toggle again
    Then I should return to text view

  @auto-advance
  Scenario: Automatic short advancement
    Given I am viewing a news short
    And auto-advance is enabled
    When I wait for 10 seconds without interaction
    Then the interface should automatically advance to the next short
    And the progression should be smooth
    And I can disable auto-advance if desired

  @responsiveness
  Scenario: Responsive design across devices
    Given I view the interface on different screen sizes
    When I load the shorts on a phone
    Then the layout should be optimized for mobile
    And when I load on a tablet
    Then controls should be appropriately sized
    And when I load on desktop
    Then I should have access to all features

  @error-handling
  Scenario: Graceful error handling for missing data
    Given the shorts data file is unavailable
    When I load the web interface
    Then I should see a helpful error message
    And the interface should not crash
    And I should be provided with troubleshooting steps

  @performance
  Scenario: Smooth performance with large datasets
    Given I have 50+ shorts in the dataset
    When I navigate through the shorts rapidly
    Then each transition should complete in under 500ms
    And the interface should remain responsive
    And memory usage should stay stable

  @visual-quality
  Scenario: High-quality visual presentation
    Given I am viewing news shorts
    When I examine the visual design
    Then background gradients should be smooth and appealing
    And text should be clearly readable on all backgrounds
    And animations should be smooth at 60fps
    And the design should feel modern and engaging

  @accessibility
  Scenario: Screen reader compatibility
    Given I am using a screen reader
    When I navigate the shorts interface
    Then the screen reader should announce each short's title
    And describe the current navigation state
    And provide accessible labels for all controls
    And support keyboard-only navigation

  @data-loading
  Scenario: Progressive data loading
    Given I have a large shorts dataset
    When the interface loads
    Then the first few shorts should load immediately
    And additional shorts should load in the background
    And I should be able to start reading immediately
    And loading should not block the interface

  @metadata
  Scenario: Article metadata display
    Given I am viewing a news short
    When I examine the interface
    Then I should see the article source
    And the publication date should be displayed
    And I should see progress through the shorts collection
    And optional metadata should be available

  @sharing
  Scenario: Social sharing capabilities
    Given I am viewing an interesting news short
    When I access sharing options
    Then I should be able to share the specific short
    And the shared link should open to that short
    And metadata should be included for rich previews

  @offline
  Scenario: Offline viewing capability
    Given I have previously loaded shorts
    When I lose internet connectivity
    Then previously loaded shorts should remain viewable
    And navigation should continue to work
    And I should be notified about offline status
    And new shorts should load when connectivity returns

  @customization
  Scenario: User preference customization
    Given I am a regular user of the interface
    When I access preference settings
    Then I should be able to adjust auto-advance timing
    And choose default view mode (text/graph)
    And set default format (original/distilled)
    And these preferences should persist between sessions