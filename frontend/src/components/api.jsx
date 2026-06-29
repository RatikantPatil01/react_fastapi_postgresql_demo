import axios from 'axios';

export const ENDPOINTS={
    LOGIN :()=>"/users/login",
    CREATE_TASK :()=>"/tasks/create-task",
    GET_TASK :()=>"/tasks/get-task",
    UPDATE_TASK :()=>"/tasks/update-task",
    DELETE_TASK :()=>"/tasks/delete-task",
}

export const instance = axios.create({
    baseURL:"http://127.0.0.1:8000"
})