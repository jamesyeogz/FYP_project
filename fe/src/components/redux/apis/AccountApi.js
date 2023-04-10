import httpClient from '../../../utils/Api';

export const AccountApi ={
    GetAccountsStats:()=>{
        return httpClient.get('dashboard/user/stats')
    },
    GetAccounts:() =>{
        return httpClient.get(`models/GetAccounts`)
    },
    AddAccount: (data) =>{
        return httpClient.post(`models/AddAccount`,data)
    },
    DeleteAccount: (data) =>{
        return httpClient.post(`models/DeleteAccount`,data)
    },
    EditAccount:(data) =>{
        return httpClient.post(`models/EditAccount/${data.id}`,data)
    }
    
}