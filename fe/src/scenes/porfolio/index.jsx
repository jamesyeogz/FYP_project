import { useTheme } from "@emotion/react";
import {
  Box,
  Button,
  Grid,
  InputLabel,
  MenuItem,
  Modal,
  Select,
  TextField,
  Typography,
} from "@mui/material";
import React, { useState } from "react";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import Header from "../../components/global/Header";
import Quick_Navigate from "../../components/global/Quick_Navigate";
import {
  CreateAccount,
  EditAccount,
  getAccounts,
  GetAccountStats,
} from "../../components/redux/slices/accountSlice";
import { tokens } from "../../theme";
import PortfolioTable from "./PortfolioTable";
import { useFormik } from "formik";
import EditA from "./EditA";
import CreateNew from "./CreateNew";

const Portfolio = () => {
  const [initial, setInitial] = useState({
    maxshares: 0,
    indicator: "ML_indicator",
    value: 0,
  });
  const editAcc = async (data) => {
    await setInitial(data);
    await setOpen(true);
  };
  const [open, setOpen] = useState(false);
  const [newopen, setNewopen] = useState(false);
  const handleNewClose = () => {
    setNewopen(false);
  };
  const handleClose = () => {
    setOpen(false);
  };
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const { navigate, params } = Quick_Navigate();
  const dispatch = useDispatch();
  const accounts = useSelector((state) => state.accounts.accounts);
  const stats = useSelector((state) => state.accounts.stats);
  useEffect(() => {
    dispatch(getAccounts());
    dispatch(GetAccountStats());
  }, []);

  return (
    <Box height={"80%"} width={"100%"} p={5}>
      <Grid container spacing={2} wrap="wrap" pl={5}>
        <Grid item>
          <Box>
            <Header Header="Account Balance" SubHeader={stats.total} />
          </Box>
          <Box>
            <Header Header="Total Profits" SubHeader={stats.profit} />
          </Box>
          <Box>
            <Header Header="Total Trades" SubHeader={stats.total_count} />
          </Box>
        </Grid>
      </Grid>
      <Box height={"70%"} width={"100%"} p={5}>
        <PortfolioTable rows={accounts} EditAccount={editAcc} />
      </Box>
      <Box
        width={"100%"}
        display={"flex"}
        alignContent={"flex-end"}
        justifyContent={"flex-end"}
        p={5}
      >
        <Button color="secondary" variant="contained" onClick={()=>{
          setNewopen(true)
        }}>
          Add New Account
        </Button>
      </Box>
      <EditA open={open} handleClose={handleClose} initialValues={initial} />
      <CreateNew  open={newopen} handleClose={handleNewClose} />
    </Box>
  );
};

export default Portfolio;
