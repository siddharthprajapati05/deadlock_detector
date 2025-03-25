function runBankersAlgorithm() {
    try {
        let allocation = JSON.parse(document.getElementById("allocation").value);
        let maximum = JSON.parse(document.getElementById("maximum").value);
        let available = JSON.parse(document.getElementById("available").value);

        fetch("/bankers", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ allocation, maximum, available })
        })
        .then(response => response.json())
        .then(data => {
            let resultElement = document.getElementById("result");

            if (data.safe) {
                resultElement.innerHTML = `✅ Safe State. Safe Sequence: ${data.sequence.map(p => `P${p}`).join(" → ")}`;
                resultElement.style.color = "green";
                drawSafeSequenceGraph(data.sequence.map(p => `P${p}`));
            } else if (data.partial_sequence.length > 0) {
                resultElement.innerHTML = `⚠️ Unsafe State! Partial Safe Sequence: ${data.partial_sequence.map(p => `P${p}`).join(" → ")}`;
                resultElement.style.color = "orange";
                drawSafeSequenceGraph(data.partial_sequence.map(p => `P${p}`));
            } else {
                resultElement.innerHTML = "❌ Deadlock detected. No safe sequence possible.";
                resultElement.style.color = "red";
            }
        })
        .catch(error => alert("Error processing request! Check JSON format."));
    } catch (error) {
        alert("Invalid input format! Please enter matrices in correct JSON format.");
    }
}

// Function to clear all input fields and reset the result
function clearFields() {
    document.getElementById("allocation").value = "";
    document.getElementById("maximum").value = "";
    document.getElementById("available").value = "";
    document.getElementById("result").innerHTML = "";
    document.getElementById("graph").innerHTML = "";
}

// Function to draw the safe sequence graph
function drawSafeSequenceGraph(sequence) {
    d3.select("#graph").html(""); // Clear previous graph before drawing

    let width = 600, height = 200;
    let svg = d3.select("#graph").append("svg")
                .attr("width", width)
                .attr("height", height);

    let nodes = sequence.map((p, index) => ({ id: p, x: (index + 1) * 100, y: 100 }));
    let links = sequence.slice(0, -1).map((p, i) => ({ source: p, target: sequence[i + 1] }));

    let nodeMap = new Map(nodes.map(node => [node.id, node])); // Ensure node existence

    let simulation = d3.forceSimulation(nodes)
        .force("link", d3.forceLink(links)
                         .id(d => d.id)
                         .distance(100))
        .force("charge", d3.forceManyBody().strength(-300))
        .force("center", d3.forceCenter(width / 2, height / 2));

    let link = svg.selectAll("line")
        .data(links)
        .enter()
        .append("line")
        .style("stroke", "#000")
        .style("stroke-width", 2);

    let node = svg.selectAll("circle")
        .data(nodes)
        .enter()
        .append("circle")
        .attr("r", 20)
        .attr("fill", "steelblue");

    let text = svg.selectAll("text")
        .data(nodes)
        .enter()
        .append("text")
        .text(d => d.id)
        .attr("font-size", "14px")
        .attr("dx", -10)
        .attr("dy", 5)
        .style("fill", "white");

    simulation.on("tick", () => {
        link.attr("x1", d => nodeMap.get(d.source.id).x)
            .attr("y1", d => nodeMap.get(d.source.id).y)
            .attr("x2", d => nodeMap.get(d.target.id).x)
            .attr("y2", d => nodeMap.get(d.target.id).y);

        node.attr("cx", d => d.x).attr("cy", d => d.y);
        text.attr("x", d => d.x).attr("y", d => d.y);
    });

    simulation.force("link").links(links);
}
