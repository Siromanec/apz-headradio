import React from "react"

export default function PhotoChange({onClick}) {
    const [file, setFile] = React.useState()
    const changleHandler = (e) => {
        setFile(e.target.files[0])
    }

    
    return <div className="PhotoChange">
        <input type="file" onChange={changleHandler} />
        Load new photo from computer
        <button onClick={onClick}>Sumbit</button>
    </div>
}