# HeadRadio

## Vision
HeadRadio was designed to be a small version of a social network that combines features from existing social networks like Spotify and Instagram along with general ideas of blog and journaling. You can use your page as a journal, follow other people, like their posts, share the music you are listening to the most right now, and much more. Our microservices-based architecture ensures scalability and reliability by incorporating Hazelcast, Consul, Docker Compose, SQL, and NoSQL databases to deliver a robust and immersive user experience.

## Architecture
![image](https://github.com/Siromanec/apz-headradio/assets/91982071/70fd01b6-7ad9-4986-b218-c4e49a9d05d1)
There are **6** main microservices:
1) **auth-service**: responsible for user authentication, storage of usernames, emails, and passwords (SQL database, sqlalchemy)
2) **post-service**: stores the information about all posts (noSQL database, MongoDB), provides API for post creation and deletion
3) **profile-service**: responsible for the profile page of the user, including setting photo, adding music, and storing this information (noSQL database, MongoDB)
4) **friendzone-service**: allows users to follow/unfollow other users and get the list of their followers (SQL database, sqlalchemy)
5) **likes-service**: provides the logic for adding/removing likes on posts (SQL database, sqlalchemy)
6) **feed-service**: incorporates all the data about followed pages, along with recently played songs from your friends and their latests posts.
   
Communication with the clients is executed via an API gateway, and all clients' activities are logged by a logging service that incorporates a message queue. 

## Use cases

### Possible actions
- register/login
- set photo
- set music
- write/delete a post
- search other users by username
- follow/remove a friend
- get a favorite song and the latest posts of followed users
- add/remove like on a post

### Examples
*would be great to add scenarios with different number of microservice instances and their behavior in different situations*

## Links
- architecture [diagram](https://drive.google.com/file/d/1--v8JdgGvQnYgnzEhLhxxedfaLRa2m69/view?usp=sharing)
- [FigmaDesign](https://www.figma.com/design/jxPF5sCpckApn59pTFHQKc/WebProject?node-id=0%3A1&t=x3PPyBabbjrCoVsd-1)
