import React, { Children } from "react";
import Login from "./components/Login";
import './App.css'
import Navbar from './components/Navbar'
import Task from './components/Task'
import {BrowserRouter,Routes,Route} from 'react-router-dom'
import { Navigate } from "react-router-dom";
import { ToastContainer } from 'react-toastify';

const ProtectedRoute=({children})=>{
  const token = localStorage.getItem("token")
  return token ? children : <Navigate to="/"/>
}
export const App = () => {
  return (
    <>
 
    <BrowserRouter>   <ToastContainer/>
      <Routes>
        <Route path="/" element={<Login/>}></Route>
        <Route path="/tasks" element={<ProtectedRoute><Navbar/><Task/></ProtectedRoute>}></Route>
      </Routes>
    </BrowserRouter>
      {/* <Navbar/>
      {/* <Login/> */}
      {/* <Task/>  */}
      
    </>
  )
}