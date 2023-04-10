import { Box, colors, Grid, Typography, useTheme } from "@mui/material";
import React from "react";
import BarChart from "../../components/charts/BarChart";
import PieChart from "../../components/charts/PieChart";
import Header from '../../components/global/Header';
import Table_Row from "../../components/charts/Table_Row";
import { tokens } from "../../theme";
import Statsbox from "./Statsbox";

const Dashboard = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const data_for_number = [
    {
      title: "Previous Close",
      number: 5000,
    },
    {
      title: "Previous Close",
      number: 5000,
    },
    {
      title: "Previous Close",
      number: 5000,
    },
    {
      title: "Previous Close",
      number: 5000,
    },
  ];
  React.useEffect(() => {
    console.log(process.env)
  }, [])
  
  return (
    <Box height="80%" width="100%">
      <Box display="flex" flexDirection={"row"} flexWrap={"wrap"}>
        <Statsbox Chart={<PieChart />} />
        <Statsbox Chart={<PieChart />} />
        <Statsbox Chart={<PieChart />} />
      </Box>
      <Grid container spacing={2} wrap="wrap" p={2}>
        <Grid item md={6}>
          <Box
            display="flex"
            flexDirection="column"
            height={"50vh"}
            p={3}
            backgroundColor={colors.primary[400]}
          >
            <Header Header={"Bot: "} SubHeader={"LSTM BiDirectional Model"} />
            <Box height={"50%"}>
              {/* <LineChart /> */}
            </Box>
            <Box m={4}>
              <Table_Row datas={data_for_number} />
            </Box>
          </Box>
        </Grid>
        <Grid item md={6}>
          <Box
            display="flex"
            flexDirection="column"
            height={"50vh"}
            p={3}
            backgroundColor={colors.primary[400]}
          >
            <Header SubHeader={"Bots Overall Performance "} />
            <Box height={"50vh"}>
              <BarChart />
            </Box>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
