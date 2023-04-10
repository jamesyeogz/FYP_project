import { Grid, Typography } from "@mui/material";
import React from "react";

const Table_Row = ({ datas }) => {
    console.log(datas)
  return (
    <Grid container spacing={2} pr={4} pl={4} >
      {datas.map((data,index) => (
        <Grid item xs={6} p={2} display="flex" flexDirection="row" justifyContent="space-between" key={index}>
          <Typography variant="h4">{data.title}</Typography>
          <Typography variant="h4">{data.number}</Typography>
        </Grid>
      ))}
    </Grid>
  );
};

export default Table_Row;
