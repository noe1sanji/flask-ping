window.addEventListener("load", function () {
  const ctx = document.getElementById("myChart");

  fetch("http://127.0.0.1:5000/api/metrics/1")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP Error, status = ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      const metrics = [];
      for (const row of data) {
        metrics.push(
          { "timestamp": row.timestamp, "response_time": row.response_time },
        );
      }
      new Chart(ctx, {
        type: "line",
        data: {
          datasets: [{
            data: metrics,
          }],
        },
        options: {
          plugins: {
            legend: {
              display: false,
            },
          },
          parsing: {
            xAxisKey: "timestamp",
            yAxisKey: "response_time",
          },
        },
      });
    })
    .catch((error) => {
      console.error(error);
    });
});
