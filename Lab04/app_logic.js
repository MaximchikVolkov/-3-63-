user_id = 279586664;
app_id = 51855155;
service_key = '4ee9945c4ee9945c4ee9945c574dfeab6f44ee94ee9945c2b23fce7182293d69d4167b2';
let posts = [];
let current_post = 0;
let profile_id = 0;

implicit_flow = 'vk1.a.H2DYmPumbxWQv5-7_vt3LjBaiXODoTuMzZw7vhVWKb4x2gRJGPbH_wgmV_0w3R7imVGCePFWiROMIRKRUciJTf3d_35orEySir0N-pDvYKYta66Fmu_I9GqxbBT2eFjBXWRzwUpWgBoO9fHXEpKquVrnaQF87X91xL50E8BudRb-PsqyJXHFhF29DGV2oFA9svlU3iuATDnzof-KhsgvSA';

$.getJSON({
url: `https://api.vk.com/method/friends.get?user_id=${user_id}&fields=photo_100,city&access_token=${service_key}&v=5.199`,
jsonp: "callback",
dataType: "jsonp"
}).done(function( data ) {
    console.log(data);

    let friends_items = data?.response?.items;
    let table_data = [];

    for (let i = 0; i < friends_items.length; i++) {

        let id = friends_items[i].id ? friends_items[i].id : "---";
        let city = friends_items[i].city ? friends_items[i].city.title : "---";
        let name = friends_items[i].first_name + " " + friends_items[i].last_name;
        let photo = friends_items[i].photo_100;

        table_data.push({id: id, name: name, city: city, photo: photo});
    }
    console.log(table_data);

    // Создаем HTML таблицу
    let table = $('<table>').addClass('friends-table');

    // Добавляем заголовки столбцов
    let thead = $('<thead>').appendTo(table);
    $('<th>').text('ID').appendTo(thead);
    $('<th>').text('ФИО').appendTo(thead);
    $('<th>').text('Город').appendTo(thead);
    $('<th>').text('Фото').appendTo(thead);

    // Добавляем данные в таблицу
    let tbody = $('<tbody>').appendTo(table);
    $.each(table_data, function(i, item){
        let row = $('<tr>').appendTo(tbody);
        $('<td>').text(item.id).appendTo(row);
        $('<td>').text(item.name).appendTo(row);
        $('<td>').text(item.city).appendTo(row);
        $('<td>').append($('<img>').attr('src', item.photo)).appendTo(row);
    });

    // Вставляем таблицу на страницу
    table.appendTo('.friends-div');
});

function btnGetPostsHandler() {
    let div_city = document.getElementsByClassName('friends-div')[0];
    div_city.innerHTML = "";

    const inputs = document.getElementsByName('comment-sender-input');
    profile_id = inputs[0].value;
    
    if (profile_id == '' || profile_id <= 0) {
        alert("Введите корректный ID пользователя");
        return;
    }

    $.getJSON({
        url: `https://api.vk.com/method/wall.get?owner_id=${profile_id}&offset=0&count=100&access_token=${implicit_flow}&v=5.199`,
        jsonp: "callback",
        dataType: "jsonp"
        }).done(function( data ) {
            let div_user_posts = document.getElementsByClassName('user-posts')[0];
            div_user_posts.innerHTML = "";
            current_post = 0;


            if (data.hasOwnProperty('error')) {
                switch (data?.error?.error_code) {
                    case 19:
                        alert("Контент заблокирован!")
                        break;

                    case 15:
                        alert("Доступ запрещен!");
                        break;

                    case 18:
                        alert("Страница удалена или заблокирована!");
                        break;

                    case 30:
                        alert("Приватный профиль!");
                        break;

                    case 113:
                        alert("Неверный ID пользователя!");
                        break;

                    default:
                        alert("Неизвестная ошибка!");
                        break;
                }
                return;
            }

            if (data?.response?.count == 0) {
                alert("У пользователя с таким ID нет постов!");
                return;
            }

            
            let comm_input = $('<input>').addClass('comment-sender-comment-input');
            let comm_btn = $('<button>').addClass('comment-sender-comment-btn');

            comm_input.attr('type', 'text');
            comm_input.attr('placeholder', 'Введите комментарий');
            
            comm_btn.attr('type', 'button');
            comm_btn.attr('onclick', 'btnSendCommHandler()');
            comm_btn.text('Прокомментировать');

            comm_input.appendTo('.user-posts');
            comm_btn.appendTo('.user-posts');

            addUserPosts(data?.response?.items);
        });
}

function addUserPosts(items_array) {
    posts = [];
    let posts_length = 0;
    
    for (let i=0; i < items_array.length; i++) {
        let post_text = items_array[i]['text'];
        
        if (post_text != '') {
            posts[posts_length] = items_array[i]['id'];

            let post = $('<p>').addClass(`user-posts-post-${posts_length}`);
            post.attr('onclick', 'postClickHandler(this)');
            post.text(`${posts_length+1}. ` + post_text).appendTo('.user-posts');

            posts_length++;
        }
    }
}

function btnSendCommHandler() {
    if (current_post == 0) {
        alert("Выберите пост!");
        return;
    }

    const inputs = document.getElementsByClassName('comment-sender-comment-input');
    let comm_text = inputs[0].value;
    if (comm_text == '') {
        alert("Введите комментарий!");
        return;
    }

    $.getJSON({
        url: `https://api.vk.com/method/wall.createComment?owner_id=${profile_id}&post_id=${current_post}&message=${comm_text}&access_token=${implicit_flow}&v=5.199`,
        jsonp: "callback",
        dataType: "jsonp"
        }).done(function( data ) {
            if (data.hasOwnProperty('error')) {
                switch (data?.error?.error_code) {
                    case 212:
                        alert("Запрещено комментировать посты!");
                        break;

                    default:
                        alert("Неизвестная ошибка!");
                        break;
                }
                return;
            }
            alert("Комментарий отправлен!");
        });
}

function postClickHandler(post) {
    for (let i = 0; i < posts.length; i++) {
        $(`.user-posts-post-` + `${i}`).css('background-color', 'rgb(255, 255, 255)');
    }

    $(`.${post.className}`).css('background-color', 'rgb(255, 189, 211)');

    current_post = posts[post.className.replace('user-posts-post-', '')];
    console.log(current_post);
}