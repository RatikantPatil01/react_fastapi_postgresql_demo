import React from "react";
import Login from "./components/Login";
import './App.css'
import Navbar from './components/Navbar'
import Task from './components/Task'
import {BrowserRouter,Routes,Route} from 'react-router-dom'

export const App = () => {
  return (
    <>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login/>}></Route>
        <Route path="/tasks" element={<Task/>}></Route>
      </Routes>
    </BrowserRouter>
      {/* <Navbar/>
      {/* <Login/> */}
      {/* <Task/>  */}
      
    </>
  )
}