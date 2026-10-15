"use strict";

import display_table from "/assets/js/table.js";
import display_form from "/assets/js/form.js";

export default async function display_main(){
    const main = document.createElement('main');
    const section = document.createElement('section');
    const userinfo = await window.pywebview.api.data.get_current_user();
    console.log(userinfo);
    section.setAttribute("aria-labelledby", "list-title");

    const pageHead = display_page_head();

    main.append(section);
    const data = await window.pywebview.api.data.get_all_payments();
    const table = await display_table(data);
    const form = display_form("payment", userinfo);
    section.append(form, pageHead, table);
    return main;
}

function display_page_head(){
    const page_head = document.createElement('div');
    const div = document.createElement('div');
    const h1 = document.createElement('h1');
    const p = document.createElement('p');
    h1.textContent = "Prior Payments";
    //p.textContent = "Search for entered payments";

    div.append(h1, p);
    page_head.append(div);
    return page_head;
}