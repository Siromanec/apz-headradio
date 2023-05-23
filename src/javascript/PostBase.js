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

async function hasLikedHandler(data) {
    const like = fetch("http://localhost:8000/fetch-has-liked", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
    }).then((data) => data.json())
    .catch((data) => data.json());
    if (like["liked"] === 0) {
        return false;
    }
    else {
        return true;
    };

}

export default function PostBase({ images, article, date, nlikes, idpost, username}) {
    const [hasLiked, setHasLiked] = useState(false);
    useEffect(()=>{setHasLiked(hasLikedHandler({"post": idpost , "username": username}));}, [])
    const [nLikes, setNLikes] = useState(nlikes);
    const likeHandler = async () => {
        const like = await setLikeHandler({"idpost": idpost , "username": username})
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
    return (
        <div className="post">
            <div className="photoPart">
            </div>
            <div className="textPart">
                <div className="fullText">
                    <div className="postText">
                        {article??false ? parse(article): ""}
                    </div>
                    <button className="openFullTextBtn"><img className="fullTextImg" src={openFullIcon}></img></button>
                </div>
                <div className="postFooter">
                    <span className="postDate">{date}</span>
                    <div className="likes">
                        <span className="nlikes">{nLikes}</span>
                        <button className="likeBtn"><img className="heart" src={hasLiked ? likeIconFull : likeIconEmpty} onClick={likeHandler}></img></button>
                    </div>
                </div>
            </div>
        </div>
    )
}