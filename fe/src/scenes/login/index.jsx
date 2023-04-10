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

import React, { useEffect } from "react";
import { tokens } from "../../theme";
import { Link } from "react-router-dom";
import { useFormik } from "formik";
import { useDispatch, useSelector } from "react-redux";
import { LoginUser } from "../../components/redux/slices/authSlice";
import Quick_Navigate from "../../components/global/Quick_Navigate";

const LoginPage = () => {
  
  const {navigate,params} = Quick_Navigate();
  
  const dispatch = useDispatch();
  const isLoggedIn = useSelector(state => state.auth.isLoggedIn)
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const formik = useFormik({
    initialValues: {
      user: '',
      password: ''
    },
    onSubmit: async(values) =>{
      await dispatch(LoginUser(values));
      await navigate("/portfolio");
    }
  });
  return (
    <Container component="main" maxWidth="xs">
      <Box
      component="form"
      onSubmit={formik.handleSubmit}
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
          Log in
        </Typography>
        <Box sx={{ mt: 1 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="user"
            label="Username"
            name="user"
            color="secondary"
            value ={formik.values.user}
            onChange ={formik.handleChange}
          />
          <TextField
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            color="secondary"
            value ={formik.values.password}
            onChange ={formik.handleChange}
          />
          <Button
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
            type='submit'

          >
            Sign In
          </Button>
          <Grid container>
            <Grid item>
              <Link to="/register">"Don't have an account? Sign Up"</Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
};

export default LoginPage;
