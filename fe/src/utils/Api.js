import axios from 'axios';

const httpClient = axios.create({
    // baseURL: 'https://stormy-mountain-44464.herokuapp.com/',
    baseURL: 'http://127.0.0.1:5000',
    headers:{
        'Content-Type': 'application/json'
    },

})

export default httpClient;