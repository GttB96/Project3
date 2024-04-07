fetch('/historical.html')
  .then(response => response.json())
  .then(data => {
    // Group the data by year and calculate the total electric charging outlets for the USA
    let groupedData = {};
    data.forEach(entry => {
      if (!groupedData[entry.year]) {
        groupedData[entry.year] = 0;
      }
      groupedData[entry.year] += entry.electric_charging_outlets;
    });

    // Extract years and total electric charging outlets for the USA
    let years = Object.keys(groupedData);
    let usaelectriccharginguutlets = Object.values(groupedData);

    // Create a trace object for the line graph
    let trace1 = {
      x: years,
      y: usaelectricchargingoutlets,
      type: 'line',
      mode: 'lines+markers',
      name: 'USA Electric Charging Outlets'
    };

    // Put the trace object in an array
    let data = [trace1];

    // Define the layout
    let layout = {
      title: "Total USA Electric Charging Outlets by Year",
      xaxis: { title: 'Year' },
      yaxis: { title: 'Count' }
    };

    // Create the Plotly line chart
    Plotly.newPlot("plot", data, layout);
  })
  .catch(error => console.error('Error fetching data:', error))
