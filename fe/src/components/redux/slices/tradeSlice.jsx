import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axios from "axios";
import { TradeApi } from "../apis/TradeApi";
import { fetchError, fetchStart, fetchSuccess } from "./commonSlice";

export const getTrades = createAsyncThunk("Trades/", 
  async (data,thunkapi) => {
  try {
    await thunkapi.dispatch(fetchStart());
    const response = await TradeApi.getHistory();
    await thunkapi.dispatch(fetchSuccess());
    return response.data;
  }  catch( error ){
    if(axios.isAxiosError(error)){        
        await thunkapi.dispatch(fetchError(error.code))
    }else if (error instanceof Error){
        await thunkapi.dispatch(fetchError(error.message))
    }
    return thunkapi.rejectWithValue(error.code);
}
});

const initialState = {
  data: [],
};

export const tradeSlice = createSlice({
  name: "trades",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
    .addCase(getTrades.pending, (state)=>{
      state.data = [];
  })
  .addCase(getTrades.fulfilled,(state,action)=>{
      console.log(action.payload)
      state.data = action.payload;
  })
  .addCase(getTrades.rejected,(state,action)=>{
      state.data =[]
  })
}});

export const { } = tradeSlice.actions;

export default tradeSlice.reducer;
