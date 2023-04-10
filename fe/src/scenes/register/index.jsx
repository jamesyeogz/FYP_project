import React from "react";
import {
  Avatar,
  Box,
  Container,
  TextField,
  useTheme,
  Typography,
  Button,
  Grid,
  FormControlLabel,
  Checkbox,
} from "@mui/material";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import { Link } from "react-router-dom";
import { tokens } from "../../theme";
import { useDispatch, useSelector } from "react-redux";
import Quick_Navigate from "../../components/global/Quick_Navigate";
import { useFormik } from "formik";
import { useState } from "react";
import { RegisterUser } from "../../components/redux/slices/authSlice";
import { fetchError } from "../../components/redux/slices/commonSlice";
import { showMessage } from "../../components/redux/slices/commonSlice";
const RegisterPage = () => {
  const [cfmpass, setCfmpass] = useState("");
  const [error, setError] = useState(false);
  const [userError, setUserError] = useState(false);
  const dispatch = useDispatch();
  const { navigate, params } = Quick_Navigate();
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const formik = useFormik({
    initialValues: {
      user: "",
      password: "",
    },
    onSubmit: async (values) => {
      if (cfmpass !== values.password) {
        setError(true);
      } else {
        await dispatch(RegisterUser(values));
      }
    },
  });

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Avatar sx={{ m: 1, bgcolor: "secondary.main" }}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign up
        </Typography>
        <Box
          component="form"
          noValidate
          sx={{ mt: 3 }}
          onSubmit={formik.handleSubmit}
        >
          <Grid container spacing={1}>
            <Grid item xs={12}>
              <TextField
              error={userError ? true : false}
                color={userError ? "error" : "secondary"}
                helperText={userError ? "Duplicate Username" : ""}
                required
                fullWidth
                label="Username"
                name="user"
                value={formik.values.user}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                color="secondary"
                value={formik.values.password}
                onChange={formik.handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                error={error ? true : false}
                margin="normal"
                required
                fullWidth
                name="Confirm Password"
                label="Confirm Password"
                type="password"
                color={error ? "error" : "secondary"}
                helperText={
                  error ? "Password does not tally Or Duplicate Username" : ""
                }
                onChange={(e) => {
                  setCfmpass(e.target.value);
                }}
              />
            </Grid>
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="filled"
            sx={{
              mt: 3,
              mb: 2,
              backgroundColor: colors.greenAccent[700],
              ":hover": {
                bgcolor: colors.greenAccent[400],
                color: colors.primary[800],
              },
            }}
          >
            Sign Up
          </Button>
          <Grid container justifyContent="flex-end">
            <Grid item>
              <Link to="/login">Already have an account? Sign in</Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
};

export default RegisterPage;
