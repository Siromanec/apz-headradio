import "../css/PostBase.css";
import likeIconEmpty from "../data/emptyHeart.svg";
import likeIconFull from "../data/redHeart.svg";
import {useEffect, useState} from "react";
import parse from "html-react-parser";

import UrlResolver from "./UrlResolver";
import RequestBodyBuilder from "./RequestBodyBuilder";

const urlResolver = new UrlResolver();

export default function PostBase({
    images,
    article,
    date,
    nlikes,
    id,
    username,
}) {
    const [hasLiked, setHasLiked] = useState(false);
    const [nLikes, setNLikes] = useState(nlikes ? nlikes : 0);
    const hasLikedHandler = async (data) => {
        // const like = fetch("http://localhost:8000/has-liked", {
        const liked = await fetch(urlResolver.getIsLikedPostUrl(username, id, sessionStorage.getItem("token")),
            RequestBodyBuilder.getIsLikedPostRequestBody())
            .then((data) => data.json())
            .catch((data) => data.json());

        console.log(liked);
        if (liked) {
            if (liked["liked"] === "0") {
                setHasLiked(false);
            } else {
                setHasLiked(true);
            }
            setNLikes(nlikes)
        }
    };
    /**
     * @param value.author
     * @param value.idpost
     * */
    const setLikeHandler = async (value) => {
        return fetch(urlResolver.getLikePostUrl(value.author, value.idpost, sessionStorage.getItem("token")),
            RequestBodyBuilder.getLikePostRequestBody()
        );
    }

    useEffect(() => {
        hasLikedHandler({ post: id, username: username, author: sessionStorage.getItem("username") });
    }, []);
    const likeHandler = async () => {
        const like = await setLikeHandler({
            idpost: id,
            username: sessionStorage.getItem("username"),
            author: username,
        })
            .then((data) => data.json())
            .catch((data) => data.json());
        if (like["liked"] === "0") {
            setHasLiked(false);
        } else {
            setHasLiked(true);
        }
        setNLikes(like["nlikes"]);
    };
    const dateObj = new Date(date);
    const dateLocale = dateObj.toLocaleString();
    return (
        <div className="post">
            <div className="textPart">
                <div className="fullText">
                    <div className="postText">{article ? parse(article) : ""}</div>
                </div>
                <div className="postFooter">
                    <span className="postDate">{dateLocale}</span>
                    <div className="likes">
                        <span className="nlikes">{nLikes}</span>
                        <button className="likeBtn">
                            <img
                                className="heart"
                                src={hasLiked ? likeIconFull : likeIconEmpty}
                                onClick={likeHandler}
                            ></img>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
