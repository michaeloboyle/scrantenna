// Graph Visualization Module for Scrantenna Shorts
export class GraphManager {
    constructor() {
        this.graphEngaged = false;
        this.onEntityClick = null;
    }

    // Generate avatar URL using DiceBear API for consistent person images
    generateAvatarUrl(name) {
        const cleanName = name.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
        return `https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(cleanName)}&backgroundColor=2563eb,7c3aed,dc2626,059669,ea580c&fontFamily=Arial&fontSize=40`;
    }

    async loadGraphForArticle(index, article) {
        const graphContainer = document.getElementById(`graph-${index}`);
        
        if (!graphContainer) {
            console.error(`Graph container graph-${index} not found`);
            return;
        }
        
        graphContainer.style.width = '100%';
        graphContainer.style.height = '100%';
        
        try {
            console.log(`Loading graph for article ${index}:`, article.title);
            
            if (article.graph && article.graph.entities) {
                console.log('Using embedded graph data with Vis.js');
                this.createVisJsGraph(graphContainer, article.graph, index);
            } else {
                console.log('Generating fallback graph');
                const entities = this.extractSimpleEntities(`${article.title || ''} ${article.description || article.content || ''}`);
                const relationships = this.extractSimpleRelationships(`${article.title || ''} ${article.description || article.content || ''}`, entities);
                
                this.createVisJsGraph(graphContainer, {
                    entities: entities,
                    relationships: relationships
                }, index);
            }
        } catch (error) {
            console.error('Graph loading failed:', error);
            graphContainer.innerHTML = `<p style="color: white;">Graph loading failed: ${error.message}</p>`;
        }
    }

    createVisJsGraph(container, graphData, currentShort) {
        container.innerHTML = '';
        
        if (!graphData || !graphData.entities || graphData.entities.length === 0) {
            container.innerHTML = '<p style="color: white; text-align: center; padding: 20px;">No entities found</p>';
            return;
        }

        const nodeCount = graphData.entities.length;
        const useCircular = nodeCount <= 8;
        
        const nodes = new vis.DataSet(
            graphData.entities.map((entity, index) => {
                let position = {};
                
                if (useCircular) {
                    const radius = Math.min(150, 50 + nodeCount * 15);
                    const angle = (2 * Math.PI * index) / nodeCount;
                    position = {
                        x: radius * Math.cos(angle),
                        y: radius * Math.sin(angle),
                        fixed: { x: true, y: true }
                    };
                }
                
                let nodeConfig = {
                    id: index,
                    label: '',
                    group: entity.type,
                    title: `${entity.type}: ${entity.name} - Click to highlight connections`,
                    borderWidth: 3,
                    borderWidthSelected: 5,
                    size: 35,
                    shadow: {
                        enabled: true,
                        color: 'rgba(0,0,0,0.5)',
                        size: 8,
                        x: 2,
                        y: 2
                    },
                    ...position
                };

                if (entity.type === 'PERSON') {
                    nodeConfig.shape = 'circularImage';
                    nodeConfig.image = this.generateAvatarUrl(entity.name);
                    nodeConfig.size = 40;
                    nodeConfig.borderWidth = 4;
                }

                return nodeConfig;
            })
        );

        const edges = new vis.DataSet(
            (graphData.relationships || []).map(rel => {
                const fromIndex = graphData.entities.findIndex(e => e.name === rel.from);
                const toIndex = graphData.entities.findIndex(e => e.name === rel.to);
                
                if (fromIndex !== -1 && toIndex !== -1) {
                    return {
                        from: fromIndex,
                        to: toIndex,
                        label: rel.type.replace(/_/g, ' '),
                        arrows: { to: { enabled: true, scaleFactor: 1.2 } },
                        font: { 
                            color: 'white', 
                            size: 12,
                            strokeWidth: 2,
                            strokeColor: 'black',
                            face: 'Arial'
                        },
                        color: { 
                            color: 'rgba(255,255,255,0.9)',
                            highlight: 'rgba(255,215,0,1)',
                            hover: 'rgba(255,255,255,1)'
                        },
                        width: 2,
                        smooth: {
                            type: 'curvedCW',
                            roundness: 0.2
                        },
                        shadow: {
                            enabled: true,
                            color: 'rgba(0,0,0,0.3)',
                            size: 5
                        }
                    };
                }
                return null;
            }).filter(edge => edge !== null)
        );

        const options = this.getGraphOptions(useCircular);
        const data = { nodes: nodes, edges: edges };
        const network = new vis.Network(container, data, options);

        this.setupNetworkInteractions(network, graphData, nodes, edges, currentShort);
    }

