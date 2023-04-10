import { Button } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import React from "react";
import Quick_Navigate from "../../components/global/Quick_Navigate";
import { useDispatch } from "react-redux";
import { DeleteAccount, GetAccountStats, getAccounts } from "../../components/redux/slices/accountSlice";

const PortfolioTable = ({ rows,EditAccount }) => {
  const dispatch = useDispatch();
  const { navigate, params } = Quick_Navigate();
  const columns = [
    {
      field: "id",
      headerName: "ID",
      flex: 1,
    },
    {
      field: "holding",
      headerName: "Shares Holding Now",
      flex: 1,
    },
    {
      field: "indicator",
      headerName: "Indicator Used",
      flex: 2,
    },
    {
      field: "maxshares",
      headerName: "Maximum Shares To hold",
      flex: 1,
    },
    {
      field: "value",
      headerName: "Value of the Shares",
      flex: 1,
    },
    {
      field: "profit",
      headerName: "Profit",
      flex: 1,
    },
    {
      field: "Edit",
      headerName: "Edit Indicator",
      flex: 1,
      renderCell: ({ row: { id,indicator,value } }) => {
        return (
          <Button
            color="neutral"
            variant="contained"
            onClick={() => {
              EditAccount({id:id,indicator:indicator,value:value})
            }}
          >
            Edit This Indicator
          </Button>
        );
      },
    },
    {
      field: "Delete",
      headerName: "Delete Indicator",
      flex: 1,
      renderCell: ({ row: { id } }) => {
        return (
          <Button
            variant="contained"
            color="red"
            onClick={() => {
              dispatch(DeleteAccount({id:id}))
              dispatch(getAccounts());
              dispatch(GetAccountStats());
            }}
          >
            Delete
          </Button>
        );
      },
    },
  ];
  return (
    <DataGrid
      autoPageSize={true}
      pageSizeOptions={[5, 10, 25]}
      disableSelectionOnClick={true}
      rows={rows}
      columns={columns}
    />
  );
};

export default PortfolioTable;
