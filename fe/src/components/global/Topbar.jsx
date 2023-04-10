import {
  Box,
  IconButton,
  InputBase,
  Typography,
  useTheme,
} from "@mui/material";
import React from "react";
import { useContext } from "react";
import { ColorModeContext, tokens } from "../../theme";
import PersonIcon from "@mui/icons-material/Person";
import LeftDrawer from "./LeftDrawer";
import LogoutIcon from "@mui/icons-material/Logout";
import { borderRadius } from "@mui/system";
import { useDispatch } from "react-redux";
import { logout } from "../redux/slices/authSlice";
const Topbar = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const colorMode = useContext(ColorModeContext);
  const dispatch = useDispatch();

  return (
    <Box display="flex" justifyContent="space-between" p={2}>
      <Box display="flex" borderRadius="3px" alignItems={"center"}>
        <LeftDrawer />
        <Typography variant="h4" fontWeight={"bold"} ml={2}>
          Welcome back James Yeo!
        </Typography>
      </Box>
      <Box display="flex">
        <IconButton>
          <PersonIcon />
        </IconButton>
        <IconButton
          sx={{
            borderRadius: 0,
          }}
          onClick={()=>{
            dispatch(logout())
          }}
        >
          <Typography marginRight={1}>Logout</Typography>
          <LogoutIcon />
        </IconButton>
      </Box>
    </Box>
  );
};

export default Topbar;
