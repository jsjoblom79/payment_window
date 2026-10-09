"use strict";

import display_button, {btn_type, display_input, display_options, grid_two, input_type} from "/assets/js/components.js";

export default function display_form(id){
    const div = document.createElement('div');
    const form = document.createElement('form');
    div.classList.add('card');

    form.setAttribute("novalidate",null);
    form.id = id;

    form.append(
        grid_two(
            display_input("SSN","pay-SSN", input_type.TEXT, false),
            display_input("Payment Date", "pay-payment_date",input_type.TEXT, false)
        ),
        grid_two(
            display_options("Void",[])
        )
    );


    const button = display_button("submit",() => {}, btn_type.PRIMARY);
    div.append(form);
    return div;
}