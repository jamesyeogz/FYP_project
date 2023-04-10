import httpClient from '../../../utils/Api';

export const TradeApi ={
    getHistory: () =>{
        return httpClient.get(`dashboard/history`)
    }
}