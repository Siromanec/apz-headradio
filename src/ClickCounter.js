import React from "react";
import "./ClickCounter.css"
export default class ClickCounter extends React.Component {
    constructor() {
        super()
        this.count = 0
        this.counter = {
            count: 0
        }
    }
    render() {
        return <div className="ClickCounter">
            <button onClick={()=>++this.count}>
                {this.counter.count}
            </button>
        </div>
    }
}
// export default function ClickCounter(props) {
    
// }