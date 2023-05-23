import React from "react"

export default function PhotoChange({changleHandler}) {    
    return <div className="PhotoChange">
        <input type="file" onChange={changleHandler} />
    </div>
}