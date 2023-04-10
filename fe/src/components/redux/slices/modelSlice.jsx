import {createAsyncThunk, createSlice} from '@reduxjs/toolkit';
import { ModelsIndicatorsApi } from '../apis/ModelApi';
import { fetchError, fetchStart, fetchSuccess } from './commonSlice';
import axios from 'axios';
// Get all the exisiting models
export const getGraph = createAsyncThunk(
    'Dashboard/data.id/data.period',
    async(data,thunkapi) =>{
        try{
            await thunkapi.dispatch(fetchStart())
            const response = await ModelsIndicatorsApi.getIndicatorGraph(data)
            await thunkapi.dispatch(fetchSuccess());
            return response.data
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

export const getGeneral = createAsyncThunk(
    'Dashboard/id/general',
    async (id,thunkapi) =>{
        try {
            await thunkapi.dispatch(fetchStart());
            const response = await ModelsIndicatorsApi.getIndicatorGeneral(id)
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
export const getMLGraph = createAsyncThunk(
    'Dashboard/ml/<period>',
    async (data,thunkapi) =>{
        try {
            await thunkapi.dispatch(fetchStart());
            // data contains indicator id and period
            const response = await ModelsIndicatorsApi.getMLGraph(data)
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
export const getMainMLGraph = createAsyncThunk(
    'Dashboard/mainml/<period>',
    async (data,thunkapi) =>{
        try {
            await thunkapi.dispatch(fetchStart());
            // data contains indicator id and period
            const response = await ModelsIndicatorsApi.getMainMLGraph(data)
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
export const getStats = createAsyncThunk(
    'Dashboard/id/stats',
    async (id,thunkapi) =>{
        try {
            console.log(id)
            await thunkapi.dispatch(fetchStart());
            const response = await ModelsIndicatorsApi.getIndicatorStats(id)
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
//Create new custom model with bot

const initialState ={
    indicators: [],
    graph: [],
    predictedgraph: [],
    stats: [],
    general: []
}

export const modelSlice = createSlice({
    name:'models',
    initialState,
    reducers:{
        getIndicators: (state)=>{
            state.indicators = [{id:1,'indicator':'ML_indicator'}];
        },
        resetMLGraph: (state) =>{
            state.predictedgraph= []
        }
    },
    extraReducers: (builder) =>{
        builder
        .addCase(getStats.pending, (state)=>{
            state.stats = [];
        })
        .addCase(getStats.fulfilled,(state,action)=>{
            state.stats = action.payload;
        })
        .addCase(getStats.rejected,(state,action)=>{
            state.stats =[]
        })
        .addCase(getGraph.pending, (state)=>{
            state.graph = [];
        })
        .addCase(getGraph.fulfilled,(state,action)=>{
            state.graph = action.payload;
        })
        .addCase(getGraph.rejected,(state,action)=>{
            state.graph =[]
        })
        .addCase(getGeneral.pending, (state)=>{
            state.general = [];
        })
        .addCase(getGeneral.fulfilled,(state,action)=>{
            state.general = action.payload;
        })
        .addCase(getGeneral.rejected,(state)=>{
            state.general = [];
        })
        .addCase(getMLGraph.pending, (state)=>{
            state.predictedgraph = [];
        })
        .addCase(getMLGraph.fulfilled,(state,action)=>{
            state.predictedgraph = action.payload;
        })
        .addCase(getMLGraph.rejected,(state)=>{
            state.predictedgraph =[]
        })
        .addCase(getMainMLGraph.pending, (state)=>{
            state.predictedgraph = [];
        })
        .addCase(getMainMLGraph.fulfilled,(state,action)=>{
            state.predictedgraph = [action.payload];
        })
        .addCase(getMainMLGraph.rejected,(state)=>{
            state.predictedgraph =[]
        })
    }
})
export const{
    getIndicators,resetMLGraph
} = modelSlice.actions;

export default modelSlice.reducer;