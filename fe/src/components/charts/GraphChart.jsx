import React from "react";
import Chart from "react-apexcharts";
const GraphChart = ({ datas }) => {
  const points = [];
  // Make sure that it filters out those that dun have signal
  const filtered_data = datas.map((each_stock) =>
    each_stock.filter((stock) => stock.signal ? Math.abs(stock.signal) > 1:false)
  );
  filtered_data.map((each_stock) =>
    each_stock.map((indicator) => {
      points.push({
        x: new Date(indicator.Date).getTime(),
        y: indicator.Close,
        marker: {
          size: 8,
          fillColor: indicator.signal < 0 ? "red" : "green",
          strokeColor: "black",
          shape: "circle",
        },
        
      });
    })
  );

  const data = datas.map((each_stock) => {
    return {
      data: each_stock.map((point) => ({
        x: new Date(point.Date).getTime(),
        y: point.Close ? point.Close:null,
      })),
    };
  });
  console.log(data)
  const state = {
    options: {
      chart: {
        background: "#fff",
        type: "line",
      },
      xaxis: {
        type: "datetime",
      },
      annotations: {
        points: points,
      },
    },
    series: data,
  };
  return <Chart options={state.options} series={state.series} width="100%" height={'100%'}/>;
};

export default GraphChart;
