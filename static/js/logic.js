fetch('/historical.html')
  .then(response => response.json())
  .then(data => {
    // Extract unique states for x-axis
    let states = [...new Set(data.map(entry => entry.state))];

    // Create trace objects for each year
    let traces = [];
    data.forEach(entry => {
      let trace = {
        x: states,
        y: [entry.electric_charging_outlets], // Use the electric charging outlets for y-axis
        type: 'bar',
        name: entry.year
      };
      traces.push(trace);
    });

    // Define the layout
    let layout = {
      title: "Electric Charging Outlets by State",
      xaxis: { title: 'State' },
      yaxis: { title: 'Electric Charging Outlets' },
      barmode: 'group'
    };

    // Create the Plotly bar chart
    Plotly.newPlot("plot", traces, layout);
  })
  .catch(error => console.error('Error fetching data:', error));
