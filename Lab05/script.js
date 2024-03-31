user_id = 279586664;
app_id = 51855155;
implicit_flow = 'vk1.a.ivzH8AP23CIje9WE5sEJmVKY80HUpAob694tdw1DbwVwI-1WFWzQEm1JEm3xJvIthAFV66epWLdAbE9Xttne10wqiFo5cdB6lJDndWCKCF1NqkNRhsQ-GMsb6uwzTwidNYqQt-BLdfR6Q-1InkfJ-WvHMOGe_BYFayEz482hH4VJhJNH17Qb2hT866zNal_hjHU25WIreuMkSmw_Aac0lQ';


async function btnPostHandler() {
    let div_groups = document.getElementsByClassName('groups')[0];
    div_groups.innerHTML = "";

    const inputs = document.getElementsByClassName('input-groups-number');
    let groups_num = inputs[0].value;
    if (groups_num <= 4 && groups_num !== "") {
        alert("Некорректное значение!");
        return;
    }

    let date_start = document.getElementsByClassName('time-start')[0].value;
    let date_end = document.getElementsByClassName('time-end')[0].value;
    if (date_start === "" || date_end === "") {
        alert("Введите дату!");
        return;
    }
    date_start = convert_datetime_to_unix(date_start);
    date_end = convert_datetime_to_unix(date_end);
    if (date_start > date_end) {
        alert("Введите корректные даты!");
        return;
    }

    let url = ``;
    if (groups_num === "") {
        url = `https://api.vk.com/method/groups.get?user_id=${user_id}&extended=1&fields=description,members_count&access_token=${implicit_flow}&v=5.199`;
    } else {
        url = `https://api.vk.com/method/groups.get?user_id=${user_id}&extended=1&fields=description,members_count&count=${groups_num}&access_token=${implicit_flow}&v=5.199`;
    }

    await $.getJSON({
        url: url,
        jsonp: "callback",
        dataType: "jsonp"
        }).done(async function( data ) {
            console.log(data);
        
            let groups_items = data?.response?.items;
            let table_data = [];
            //let random = get_random_int(0, (groups_items.length - 5) - 1);

            for (let i = 0; i < groups_items.length; i++) {
                sleep(500);
                await $.getJSON({
                    url: `https://api.vk.com/method/wall.get?owner_id=-${groups_items[i].id}&count=100&access_token=${implicit_flow}&v=5.199`,
                    jsonp: "callback",
                    dataType: "jsonp"
                }).done(async function(data_posts) {

                    let name = groups_items[i].name;
                    let members_count = groups_items[i].members_count;
                    let photo = groups_items[i].photo_100;
                    
                    let posts_items = data_posts?.response?.items;
                    let posts_count = 0;
                    for (let j = 0; j < posts_items.length; j++) {
                        let post_date = posts_items[j].date;
                        // console.log(post_date);
                        if (post_date <= date_end && post_date >= date_start) {
                            posts_count++;
                        }

                    }

            
                    table_data.push({name: name, members_count: members_count, photo: photo, posts_count: posts_count});
                    
                });
            }
            table_data.sort( function(a, b) { return b.posts_count - a.posts_count});

            let table = $('<table>').addClass('groups-table');
        
            // Добавляем заголовки столбцов
            let thead = $('<thead>').appendTo(table);
            $('<th>').text('Название').appendTo(thead);
            $('<th>').text('Количество участников').appendTo(thead);
            $('<th>').text('Количество постов').appendTo(thead);
            $('<th>').text('Аватарка').appendTo(thead);
        
            // Добавляем данные в таблицу
            let tbody = $('<tbody>').appendTo(table);
            for (let i = 0; i < 5; i++) {
                let row = $('<tr>').appendTo(tbody);
                $('<td>').text(table_data[i].name).appendTo(row);
                $('<td>').text(table_data[i].members_count).appendTo(row);
                $('<td>').text(table_data[i].posts_count).appendTo(row);
                $('<td>').append($('<img>').attr('src', table_data[i].photo)).appendTo(row);
            }
            
            // Вставляем таблицу на страницу
            table.appendTo('.groups');
        });

            /*for (let i = random; i < random + 5; i++) {
                
                let name = groups_items[i].name;
                let members_count = groups_items[i].members_count;
                let photo = groups_items[i].photo_100;
        
                table_data.push({name: name, members_count: members_count, photo: photo});
            }
            console.log(table_data);
        
            // Создаем HTML таблицу
            let table = $('<table>').addClass('groups-table');
        
            // Добавляем заголовки столбцов
            let thead = $('<thead>').appendTo(table);
            $('<th>').text('Название').appendTo(thead);
            $('<th>').text('Количество участников').appendTo(thead);
            $('<th>').text('Аватарка').appendTo(thead);
        
            // Добавляем данные в таблицу
            let tbody = $('<tbody>').appendTo(table);
            $.each(table_data, function(i, item){
                let row = $('<tr>').appendTo(tbody);
                $('<td>').text(item.name).appendTo(row);
                $('<td>').text(item.members_count).appendTo(row);
                $('<td>').append($('<img>').attr('src', item.photo)).appendTo(row);
            });
            
            // Вставляем таблицу на страницу
            table.appendTo('.groups');
            
            post(table_data);
        });
        */
}

function get_random_arbitrary(min, max) {
    return Math.random() * (max - min) + min;
}

function get_random_int(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function post(group_data) {
    let text = `Не обращайте внимание, я делаю лабу <3%0A%0A`;

    for (let i = 0; i < group_data.length; i++) {
        text += `В группе  ${group_data[i]?.name}  --  ${group_data[i]?.members_count}  участников.%0A`; 
    }
    console.log(text);

    $.getJSON({
        url: `https://api.vk.com/method/wall.post?owner_id=${user_id}&friends_only=1&message=${text}&close_comments=1&access_token=${implicit_flow}&v=5.199`,
        jsonp: "callback",
        dataType: "jsonp"
        }).done(function( data ) {
            if (data.hasOwnProperty('error')) {
                alert("Ошибка!");
                return;
            }
            alert("Пост отправлен!");
        });
}

function convert_datetime_to_unix(datetime) {
    return (new Date(datetime).getTime() / 1000);
}

function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
        currentDate = Date.now();

    } while (currentDate - date < milliseconds);
}