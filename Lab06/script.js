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

    let url = ``;
    if (groups_num === "") {
        url = `https://api.vk.com/method/groups.get?user_id=${user_id}&extended=1&fields=description,members_count&access_token=${implicit_flow}&v=5.199`;
    } else {
        url = `https://api.vk.com/method/groups.get?user_id=${user_id}&extended=1&fields=description,members_count&count=${groups_num}&access_token=${implicit_flow}&v=5.199`;
    }

    let groups_items;
    try {
        groups_items = (await get_groups(url))?.response?.items;
    } catch(error) {
        alert(error);
        return;
    }

    let table_data = [];
    let random = get_random_int(0, (groups_items.length - 5) - 1);

    for (let i = random; i < random + 5; i++) {
        
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


    let exel_data = [];
    for (let i = 0; i < groups_items.length; i++) {
        
        let name = groups_items[i].name;
        let members_count = groups_items[i].members_count;

        exel_data.push([name, members_count]);
    }

    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(exel_data);
    
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    XLSX.writeFile(wb, "groups.xlsx");
}

async function get_groups(url) {
    return  $.getJSON({
        url: url,
        jsonp: "callback",
        dataType: "jsonp"
        }).promise();
}

function get_random_arbitrary(min, max) {
    return Math.random() * (max - min) + min;
}

function get_random_int(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

async function post(group_data) {
    let text = `Не обращайте внимание, я делаю лабу <3%0A%0A`;

    for (let i = 0; i < group_data.length; i++) {
        text += `В группе  ${group_data[i]?.name}  --  ${group_data[i]?.members_count}  участников.%0A`; 
    }
    console.log(text);

    try {
        let result = (await post_groups(text));
    } catch (error) {
        alert(error);
        return;
    }

    alert("Пост отправлен!");
}

async function post_groups(text) {
    return $.getJSON({
        url: `https://api.vk.com/method/wall.post?owner_id=${user_id}&friends_only=1&message=${text}&close_comments=1&access_token=${implicit_flow}&v=5.199`,
        jsonp: "callback",
        dataType: "jsonp"
        }).promise();
}