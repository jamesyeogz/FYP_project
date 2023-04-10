import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  error: "",
  loading: false,
  message: "",
};

export const commonSlice = createSlice({
  name: "common",
  initialState,
  reducers: {
    fetchStart: (state) => {
      state.loading = true;
      state.error = "";
      state.message = "";
    },
    fetchSuccess: (state) => {
      state.loading = false;
      state.error = "";
      state.message = "";
    },
    fetchError: (state, action) => {
      state.loading = false;
      state.error = action.payload;
      state.message = "";
    },
    showMessage: (state, action) => {
      state.loading = false;
      state.error = "";
      state.message = action.payload;
    },
  },
});


export const {
    fetchStart,
    fetchError,
    fetchSuccess,
    showMessage,
    
} = commonSlice.actions;

export default commonSlice.reducer;    