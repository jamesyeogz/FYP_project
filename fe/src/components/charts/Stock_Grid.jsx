import React from "react";
import { DataGrid, GridRowsProp, GridColDef } from "@mui/x-data-grid";
import { Box, useTheme } from "@mui/material";
import { tokens } from "../../theme";
import { clsx } from "clsx";
import { useDispatch, useSelector } from "react-redux";
import { getTrades } from "../redux/slices/tradeSlice";
import { useEffect } from "react";
const Stock_Grid = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const dispatch = useDispatch();
  const trades = useSelector((state) => state.trades);
  useEffect(() => {
    dispatch(getTrades());
  }, [dispatch]);
  const columns = [
    { field: "Date", headerName: "Date", flex: 1 },
    { field: "account_id", headerName: "Account Id", flex: 1 },
    { field: "buy", headerName: "Price Opened", flex: 1 },
    {
      field: "profit",
      headerName: "Profit/Loss",
      flex: 1,
      cellClassName: (params) => {
        if (params.value == null) {
          return "";
        }
        return clsx("super-app", {
          negative: params.value < 0,
          positive: params.value > 0,
        });
      },
    },
    { field: "sell", headerName: "Price Closed", flex: 1 },
    // {
    //   field: "sell",
    //   headerName: "Status",
    //   flex: 1,
    //   renderCell: ({ row: { sell } }) => {
    //     if(sell){
    //       var Status = "Closed"
    //     }else{
    //       var Status = "Trading"
    //     }
    //     return (
    //       <Box
    //         width="60%"
    //         m="0"
    //         p={1}
    //         display="flex"
    //         justifyContent={"center"}
    //         backgroundColor={
    //           Status === "Trading"
    //             ? colors.blueAccent[400]
    //             : Status === "Closed"
    //             ? colors.redAccent[400]
    //             : colors.greenAccent[400]
    //         }
    //         fontWeight={'bold'}
    //         borderRadius={1}
    //         color={colors.grey[100]}
    //       >
    //         {Status}
    //       </Box>
    //     );
    //   },
    // },
  ];

  return (
    <Box
      height="80%"
      width="80%"
      sx={{
        "& .super-app.negative": {
          color: colors.redAccent[300],
        },
        "& .super-app.positive": {
          color: colors.greenAccent[300],
        },
      }}
    >
      <DataGrid
        rows={trades.data}
        columns={columns}
        autoPageSize={true}
        disableSelectionOnClick={true}
        initialState={{
          rows: [],
          pagination: {
            paginationModel: { pageSize: 5 },
          },
        }}
      />
    </Box>
  );
};

export default Stock_Grid;
