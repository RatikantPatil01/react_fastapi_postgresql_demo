import React, { useState }  from "react";

const Login = () => {
    const [username,setUsername]=useState("")
    const [password,setPassword]=useState("")
    return (
        <>
         <div className="container">
            <form className="login-form">
                <h2>Login</h2>
                <input type="text"
                value={username}
                onChange={(e)=>setUsername(e.target.value)}
                placeholder="Username"></input>
                <input type="password" 
                value={password}
                onChange={(e)=>setUsername(e.target.value)}
                placeholder="Password"></input>
                <button>Login</button>
            </form>
         </div>
        </>
    )
}

export default Login