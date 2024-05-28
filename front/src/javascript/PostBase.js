import "../css/PostBase.css";
import likeIconEmpty from "../data/emptyHeart.svg";
import likeIconFull from "../data/redHeart.svg";
import {useEffect, useState} from "react";
import parse from "html-react-parser";

import UrlResolver from "./api/UrlResolver";
import RequestBodyBuilder from "./api/RequestBodyBuilder";
import {getToken, getUsername} from "./api/SessionStorage";

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
        const liked = await fetch(urlResolver.getIsLikedPostUrl(username, id, getToken()),
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
        return fetch(urlResolver.getLikePostUrl(value.author, value.idpost, getToken()),
            RequestBodyBuilder.getLikePostRequestBody()
        );
    }

    useEffect(() => {
        hasLikedHandler({ post: id, username: username, author: getUsername()});
    }, []);
    const likeHandler = async () => {
        const like = await setLikeHandler({
            idpost: id,
            username: getUsername(),
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