    getGraphOptions(useCircular) {
        return {
            nodes: {
                shape: 'dot',
                size: 30,
                borderWidth: 3,
                shadow: {
                    enabled: true,
                    color: 'rgba(0,0,0,0.5)',
                    size: 8
                },
                font: {
                    color: 'white',
                    size: 12,
                    face: 'Arial',
                    strokeWidth: 2,
                    strokeColor: 'black'
                },
                chosen: {
                    node: function(values, id, selected, hovering) {
                        values.shadow = true;
                        values.shadowColor = 'rgba(255,215,0,0.8)';
                        values.shadowSize = 15;
                    }
                }
            },
            groups: {
                PERSON: { 
                    color: { 
                        background: '#FF6B6B', 
                        border: '#E85A5A',
                        highlight: { background: '#FF5252', border: '#D32F2F' }
                    } 
                },
                ORGANIZATION: { 
                    color: { 
                        background: '#4ECDC4', 
                        border: '#26A69A',
                        highlight: { background: '#26C6DA', border: '#00838F' }
                    } 
                },
                LOCATION: { 
                    color: { 
                        background: '#45B7D1', 
                        border: '#2E95B1',
                        highlight: { background: '#35A7C1', border: '#1E85A1' }
                    } 
                },
                WORK: { 
                    color: { 
                        background: '#9C27B0', 
                        border: '#7C1B90',
                        highlight: { background: '#8C17A0', border: '#6C0B80' }
                    } 
                },
                EVENT: { 
                    color: { 
                        background: '#AB47BC', 
                        border: '#8B279C',
                        highlight: { background: '#9B37AC', border: '#7B178C' }
                    } 
                },
                OTHER: { 
                    color: { 
                        background: '#78909C', 
                        border: '#58707C',
                        highlight: { background: '#68808C', border: '#48606C' }
                    } 
                }
            },
            physics: {
                enabled: !useCircular,
                stabilization: { iterations: 100 },
                barnesHut: {
                    gravitationalConstant: -8000,
                    centralGravity: 0.3,
                    springLength: 95,
                    springConstant: 0.04,
                    damping: 0.09,
                    avoidOverlap: 0.1
                }
            },
            interaction: {
                hover: true,
                selectConnectedEdges: true,
                dragNodes: !useCircular,
                zoomView: true,
                dragView: true,
                tooltipDelay: 200
            },
            layout: {
                randomSeed: 42,
                improvedLayout: !useCircular
            }
        };
    }

    setupNetworkInteractions(network, graphData, nodes, edges, currentShort) {
        network.on("click", (params) => {
            this.markGraphEngaged();
            
            if (params.nodes.length > 0) {
                const nodeId = params.nodes[0];
                const entity = graphData.entities[nodeId];
                const connectedNodes = network.getConnectedNodes(nodeId);
                const connectedEdges = network.getConnectedEdges(nodeId);
                
                this.showEntityInfo(entity, currentShort);
                this.highlightConnections(nodes, edges, nodeId, connectedNodes, connectedEdges);
            } else {
                this.hideEntityInfo(currentShort);
                this.resetHighlighting(nodes, edges, graphData);
            }
        });

        network.on("click", (params) => {
            if (params.nodes.length === 0) {
                this.resetHighlighting(nodes, edges, graphData);
            }
        });
    }

