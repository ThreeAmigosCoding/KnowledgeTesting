import { useRef, useEffect } from 'react';
import * as d3 from 'd3';
import {useTheme} from "@mui/material";

export default function KnowledgeGraph ({nodes, links}) {
    const svgRef = useRef();
    const theme = useTheme();

    useEffect(() => {
        const svg = d3.select(svgRef.current)
            .attr("width", "100%")
            .attr("height", "100%");

        svg.append("defs").append("marker")
            .attr("id", "arrow")
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 8)
            .attr("refY", 0)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("path")
            .attr("d", "M0,-5L10,0L0,5")
            .attr("fill", "#040303");

        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.title).distance(150))
            .force("charge", d3.forceManyBody().strength(-200))
            .force("center", d3.forceCenter(400, 300));


        const nodeGroup = svg.append("g")
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
            .attr("fill", theme.palette.primary.main)
            .attr("rx", 5)
            .attr("ry", 5);

        const link = svg.append("g")
            .selectAll("line")
            .data(links)
            .enter()
            .append("line")
            .attr("stroke", theme.palette.secondary.contrastText)
            .attr("stroke-width", 2)
            .attr("marker-end", "url(#arrow)");

        // Ažuriraj pozicije tokom simulacije
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
        });

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
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
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