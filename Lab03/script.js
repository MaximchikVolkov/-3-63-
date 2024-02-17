service_key = '4ee9945c4ee9945c4ee9945c574dfeab6f44ee94ee9945c2b23fce7182293d69d4167b2';
user_id = 279586664;

function btnHandler() {
    let div_city = document.getElementsByClassName('city-div')[0];
    div_city.innerHTML = "";

    const inputs = document.getElementsByClassName('city-input');
    let city = inputs[0].value;
    if (city == "") {
        alert("Введите город!");
        return;
    }

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
            if (item.city.toLowerCase().indexOf(city.toLowerCase()) != -1) {
                let row = $('<tr>').appendTo(tbody);
                $('<td>').text(item.id).appendTo(row);
                $('<td>').text(item.name).appendTo(row);
                $('<td>').text(item.city).appendTo(row);
                $('<td>').append($('<img>').attr('src', item.photo)).appendTo(row);
            }
        });

        // Вставляем таблицу на страницу
        table.appendTo('.city-div');
    });
}