    showEntityInfo(entity, currentShort) {
        const entityInfo = document.getElementById(`entity-info-${currentShort}`);
        const entityName = document.getElementById(`entity-name-${currentShort}`);
        const entityType = document.getElementById(`entity-type-${currentShort}`);
        
        if (entityInfo && entityName && entityType && entity) {
            entityName.textContent = entity.name;
            entityType.textContent = entity.type;
            entityInfo.classList.add('visible');
        }
    }

    hideEntityInfo(currentShort) {
        const entityInfo = document.getElementById(`entity-info-${currentShort}`);
        if (entityInfo) {
            entityInfo.classList.remove('visible');
        }
    }

    highlightConnections(nodes, edges, nodeId, connectedNodes, connectedEdges) {
        const updateArray = [];
        nodes.forEach((node) => {
            const isPerson = node.group === 'PERSON';
            const baseSize = isPerson ? 40 : 35;
            
            if (connectedNodes.indexOf(node.id) !== -1 || node.id === nodeId) {
                updateArray.push({
                    id: node.id,
                    opacity: 1,
                    size: baseSize * 1.2
                });
            } else {
                updateArray.push({
                    id: node.id,
                    opacity: 0.3,
                    size: baseSize * 0.8
                });
            }
        });
        
        nodes.update(updateArray);
        
        const edgeUpdateArray = [];
        edges.forEach((edge) => {
            if (connectedEdges.indexOf(edge.id) !== -1) {
                edgeUpdateArray.push({
                    id: edge.id,
                    color: { color: '#FFD700', opacity: 1 },
                    width: 4
                });
            } else {
                edgeUpdateArray.push({
                    id: edge.id,
                    color: { color: 'rgba(255,255,255,0.2)', opacity: 0.2 },
                    width: 1
                });
            }
        });
        
        edges.update(edgeUpdateArray);
    }

    resetHighlighting(nodes, edges, graphData) {
        const resetNodes = nodes.map(node => {
            const isPerson = node.group === 'PERSON';
            return {
                id: node.id,
                opacity: 1,
                size: isPerson ? 40 : 35
            };
        });
        
        const resetEdges = edges.map(edge => ({
            id: edge.id,
            color: { color: 'rgba(255,255,255,0.9)', opacity: 0.8 },
            width: 2
        }));
        
        nodes.update(resetNodes);
        edges.update(resetEdges);
    }

    markGraphEngaged() {
        this.graphEngaged = true;
        if (this.onEntityClick) {
            this.onEntityClick();
        }
    }

    // Simple entity extraction for fallback
    extractSimpleEntities(text) {
        const entities = [];
        const patterns = [
            { pattern: /\b([A-Z][a-z]+ [A-Z][a-z]+)\b/g, type: 'PERSON' },
            { pattern: /\b(Scranton|Pennsylvania|PA)\b/g, type: 'LOCATION' },
            { pattern: /\b([A-Z][a-z]+ (?:Department|Office|Service|Agency))\b/g, type: 'ORGANIZATION' }
        ];

        patterns.forEach(({ pattern, type }) => {
            let match;
            while ((match = pattern.exec(text)) !== null) {
                entities.push({ name: match[1], type });
            }
        });

        return entities.slice(0, 8);
    }

    extractSimpleRelationships(text, entities) {
        const relationships = [];
        const verbPatterns = [
            'announced', 'said', 'stated', 'issued', 'released'
        ];

        verbPatterns.forEach(verb => {
            const pattern = new RegExp(`([A-Z][a-z]+ [A-Z][a-z]+)\\s+${verb}\\s+([a-z]+)`, 'gi');
            let match;
            while ((match = pattern.exec(text)) !== null) {
                const from = entities.find(e => e.name === match[1]);
                if (from) {
                    relationships.push({
                        from: from.name,
                        to: match[2],
                        type: verb.toUpperCase()
                    });
                }
            }
        });

        return relationships.slice(0, 5);
    }
}