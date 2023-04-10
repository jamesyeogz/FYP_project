import httpClient from '../../../utils/Api';

export const ModelsIndicatorsApi ={
    getIndicatorStats: (id) =>{
        return httpClient.get(`dashboard/${id}/stats`)
    },
    getIndicatorGeneral: (id) =>{
        return httpClient.get(`Dashboard/${id}/general`)
    },
    getIndicatorGraph:(data) =>{
        return httpClient.get(`dashboard/${data.id}/${data.period}`)
    },
    getMLGraph:(data) =>{
        return httpClient.get(`dashboard/ml/${data.period}`)
    },
    getMainMLGraph:(data) =>{
        return httpClient.get(`dashboard/mainml/${data.period}`)
    },
}