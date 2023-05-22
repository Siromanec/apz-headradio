import "../css/PostBase.css"
import openFullIcon from "../data/three-dots.svg"
import likeIconEmpty from "../data/emptyHeart.svg"
export default function PostBase({photos, text, date, numberLikes}) {
    return (
        <div className="post">
            <div className="photoPart">
            </div>
            <div className="textPart">
                <div className="fullText">
                    <div className="postText">
                        <p>{text}</p>
                    </div>
                    <button className="openFullTextBtn"><img className="fullTextImg" src={openFullIcon}></img></button>
                </div>
                <div className="postFooter">
                    <span className="postDate">{date}</span>
                    <div className="likes">
                        <span className="numberLikes">{numberLikes}</span>
                        <button className="likeBtn"><img className="heart" src={likeIconEmpty}></img></button>
                    </div>
                </div>
            </div>
        </div>
    )
}