user_id = 279586664;
app_id = 51855155;

function btnAuthHandler() {
    window.location.replace(`https://oauth.vk.com/authorize?client_id=${app_id}&display=popup&redirect_uri=https://oauth.vk.com/blank.htm&scope=wall,groups,offline&response_type=token&v=5.199`);
}