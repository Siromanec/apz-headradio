import React, { useState, useEffect } from "react";
import "../css/ChangeSong.css";
import crossButton from "../data/cross.svg"

export default function ChangeSong() {
    const [popUpClass, setPopUpClass] = useState("popup-change");
    function handleClick() {
        setPopUpClass("popup-change show")
    }

    function exitClick() {
        setPopUpClass("popup-change")
    }
    return <div className="changeSong">
        <div className={popUpClass}>
            <div className="insert-song">
                <span>Insert song link</span>
                <input type="text" placeholder="..." />
                <button className="exitButton" onClick={exitClick}>
                    <img src={crossButton} />
                </button>
            </div>
        </div>
        <div className="lower-button">
            <button onClick={handleClick}>Change Song</button>
        </div>
    </div>
}