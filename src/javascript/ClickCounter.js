import React from "react";
import "../css/ClickCounter.css"
export default class ClickCounter extends React.Component {
    constructor(props) {
        super(props)
        this.counter = {
            count: 0
        }
        this.clicked = this.clicked.bind(this)
    }
    clicked(event){
        this.setState({value: ++this.counter.count})
    }
    render() {
        return <div className="ClickCounter">
            <button onClick={this.clicked}>
                {this.counter.count}
            </button>
        </div>
    }
}
// export default function ClickCounter(props) {
    
// }