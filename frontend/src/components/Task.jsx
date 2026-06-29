import React, { use, useState } from "react";
import { Check , Trash ,Pencil,Save } from 'lucide-react';

const Task = () =>  {
    const [tasks,setTasks]=useState([
        {
            id:1,title:"java",completed:true
        },
        {
            id:2,title:"python",completed:false
        }
    ])

    const [editable,setEditable]=useState(null)
    const editTask=(e,id)=>{
        setTasks(items => items.map(item=>item.id===id ? {...item,title:e.target.value}: item))
    }
    const saveTask=()=>{
        setEditable(null)
    }
    return (
        <>
        <div className="container">
            <div className="input-box">
                <input type="text"></input>
                <span className="add">Add</span>
            </div>
            <div className="container">
                {
                    tasks.map((item,index)=>{
                        return (
                            <div key={item.id} className="task-items">
                                <div className="task-title">
                                    <div className="">
                                        <label className="title">Title :</label>
                                        <input type="text" 
                                        value={item.title} 
                                        disabled={editable !== item.id}
                                        onChange={(e)=>editTask(e,item.id)}></input>
                                        </div>
                                        <Check/>
                                    </div>
                                    <div className="icon-group">
                                        {(editable !== item.id ) ? <Pencil size={20} onClick={()=>setEditable(item.id)}/>
                                        : <Save size={20} onClick={saveTask}/>}
                                        <Trash size={20}/>
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