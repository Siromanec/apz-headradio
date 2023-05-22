import React from "react"
import FriendSongElement from "./FriendSongElement.js"
import Avatar from "../data/profile.jpg"
import PostBase from "./PostBase.js"

export default function Home() {
    return (<div>
        <PostBase
            numberLikes={22}
            date={"2 MAY 2023"}
            text={"Alonso is greatest driver of all time. Everyone who thinks different — is wrong. He won championships in bad cars and always showed great results. Alonso FTW"}
        ></PostBase>

        <FriendSongElement songName="Окситоцин  •  Ницо Потворно" avatar={Avatar}></FriendSongElement>
    </div>)
    }
