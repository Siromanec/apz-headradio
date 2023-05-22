import { spotifyClientID, spotifyClientSecret } from "./APIKeys";

const APIController = (function () {

    const clientId = spotifyClientID;
    const clientSecret = spotifyClientSecret;

    // private methods
    const _getToken = async () => {

        const result = await fetch("https://accounts.spotify.com/api/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic " + btoa(clientId + ":" + clientSecret)
            },
            body: "grant_type=client_credentials"
        });

        const data = await result.json();
        return data.access_token;
    }

    const _getTrack = async (token, songID) => {

        const result = await fetch(`https://api.spotify.com/v1/tracks/${songID}`, {
            method: "GET",
            headers: { "Authorization": "Bearer " + token }
        });

        const data = await result.json();
        return data.name + " • " + data.artists[0].name;
    }

    return {
        getToken() {
            return _getToken();
        },
        getTrack(token, trackEndPoint) {
            return _getTrack(token, trackEndPoint);
        }
    }
})();

async function getSong(songID) {
    const token = await APIController.getToken();
    return await APIController.getTrack(token, songID);
}

getSong("2QjOHCTQ1Jl3zawyYOpxh6")
  .then(song => {
    console.log(song); // Update the DOM element with the song data
  })

