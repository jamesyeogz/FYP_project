import {configureStore} from '@reduxjs/toolkit';
import commonSlice  from '../slices/commonSlice';
import  modelSlice  from '../slices/modelSlice';
import authSlice from '../slices/authSlice';
import tradeSlice from '../slices/tradeSlice';
import accountSlice from '../slices/accountSlice';


export const store = configureStore({
    reducer: {
        common: commonSlice,
        auth: authSlice,
        models: modelSlice,
        trades: tradeSlice,
        accounts:accountSlice
    },
})

