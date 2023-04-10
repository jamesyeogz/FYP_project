import { Box, colors, Typography, useTheme } from "@mui/material";
import React from "react";
import { tokens } from "../../theme";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import TrendingDownIcon from "@mui/icons-material/TrendingDown";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";

export const SmallBox = ({ Day, Profit }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  return (
    <Box pr={1}>
      <Typography variant="h5">{Day}</Typography>
      <Typography
        variant="h4"
        fontWeight={"bold"}
        color={Profit < 0 ? colors.redAccent[400] : colors.greenAccent[400]}
      >
        {Profit}
      </Typography>
    </Box>
  );
};

const Statsbox = ({ number = 1000, Chart }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  return (
    <Box
      flexGrow={1}
      backgroundColor={colors.primary[400]}
      display="flex"
      flexDirection="row"
      justifyContent="space-between"
      p={3}
      mb={2}
      m={2}
    >
      <Box display="flex" flexDirection="column" justifyContent="space-around">
        <Box display="flex" alignItems="center">
          <AccountBalanceIcon />
          <Typography variant="h4" paddingLeft={1}>
            Total Profit Margin
          </Typography>
        </Box>
        <Typography
          variant="h1"
          fontWeight="bold"
          color={number > 0 ? colors.greenAccent[400] : colors.redAccent[400]}
        >
          ${number}
          {number > 0 ? (
            <TrendingUpIcon fontSize="large" />
          ) : (
            <TrendingDownIcon />
          )}
        </Typography>
        <Box display="flex" flexDirection="row" justifyContent="space-between">
          <SmallBox Day="Daily" Profit="-500" />
          <SmallBox Day="Weekly" Profit="-500" />
          <SmallBox Day="Monthly" Profit="-500" />
        </Box>
      </Box>
      {Chart}
    </Box>
  );
};

export default Statsbox;
