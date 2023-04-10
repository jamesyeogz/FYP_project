import {createAsyncThunk, createSlice} from '@reduxjs/toolkit';
import { AccountApi } from '../apis/AccountApi';
import { ModelsIndicatorsApi } from '../apis/ModelApi';
import { fetchError, fetchStart, fetchSuccess } from './commonSlice';
import axios from 'axios'

export const DeleteAccount = createAsyncThunk(
    'models/DeleteAccount',
    async(data,thunkapi) =>{
        try{
            await thunkapi.dispatch(fetchStart())
            const response = await AccountApi.DeleteAccount(data)
            await thunkapi.dispatch(fetchSuccess());
            return response.data
        } catch (error) {
            if(axios.isAxiosError(error)){
                await thunkapi.dispatch(fetchError(error.code))
            } else if (error instanceof Error){
                await thunkapi.dispatch(fetchError(error.message))
            }
            return thunkapi.rejectWithValue(error.code)
        }
    }
)

export const EditAccount = createAsyncThunk(
    'models/EditAccount',
    async(data,thunkapi) =>{
        console.log(data)
        try{
            await thunkapi.dispatch(fetchStart())
            const response = await AccountApi.EditAccount(data)
            await thunkapi.dispatch(fetchSuccess());
            return response.data
        } catch (error) {
            if(axios.isAxiosError(error)){
                await thunkapi.dispatch(fetchError(error.code))
            } else if (error instanceof Error){
                await thunkapi.dispatch(fetchError(error.message))
            }
            return thunkapi.rejectWithValue(error.code)
        }
    }
)

export const CreateAccount = createAsyncThunk(

    'models/AddAcount',
    async(data,thunkapi) =>{
        try{
            await thunkapi.dispatch(fetchStart())
            const response = await AccountApi.AddAccount(data)
            await thunkapi.dispatch(fetchSuccess());
            return response.data
        } catch (error) {
            if(axios.isAxiosError(error)){
                await thunkapi.dispatch(fetchError(error.code))
            } else if (error instanceof Error){
                await thunkapi.dispatch(fetchError(error.message))
            }
            return thunkapi.rejectWithValue(error.code)
        }
    }
)

export const GetAccountStats = createAsyncThunk(

    'dashboard/users/stats',
    async(_,thunkapi) =>{
        try{
            await thunkapi.dispatch(fetchStart())
            const response = await AccountApi.GetAccountsStats()
            await thunkapi.dispatch(fetchSuccess());
            return response.data
        } catch (error) {
            if(axios.isAxiosError(error)){
                await thunkapi.dispatch(fetchError(error.code))
            } else if (error instanceof Error){
                await thunkapi.dispatch(fetchError(error.message))
            }
            return thunkapi.rejectWithValue(error.code)
        }
    }
)

export const getAccounts = createAsyncThunk(

    'models/GetAccounts',
    async(_,thunkapi) =>{
        try{
            await thunkapi.dispatch(fetchStart())
            const response = await AccountApi.GetAccounts()
            await thunkapi.dispatch(fetchSuccess());
            return response.data
        } catch (error) {
            if(axios.isAxiosError(error)){
                await thunkapi.dispatch(fetchError(error.code))
            } else if (error instanceof Error){
                await thunkapi.dispatch(fetchError(error.message))
            }
            return thunkapi.rejectWithValue(error.code)
        }
    }
)

const initialState = {
    accounts: [],
    stats: []
}

export const accountSlice = createSlice({
    name:'accounts',
    initialState,
    reducers:{
    },
    extraReducers:(builder) =>{
        builder
        .addCase(getAccounts.pending, (state) =>{
            state.accounts = [];
        })
        .addCase(getAccounts.fulfilled,(state,action)=>{
            state.accounts = action.payload;
        })
        .addCase(getAccounts.rejected,(state,action)=>{
            state.accounts =[]
        })
        .addCase(GetAccountStats.pending, (state) =>{
            state.stats = [];
        })
        .addCase(GetAccountStats.fulfilled,(state,action)=>{
            state.stats = action.payload;
        })
        .addCase(GetAccountStats.rejected,(state,action)=>{
            state.stats =[]
        })
    }
})

export const{
    
} = accountSlice.actions;

export default accountSlice.reducer;