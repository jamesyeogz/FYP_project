import {
  Box,
  Button,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  useTheme,
} from "@mui/material";
import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import GraphChart from "../../components/charts/GraphChart";
import { getGraph, getMLGraph, getMainMLGraph, resetMLGraph } from "../../components/redux/slices/modelSlice";
import { tokens } from "../../theme";

const Graph = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [days, setDays] = useState(30);
  const [predict, setPredict] = useState(false);
  const [indicator_id, setIndicator] = useState(1);
  const dispatch = useDispatch();
  const stock_price = useSelector((state) => state.models.graph);
  const ml_stock_price = useSelector((state) => state.models.predictedgraph);
  useEffect(() => {
    dispatch(getGraph({ id: indicator_id, period: days }));
    if(predict){
      dispatch(getMLGraph({period: days }));
    }else{
      dispatch(getMainMLGraph({period:days}));
    }
  }, [days, predict, indicator_id]);
  return (
    <Box width={"100%"} height={"80%"} p={10}>
      <Box width={"100%"} height={"10%"}>
        <Stack direction={"row"} spacing={2}>
          <Box>
            <InputLabel>Days</InputLabel>
            <Select
              labelId="demo-simple-select-autowidth-label"
              color="secondary"
              value={days}
              onChange={(e) => {
                setDays(e.target.value);
              }}
            >
              <MenuItem value={7}>Weekly</MenuItem>
              <MenuItem value={30}>Monthly</MenuItem>
              <MenuItem value={365}>Yearly</MenuItem>
            </Select>
          </Box>
          <Box>
            <InputLabel>Indicator</InputLabel>
            <Select
              value={indicator_id}
              onChange={(e) => {
                setIndicator(e.target.value);
              }}
            >
              <MenuItem value={1}>ML Indicator</MenuItem>
              <MenuItem value={2}>SMA Indicator</MenuItem>
            </Select>
          </Box>
          <Box>
          <InputLabel>Combine or Split Graph</InputLabel>
            <Button
              variant="contained"
              sx={{
                height: "70%",
                backgroundColor: predict
                  ? colors.redAccent[600]
                  : colors.greenAccent[600],
                ":hover": { backgroundColor: colors.grey[500] },
              }}
              onClick={() => {
                setPredict(!predict);
              }}
              disabled={indicator_id === 2}
            >
              {predict ? "Individual Graph":"Main ML Graph"}
            </Button>
          </Box>
        </Stack>
      </Box>
      <Box width={"100%"} height={"80%"} mt={5}>
        <GraphChart datas={predict ? [stock_price,...ml_stock_price]:[stock_price,...ml_stock_price]} />
      </Box>
    </Box>
  );
};

export default Graph;
