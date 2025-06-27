/**
 * Deckset-style Markdown Parser for Scrantenna
 * Parses Deckset presentation directives and formats content for slides
 */

class DecksetParser {
    constructor() {
        this.slideDelimiter = /^---$/gm;
        this.fitPattern = /\[fit\]\s*(.+?)$/gm;
        this.imagePattern = /!\[(.*?)\]\((.*?)\)/g;
        this.notePattern = /^\^\s*(.+?)$/gm;
        this.headerPattern = /^(#{1,6})\s+(.+?)$/gm;
    }

    /**
     * Parse markdown content into slides
     * @param {string} markdown - Raw markdown content
     * @returns {Array} Array of slide objects
     */
    parseMarkdown(markdown) {
        const slides = this.splitIntoSlides(markdown);
        return slides.map((slideMarkdown, index) => this.parseSlide(slideMarkdown, index));
    }

    /**
     * Split markdown content into individual slides
     * @param {string} markdown - Raw markdown content
     * @returns {Array} Array of slide markdown strings
     */
    splitIntoSlides(markdown) {
        return markdown.split(this.slideDelimiter).filter(slide => slide.trim().length > 0);
    }

    /**
     * Parse individual slide markdown
     * @param {string} slideMarkdown - Markdown for single slide
     * @param {number} index - Slide index
     * @returns {Object} Parsed slide object
     */
    parseSlide(slideMarkdown, index) {
        const slide = {
            id: `slide_${index}`,
            index: index,
            raw: slideMarkdown,
            title: '',
            fitText: [],
            content: '',
            images: [],
            notes: [],
            layout: 'center',
            template: 'default'
        };

        // Extract fit text
        slide.fitText = this.extractFitText(slideMarkdown);
        
        // Extract images with positioning
        slide.images = this.extractImages(slideMarkdown);
        
        // Extract presenter notes
        slide.notes = this.extractNotes(slideMarkdown);
        
        // Extract headers and content
        const { title, content } = this.extractContent(slideMarkdown);
        slide.title = title;
        slide.content = content;
        
        // Determine layout based on images
        slide.layout = this.determineLayout(slide.images);
        
        // Determine template based on content structure
        slide.template = this.determineTemplate(slide);

        return slide;
    }

    /**
     * Extract [fit] text directives
     * @param {string} markdown - Slide markdown
     * @returns {Array} Array of fit text strings
     */
    extractFitText(markdown) {
        const fits = [];
        let match;
        
        const fitRegex = /\[fit\]\s*(.+?)$/gm;
        while ((match = fitRegex.exec(markdown)) !== null) {
            fits.push(match[1].trim());
        }
        
        return fits;
    }

    /**
     * Extract image directives with positioning
     * @param {string} markdown - Slide markdown
     * @returns {Array} Array of image objects
     */
    extractImages(markdown) {
        const images = [];
        let match;
        
        const imageRegex = /!\[(.*?)\]\((.*?)\)/g;
        while ((match = imageRegex.exec(markdown)) !== null) {
            const [fullMatch, attributes, url] = match;
            
            const image = {
                url: url.trim(),
                alt: '',
                position: 'background',
                size: 'cover',
                filter: false,
                attributes: attributes.trim()
            };
            
            // Parse image attributes
            this.parseImageAttributes(image, attributes);
            
            images.push(image);
        }
        
        return images;
    }

    /**
     * Parse image positioning and styling attributes
     * @param {Object} image - Image object to modify
     * @param {string} attributes - Attribute string from markdown
     */
    parseImageAttributes(image, attributes) {
        const attrs = attributes.toLowerCase().split(/\s+/);
        
        for (const attr of attrs) {
            switch (attr) {
                case 'left':
                    image.position = 'left';
                    break;
                case 'right':
                    image.position = 'right';
                    break;
                case 'inline':
                    image.position = 'inline';
                    break;
                case 'fit':
                    image.size = 'fit';
                    break;
                case 'original':
                    image.size = 'original';
                    break;
                case 'filtered':
                    image.filter = true;
                    break;
                default:
                    // Check for percentage sizes
                    const percentMatch = attr.match(/^(\d+)%$/);
                    if (percentMatch) {
                        image.size = percentMatch[1] + '%';
                    } else if (attr.length > 0) {
                        image.alt = attr;
                    }
            }
        }
    }

    /**
     * Extract presenter notes (lines starting with ^)
     * @param {string} markdown - Slide markdown
     * @returns {Array} Array of note strings
     */
    extractNotes(markdown) {
        const notes = [];
        let match;
        
        const noteRegex = /^\^\s*(.+?)$/gm;
        while ((match = noteRegex.exec(markdown)) !== null) {
            notes.push(match[1].trim());
        }
        
        return notes;
    }

    /**
     * Extract title and content from markdown
     * @param {string} markdown - Slide markdown
     * @returns {Object} Object with title and content
     */
    extractContent(markdown) {
        // Remove fit directives, images, and notes for clean content
        let cleanMarkdown = markdown
            .replace(/\[fit\]\s*(.+?)$/gm, '') // Remove fit directives
            .replace(/!\[(.*?)\]\((.*?)\)/g, '') // Remove images
            .replace(/^\^\s*(.+?)$/gm, '') // Remove notes
            .trim();

        const lines = cleanMarkdown.split('\n').filter(line => line.trim().length > 0);
        
        let title = '';
        let content = '';
        let foundTitle = false;
        
        for (const line of lines) {
            const trimmed = line.trim();
            
            // Check for headers
            const headerMatch = trimmed.match(/^(#{1,6})\s+(.+)$/);
            if (headerMatch && !foundTitle) {
                title = headerMatch[2].trim();
                foundTitle = true;
            } else if (trimmed.length > 0) {
                content += (content ? '\n' : '') + trimmed;
            }
        }
        
        return { title, content };
    }

    /**
     * Determine slide layout based on images
     * @param {Array} images - Array of image objects
     * @returns {string} Layout type
     */
    determineLayout(images) {
        if (images.length === 0) return 'center';
        
        const positions = images.map(img => img.position);
        
        if (positions.includes('left')) return 'left';
        if (positions.includes('right')) return 'right';
        if (positions.includes('inline')) return 'inline';
        
        return 'background';
    }

    /**
     * Determine slide template based on content structure
     * @param {Object} slide - Slide object
     * @returns {string} Template type
     */
    determineTemplate(slide) {
        if (slide.fitText.length > 0 && slide.images.length > 0) {
            return 'headline';
        } else if (slide.images.length > 0 && slide.content.length < 100) {
            return 'visual';
        } else if (slide.content.includes('*') || slide.content.includes('-')) {
            return 'breakdown';
        } else {
            return 'default';
        }
    }

    /**
     * Convert news article to Deckset-style markdown
     * @param {Object} article - News article object
     * @param {string} template - Template type
     * @returns {string} Deckset markdown
     */
    articleToMarkdown(article, template = 'headline') {
        const title = article.title_distilled || article.title || 'News Update';
        const content = article.description || article.content || '';
        const image = article.urlToImage || '';
        const source = article.source?.name || article.source || 'Unknown';
        const date = new Date(article.publishedAt).toLocaleDateString();

        switch (template) {
            case 'headline':
                return this.createHeadlineSlide(title, content, image, source, date);
            case 'visual':
                return this.createVisualSlide(title, content, image, source, date);
            case 'breakdown':
                return this.createBreakdownSlide(title, content, image, source, date);
            default:
                return this.createDefaultSlide(title, content, image, source, date);
        }
    }

    /**
     * Create headline template slide
     * @param {string} title - Article title
     * @param {string} content - Article content
     * @param {string} image - Image URL
     * @param {string} source - News source
     * @param {string} date - Publication date
     * @returns {string} Markdown for headline slide
     */
    createHeadlineSlide(title, content, image, source, date) {
        const fitText = this.extractKeywords(title);
        
        return `# [fit] **${fitText}**

${image ? `![right filtered](${image})` : ''}

## ${source}
### ${date}

${this.truncateContent(content, 150)}

^ Source: ${source}
^ Published: ${date}
^ ${content}`;
    }

    /**
     * Create visual template slide
     * @param {string} title - Article title
     * @param {string} content - Article content
     * @param {string} image - Image URL
     * @param {string} source - News source
     * @param {string} date - Publication date
     * @returns {string} Markdown for visual slide
     */
    createVisualSlide(title, content, image, source, date) {
        const fitText = this.extractKeywords(title);
        
        return `${image ? `![filtered](${image})` : ''}

# [fit] **${fitText}**

^ Source: ${source}
^ Published: ${date}
^ ${content}`;
    }

    /**
     * Create breakdown template slide
     * @param {string} title - Article title
     * @param {string} content - Article content
     * @param {string} image - Image URL
     * @param {string} source - News source
     * @param {string} date - Publication date
     * @returns {string} Markdown for breakdown slide
     */
    createBreakdownSlide(title, content, image, source, date) {
        const bullets = this.extractBulletPoints(content);
        
        return `${image ? `![left filtered](${image})` : ''}

# ${title}

${bullets.map(bullet => `* ${bullet}`).join('\n')}

^ Source: ${source}
^ Published: ${date}
^ Full content: ${content}`;
    }

    /**
     * Create default template slide
     * @param {string} title - Article title
     * @param {string} content - Article content
     * @param {string} image - Image URL
     * @param {string} source - News source
     * @param {string} date - Publication date
     * @returns {string} Markdown for default slide
     */
    createDefaultSlide(title, content, image, source, date) {
        return `# ${title}

${image ? `![](${image})` : ''}

${content}

---

**${source}** • ${date}

^ ${content}`;
    }

    /**
     * Extract keywords for [fit] text
     * @param {string} title - Article title
     * @returns {string} Keywords for fit text
     */
    extractKeywords(title) {
        const words = title.split(' ');
        const stopWords = ['the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'];
        
        const keywords = words.filter(word => 
            word.length > 3 && 
            !stopWords.includes(word.toLowerCase())
        );
        
        // Take first 2-3 keywords or fallback to first few words
        return keywords.length > 0 
            ? keywords.slice(0, 3).join(' ')
            : words.slice(0, 3).join(' ');
    }

    /**
     * Extract bullet points from content
     * @param {string} content - Article content
     * @returns {Array} Array of bullet points
     */
    extractBulletPoints(content) {
        // Split content into sentences and take key points
        const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 10);
        
        // Take first 3-4 sentences as bullet points
        return sentences.slice(0, 4).map(s => s.trim());
    }

    /**
     * Truncate content to specified length
     * @param {string} content - Content to truncate
     * @param {number} maxLength - Maximum length
     * @returns {string} Truncated content
     */
    truncateContent(content, maxLength = 200) {
        if (content.length <= maxLength) return content;
        
        const truncated = content.substring(0, maxLength);
        const lastSpace = truncated.lastIndexOf(' ');
        
        return lastSpace > 0 
            ? truncated.substring(0, lastSpace) + '…'
            : truncated + '…';
    }

    /**
     * Generate presentation from multiple articles
     * @param {Array} articles - Array of news articles
     * @param {Object} options - Generation options
     * @returns {string} Complete presentation markdown
     */
    generatePresentation(articles, options = {}) {
        const {
            template = 'mixed',
            title = 'Scrantenna News Update',
            subtitle = 'Local News Digest',
            includeTitle = true
        } = options;

        let presentation = '';

        // Add title slide if requested
        if (includeTitle) {
            presentation += `# [fit] **${title}**
## ${subtitle}

---

`;
        }

        // Generate slides for each article
        articles.forEach((article, index) => {
            const slideTemplate = template === 'mixed' 
                ? ['headline', 'visual', 'breakdown'][index % 3]
                : template;
            
            const slideMarkdown = this.articleToMarkdown(article, slideTemplate);
            presentation += slideMarkdown;
            
            // Add separator between slides
            if (index < articles.length - 1) {
                presentation += '\n\n---\n\n';
            }
        });

        return presentation;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DecksetParser;
}

// Global access for browser usage
if (typeof window !== 'undefined') {
    window.DecksetParser = DecksetParser;
}

// Usage example:
/*
const parser = new DecksetParser();

// Parse existing markdown
const slides = parser.parseMarkdown(markdownContent);

// Convert article to slide
const slideMarkdown = parser.articleToMarkdown(newsArticle, 'headline');

// Generate full presentation
const presentation = parser.generatePresentation(articles, {
    template: 'mixed',
    title: 'Weekly News Digest',
    includeTitle: true
});
*/