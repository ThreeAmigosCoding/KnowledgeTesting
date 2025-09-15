// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
import { useRef, useEffect } from 'react';
import * as d3 from 'd3';
import {useTheme} from "@mui/material";


export default function KnowledgeGraph ({nodes, links}) {
    const svgRef = useRef();
    const theme = useTheme();
    let hasZoomed = false;

    useEffect(() => {
        const svg = d3.select(svgRef.current)
            .attr("width", "100%")
            .attr("height", "100%");

        svg.append("defs").selectAll("marker")
            .data(links)
            .enter()
            .append("marker")
            .attr("id", (d) => `arrow-${d.id}`)
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 8)
            .attr("refY", 0)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("path")
            .attr("d", "M0,-5L10,0L0,5")
            .attr("fill", d => d.color);

        const g = svg.append("g");

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.title).distance(200))
            .force("charge", d3.forceManyBody().strength(-1000))
            .force("center", d3.forceCenter(svgRef.current.clientWidth / 2, svgRef.current.clientHeight / 2));


        const nodeGroup = g.append("g")
            .selectAll("g")
            .data(nodes)
            .enter()
            .append("g")
            .call(drag(simulation));

        const labels = nodeGroup.append("text")
            .attr("text-anchor", "middle")
            .text(d => d.title)
            .attr("font-size", "18px")
            .attr("fill", theme.palette.primary.contrastText)
            .attr("dy", ".30em");
        console.log(labels)

        nodeGroup.each(function(d) {
            const textElement = d3.select(this).select("text");
            const { width, height } = textElement.node().getBBox();
            d.bboxWidth = width + 30;
            d.bboxHeight = height + 20;
        });

        nodeGroup.insert("rect", "text")
            .attr("width", d => d.bboxWidth)
            .attr("height", d => d.bboxHeight)
            .attr("x", d => -d.bboxWidth / 2)
            .attr("y", d => -d.bboxHeight / 2)
            .attr("fill", d => d.color)
            .attr("rx", 5)
            .attr("ry", 5);

        nodeGroup.append("title")
            .text(d => d.questionText ? `Question: ${d.questionText}` : "No associated question");

        const link = g.append("g")
            .selectAll("line")
            .data(links)
            .enter()
            .append("line")
            .attr("stroke", e => e.color)
            .attr("stroke-width", 2)
            .attr("marker-end", (d) => `url(#arrow-${d.id})`);

        const initialZoom = ()=> {
            const bounds = g.node().getBBox();
            const fullWidth = svgRef.current.clientWidth;
            const fullHeight = svgRef.current.clientHeight;
            const width = bounds.width;
            const height = bounds.height;
            const midX = bounds.x + width / 2;
            const midY = bounds.y + height / 2;

            const scale = 0.8 / Math.max(width / fullWidth, height / fullHeight);
            const transform = d3.zoomIdentity
                .translate(fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY)
                .scale(scale);

            svg.call(zoom.transform, transform);
        }
        simulation.on("tick", () => {
            link.each(function(d) {
                const { x1, y1, x2, y2 } = getEdgeCoordinates(d.source, d.target);
                d3.select(this)
                    .attr("x1", x1)
                    .attr("y1", y1)
                    .attr("x2", x2)
                    .attr("y2", y2);
            });

            nodeGroup
                .attr("transform", d => `translate(${d.x},${d.y})`);

            if (!hasZoomed) {
                initialZoom();
                hasZoomed = true;
            }
        });

        const zoom = d3.zoom()
            .scaleExtent([0.1, 5]) // Set zoom range
            .on("zoom", (event) => {
                g.attr("transform", event.transform);
            });

        svg.call(zoom);

        return () => {
            svg.selectAll('*').remove();
            simulation.stop();
        };

    }, [nodes, links]);

    const drag = simulation => {

        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        function dragended(event, d) {
            //if (!event.active) simulation.alphaTarget(0);
            console.log(event, d);
        }

        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }

    function getEdgeCoordinates(source, target) {
        const dx = target.x - source.x;
        const dy = target.y - source.y;
        const angle = Math.atan2(dy, dx);

        const sourceHalfWidth = source.bboxWidth / 2;
        const sourceHalfHeight = source.bboxHeight / 2;
        const targetHalfWidth = target.bboxWidth / 2;
        const targetHalfHeight = target.bboxHeight / 2;

        const x1 = source.x + sourceHalfWidth * Math.cos(angle);
        const y1 = source.y + sourceHalfHeight * Math.sin(angle);

        const x2 = target.x - targetHalfWidth * Math.cos(angle);
        const y2 = target.y - targetHalfHeight * Math.sin(angle);

        return { x1, y1, x2, y2 };
    }



    return (<svg ref={svgRef}></svg>);
};