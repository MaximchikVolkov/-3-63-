let xml_text = "";

function inputOnChangeHandler(input) {
    let file = input.files[0];

    let reader = new FileReader();

    reader.readAsText(file);

    reader.onload = function() {
        console.log(reader.result);
        
        xml_text = reader.result.replace(/  |\r\n|\n|\r/gm, "");
    }

    reader.onerror = function() {
        console.log(reader.error);

        xml_text = "";
    }
}


function btnOnClickHandler() {
    if (xml_text == "")
    {
        alert("Выберите XML файл!");
        return;
    }

    const xml_obj = parseXML(xml_text);
    console.log(xml_obj);

    let elems = get_elems_last_level(xml_obj);
    console.log(elems);
    
    let elem_num_input = document.querySelector("input[name='elem-num-input']");
    if (elem_num_input.value == "")
    {
        alert("Random elements by 3rd lvl: \n" + myToString(elems[get_random_int(0, elems.length - 1)]));
    }
    else
    {
        if (elem_num_input.value < 1 || elem_num_input.value > elems.length) {
            alert("Неправильно введенный номер элемента 2-го уровня!");
            return;
        }

        alert(`Elements of 3rd lvl by ${elem_num_input.value} element: \n` + myToString(elems[elem_num_input.value - 1]));
    }
    
}

function parseXML(xml_str) {
    const dom_parser = new DOMParser();
    const xml_dom = dom_parser.parseFromString(xml_str, "text/xml");
    
    const error = xml_dom.querySelector("parsererror");
    if (error) {
        alert("Файл некорректен!");
        return null;
    }

    const root_elem = xml_dom.documentElement;

    function parse_node(node) {
        const result = {};

        const attributes = node.attributes;
        for (let i = 0; i < attributes.length; i++) {
            const attribute = attributes[i];
            result[attribute.name] = attribute.value;
        }

        const child_nodes = node.childNodes;
        for (let i = 0; i < child_nodes.length; i++) {
            const child_node = child_nodes[i];

            if (child_node.nodeType == Node.ELEMENT_NODE) {
                const child_result = parse_node(child_node);

                if (result[child_node.nodeName]) {
                    if (!Array.isArray(result[child_node.nodeName])) {
                        result[child_node.nodeName] = [result[child_node.nodeName]];
                    }
                    result[child_node.nodeName].push(child_result);
                } else {
                    result[child_node.nodeName] = child_result;
                }
            }

            if (child_node.nodeType == Node.TEXT_NODE) {
                result["text"] = child_node.nodeValue;
            }
        }

        return result;
    }

    return parse_node(root_elem);
}

function get_elems_last_level(obj) {
    let obj_depth = get_obj_depth(obj);
    
    let result = [];
    function get_elems_by_depth(other_obj, cur_obj_depth) {
        for (let key in other_obj) {
            if (!other_obj.hasOwnProperty(key)) continue;

            if (typeof other_obj[key] == 'object') {
                if (Array.isArray(other_obj[key])) {
                    result = get_elems_by_depth(other_obj[key], cur_obj_depth);
                } else {
                    result = get_elems_by_depth(other_obj[key], cur_obj_depth + 1);

                    if ((cur_obj_depth == obj_depth - 1) && (!other_obj[key].hasOwnProperty('text'))) {
                        result.push(other_obj[key]);
                    }
                }
            }
        }

        return result;
    }

    return get_elems_by_depth(obj, 1);
}

function get_obj_depth(obj) {
    let level = 0;
    for (let key in obj) {
        if (!obj.hasOwnProperty(key)) continue;

        if (typeof obj[key] == 'object') {
            let depth;
            if (Array.isArray(obj[key])) {
                depth = get_obj_depth(obj[key]);
            }
            else {
                depth = get_obj_depth(obj[key]) + 1;
            }
            
            level = Math.max(depth, level);
        }
    }
    return level;
}

function get_random_arbitrary(min, max) {
    return Math.random() * (max - min) + min;
}

function get_random_int(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function myToString(obj) {
    let str = "";
    for (key in obj) {
        str += key.toString();
        str += ": ";
        str += obj[key]['text'];
        str += ";\n"
    }
    return str;
}