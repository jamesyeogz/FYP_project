import {
  Box,
  Grid,
  InputLabel,
  MenuItem,
  Modal,
  Select,
  TextField,
  Typography,
  Button,
} from "@mui/material";
import { useFormik } from "formik";
import React, { useEffect } from "react";
import { useDispatch } from "react-redux";
import {
  CreateAccount,
  EditAccount,
  GetAccountStats,
  getAccounts,
} from "../../components/redux/slices/accountSlice";
const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  pt: 2,
  px: 4,
  pb: 3,
};
const CreateNew = ({ open, handleClose }) => {
  const dispatch = useDispatch();
  const formik = useFormik({
    initialValues: { indicator: "ML_indicator", value: 0 },
    onSubmit: (values) => {
      dispatch(CreateAccount(values));
      dispatch(getAccounts());
      dispatch(GetAccountStats());
    },
  });
  return (
    <Modal
      open={open}
      onClose={handleClose}
      aria-labelledby="child-modal-title"
      aria-describedby="child-modal-description"
    >
      <Box sx={{ ...style, width: 500, height: 350 }}>
        <Typography variant="h2" mb={3}>
          Create New Account
        </Typography>
        <Grid container spacing={3}>
          <Grid item>
            <InputLabel>Indicator</InputLabel>
            <Select
              fullWidth
              defaultValue="ML_indicator"
              color="secondary"
              name="indicator"
              value={formik.values.indicator}
              onChange={formik.handleChange}
            >
              <MenuItem value={"ML_indicator"}>ML_Indicator</MenuItem>
              <MenuItem value={"SMA_indicator"}>SMA_Indicator</MenuItem>
            </Select>
          </Grid>
        </Grid>
        <Box pr={9} pt={2}>
          <InputLabel>Amount</InputLabel>
          <TextField
            fullWidth
            type="number"
            value={formik.values.value}
            name="value"
            onChange={formik.handleChange}
          />
        </Box>
        <Grid container spacing={10} pt={4}>
          <Grid item>
            <Button variant="contained" color="error" onClick={handleClose}>
              Close Tab
            </Button>
          </Grid>
          <Grid item>
            <Button
              variant="contained"
              color="success"
              onClick={async () => {
                await formik.handleSubmit();
                await handleClose();
              }}
            >
              Create New Account
            </Button>
          </Grid>
        </Grid>
      </Box>
    </Modal>
  );
};

export default CreateNew;
