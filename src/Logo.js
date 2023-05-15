import React from "react";
import "./Logo.css"

export default class Logo extends React.Component{
    constructor(props){
        super(props)
        this.pathname = "./logo.svg"
        this.path = "root"
    }
    render(){
        return <div className="Logo"></div>
    }
}