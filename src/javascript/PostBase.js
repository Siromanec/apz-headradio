import "../css/PostBase.css"
import openFullIcon from "../data/three-dots.svg"
import likeIconEmpty from "../data/emptyHeart.svg"
import likeIconFull from "../data/redHeart.svg"
import { useEffect, useState } from "react";
import parse from 'html-react-parser';

async function setLikeHandler(data) {
    return fetch("http://localhost:8000/fetch-like", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    });
}


export default function PostBase({ images, article, date, nlikes, id, username }) {
    const [hasLiked, setHasLiked] = useState(false);
    const [nLikes, setNLikes] = useState(nlikes);
    const hasLikedHandler = async(data) => {
        const like = fetch("http://localhost:8000/fetch-has-liked", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data)
        }).then((data) => data.json())
            .catch((data) => data.json());
        if (like["liked"] === 0) {
            setHasLiked(false)
        }
        else {
            setHasLiked(true)
        };
        console.log(hasLiked)
    
    }

    useEffect(() => {hasLikedHandler({ "post": id, "username": sessionStorage.getItem("username") })} , [])
    const likeHandler = async () => {
        
        const like = await setLikeHandler({ "idpost": id, "username": sessionStorage.getItem("username"), "author": username})
            .then((data) => data.json())
            .catch((data) => data.json());
        if (like["liked"] === "0") {
            setHasLiked(false);
        }
        else {
            setHasLiked(true);
        }
        setNLikes(like["nlikes"]);
    }
    const dateObj = new Date(date);
    const dateLocale = dateObj.toLocaleString()
    return (
        <div className="post">
            <div className="photoPart">
            </div>
            <div className="textPart">
                <div className="fullText">
                    <div className="postText">
                        {article ? parse(article) : ""}
                    </div>
                </div>
                <div className="postFooter">
                    <span className="postDate">{dateLocale}</span>
                    <div className="likes">
                        <span className="nlikes">{nLikes}</span>
                        <button className="likeBtn"><img className="heart" src={!hasLiked ? likeIconFull : likeIconEmpty} onClick={likeHandler}></img></button>
                    </div>
                </div>
            </div>
        </div>
    )
}