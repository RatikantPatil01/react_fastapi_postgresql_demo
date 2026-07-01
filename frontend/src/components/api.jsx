import axios from 'axios';
import { toast } from 'react-toastify'

export const ENDPOINTS={
    LOGIN :()=>"/user/login",
    CREATE_TASK :()=>"/tasks/create-task",
    GET_TASK :()=>"/tasks/get-tasks",
    UPDATE_TASK :(id)=>`/tasks/update-task/${id}`,
    DELETE_TASK :(id)=>`/tasks/delete-task?id=${id}`,
}


export const instance = axios.create({
    baseURL:"http://127.0.0.1:8000/"
})

instance.interceptors.request.use(config=>{
    const token = localStorage.getItem("token")
    if(token)
        config.headers.Authorization = `Bearer ${token}`
    return config
},(error)=>{return Promise.reject(error)})

// Interceptors Is Basically Used For To Perform An Action Before CAlling a APi or Getting Response From Api 
// Example Sending Token While Calling Api or Handling Error AFter Calling Api

instance.interceptors.response.use((response)=>response,(error)=>{
    if(error.response.status === 401){
        localStorage.removeItem("token")
        toast.error("Invalid Credentials")
        window.location.href="/"
    }
    return Promise.reject(error)
})