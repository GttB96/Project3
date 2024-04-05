fetch('/historical.html')
  .then(response => response.json())
  .then(data => {
    // Extract unique years from the data
    let years = [...new Set(data.map(entry => entry.year))];

    // Create a bar chart for each year
    years.forEach(year => {
      // Filter the data for the current year
      let filteredData = data.filter(entry => entry.year === year);
      
      // Extract states and electric charging outlets for the current year
      let states = filteredData.map(entry => entry.state);
      let electricChargingOutlets = filteredData.map(entry => entry.electric_charging_outlets);

      // Create a trace object for the bar chart
      let trace = {
        x: states,
        y: electricChargingOutlets,
        type: 'bar',
        name: `Electric Charging Outlets ${year}`
      };

      // Put the trace object in an array
      let data = [trace];

      // Define the layout
      let layout = {
        title: `Electric Charging Outlets Count by State for ${year}`,
        xaxis: { title: 'State' },
        yaxis: { title: 'Electric Charging Outlets Count' }
      };

      // Create the Plotly bar chart
      Plotly.newPlot(`plot-${year}`, data, layout);
    });
  })
  .catch(error => console.error('Error fetching data:', error));
