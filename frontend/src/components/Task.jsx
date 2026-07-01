import React, { use, useEffect, useState } from "react";
import { Check , Trash ,Pencil,Save } from 'lucide-react';
import { ENDPOINTS, instance } from './api';
import { toast } from "react-toastify";

const Task = () =>  {
    const [tasks,setTasks]=useState([])
    const [editable,setEditable]=useState(null)
    const [inputTask,setInputTask]=useState("")
    const [inputDesc,setInputDesc]=useState("")

    const editTask=(e,id)=>{
        setTasks(items => items.map(item=>item.id===id ? {...item,title:e.target.value}: item))
    }

    const editDesc=(e,id)=>{
        setTasks(items => items.map(item=>item.id===id ? {...item,description:e.target.value}: item))
    }
    
    const saveTask=async(id)=>{
        const task= tasks.filter(task=>task.id==id)[0]
        console.log(task);
        await instance.put(ENDPOINTS.UPDATE_TASK(id),{
    title: task.title,
    description: task.description || "",
    completed: task.completed
})
        .then(res=>{
            toast.success("Task Updated successfully")
            getAllTasks()
            setEditable(null)
        })
        .catch(err => {
            console.log(err.response.data);
        });
    }

    const completeTask=async(id)=>{
        const task= tasks.filter(task=>task.id==id)[0]
        await instance.put(ENDPOINTS.UPDATE_TASK(id),{
            title: task.title,
    description: task.description || "",
    completed: 1
        })
        .then(res=>{
            toast.success("Task Completed successfully")
            getAllTasks()
            setEditable(null)
        })
        .catch(err => {
            console.log(err.response.data);
        });
    }

    const undoTask=async(id)=>{
        const task= tasks.filter(task=>task.id==id)[0]
        await instance.put(ENDPOINTS.UPDATE_TASK(id),{
            title: task.title,
    description: task.description || "",
    completed: 0
        })
        .then(res=>{
            toast.success("Task Completed successfully")
            getAllTasks()
            setEditable(null)
        })
        .catch(err => {
            console.log(err.response.data);
        });
    }


    const deleteTask=async(id)=>{
        const task= tasks.filter(task=>task.id==id)[0]
        console.log(task);
        await instance.delete(ENDPOINTS.DELETE_TASK(id))
        .then(res=>{
            toast.success("Task deleted successfully")
            getAllTasks()
            setEditable(null)
        })
        .catch(err => {
            console.log(err.response.data);
        });
    }

    const addTask=async()=>{
        await instance.post(ENDPOINTS.CREATE_TASK(),{title:inputTask,completed:false})
                        .then(res=>{
                            toast.success("Task created successfully")
                            getAllTasks() // This is for fetching All Task After Successfully Added
                            setInputTask("")
                        })
                        .catch(err=>console.log(err))
    }

    const getAllTasks=async()=>{
        await instance.get(ENDPOINTS.GET_TASK())
        .then(res=>setTasks(res.data))
        .catch(error=>console.log(error))
    }

   // This Function will only Call once when component loaded because we passed []
    useEffect(()=>{
        getAllTasks()
    },[])

    // This Function will call when task is updated i mean added , or deleted like that 
    // useEffect(()=>{
    //     getAllTasks()
    // },[tasks])

    return (
        <>
        <div className="container">
            <div className="input-box">
                <input type="text" value={inputTask} onChange={(e)=>setInputTask(e.target.value)}></input>
                <span className="add" onClick={addTask}>Add</span>
            </div>
            <div className="container">
                {
                    tasks.map((item,index)=>{
                        return (
                            <div key={item.id} className="task-items" style={{backgroundColor: item.completed ? "#951547" : "white"}}> 
                                <div className="task-title">
                                    <div className="">
                                        <label className="title">Title :</label>
                                        <input type="text" 
                                        value={item.title} 
                                        disabled={editable !== item.id}
                                        onChange={(e)=>editTask(e,item.id)}></input>

                                        <label className="description">Description :</label>
                                        <input type="text" 
                                        value={item.description} 
                                        disabled={editable !== item.id}
                                        onChange={(e)=>editDesc(e,item.id)}></input>

                                        </div>
                                        <Check size={20} 
                                        onClick={() =>
                                          item.completed
                                            ? undoTask(item.id)
                                            : completeTask(item.id)
                                        }
                                        />
                                    </div>
                                    <div className="icon-group">
                                        {(editable !== item.id ) ? <Pencil size={20} onClick={()=>setEditable(item.id)}/>
                                        : <Save size={20} onClick={()=>saveTask(item.id)}/>}
                                        <Trash size={20} onClick={()=>deleteTask(item.id)} />
                                        </div>
                            </div>
                        )
                    })
                }
            </div>
        </div>
        </>
    )
}

export default Task