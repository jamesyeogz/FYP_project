import httpClient from '../../../utils/Api';

export const AuthApi ={
    Login: (data) =>{
        return httpClient.post(`auth/login`,data)
    },
    Register: (data) =>{
        return httpClient.post(`auth/register`,data)
    }
    
}