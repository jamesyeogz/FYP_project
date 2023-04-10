import { AuthApi } from "../apis/AuthApi";
import {createAsyncThunk, createSlice} from '@reduxjs/toolkit';
import { ModelsIndicatorsApi } from '../apis/ModelApi';
import { fetchError, fetchStart, fetchSuccess } from './commonSlice';
import axios from 'axios'
import httpClient from "../../../utils/Api";

const initialState = {
  isLoggedIn: false,
  username: "",
  isAdmin: false,
};
export const RegisterUser = createAsyncThunk(
    'auth/register',
    async (data,thunkapi) =>{
        try {
            await thunkapi.dispatch(fetchStart());
            // data contains indicator id and period
            const response = await AuthApi.Register(data)
            await thunkapi.dispatch(fetchSuccess());
            return response.data;
        } catch( error ){
            if(axios.isAxiosError(error)){        
                await thunkapi.dispatch(fetchError(error.code))
            }else if (error instanceof Error){
                await thunkapi.dispatch(fetchError(error.message))
            }
            return thunkapi.rejectWithValue(error.code);
        }
    }
)


export const LoginUser = createAsyncThunk(
    'auth/login',
    async (data,thunkapi) =>{
        try {
            await thunkapi.dispatch(fetchStart());
            // data contains indicator id and period
            const response = await AuthApi.Login(data)
            await thunkapi.dispatch(fetchSuccess());
            return response.data;
        } catch( error ){
            if(axios.isAxiosError(error)){        
                await thunkapi.dispatch(fetchError(error.code))
            }else if (error instanceof Error){
                await thunkapi.dispatch(fetchError(error.message))
            }
            return thunkapi.rejectWithValue(error.code);
        }
    }
)

export const authSlice = createSlice({
  name: "auth",
  initialState: initialState,
  reducers: {
    logout: (state) => {
      state.isLoggedIn = false;
      state.username = "";
      state.isAdmin = false;
      httpClient.defaults.headers.common['Authorization'] = ``
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(LoginUser.pending, (state) => {
      })
      .addCase(LoginUser.fulfilled, (state, action) => {
        const {access_token, username} = action.payload
        state.isLoggedIn = true;
        state.isAdmin = true;
        state.username = username
        httpClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      })
      .addCase(LoginUser.rejected, (state, action) => {
        state.isLoggedIn = false;
      })
      .addCase(RegisterUser.pending, (state) => {
      })
      .addCase(RegisterUser.fulfilled, (state) => {
      })
      .addCase(RegisterUser.rejected, (state, action) => {
      });
  },
});

export const { logout } = authSlice.actions;

export default authSlice.reducer;
