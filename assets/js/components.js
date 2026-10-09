"use strict";


export let btn_type = Object.freeze({
    DANGER: 'danger',
    PRIMARY: 'primary',
    SECONDARY: 'secondary',
    SMALL: 'small'
});

export let badge_type = Object.freeze({
    INPROGRESS: 'inprogress',
    TODO: 'todo',
    DONE: 'done'
});

export let input_type = Object.freeze({
    TEXT: 'text',
    SELECT: 'select',
    DATE: 'date',
    EMAIL: 'email'
});

export let option_type = Object.freeze({
    RADIO: 'radio',
    CHECKBOX: 'checkbox'
});

export default function display_button(content, event, btntype){
    const button = document.createElement('button');
    button.textContent = content;
    button.classList.add('btn');
    button.addEventListener('click', event);

    switch (btntype){
        case btn_type.DANGER:
            button.classList.add('btn-danger');
            break;
        case btn_type.PRIMARY:
            button.classList.add('btn-primary');
            break;
        case btn_type.SMALL:
            button.classList.add('btn-small');
    }

    return button;
}

export function display_badge(content, badgeType){
    const span = document.createElement('span');
    span.classList.add('badge');

    switch (badgeType){
        case badge_type.INPROGRESS:
            span.classList.add('inprogress');
            break;
        case badge_type.DONE:
            span.classList.add('done');
            break;
        case badge_type.TODO:
            span.classList.add('todo');
            break;
    }

    span.textContent = content;
    return span;
}

export function display_topbar(span_content){
    const header = document.createElement('header');
    const top_div = document.createElement('div');
    const brand = document.createElement('div');
    const span = document.createElement('span');
    const brand_mark = document.createElement('span');

    header.classList.add('topbar');
    top_div.classList.add('topbar-inner');
    brand.classList.add('brand');
    brand_mark.classList.add('brand-mark');
    span.classList.add('muted');

    brand_mark.textContent = "PW";
    brand.append(brand_mark, "Payment Window");

    span.textContent = span_content;

    top_div.append(brand, span);
    header.append(top_div);

    return header;
}

export function display_input(input_label, input_id, input_type, required = false, placeholder= null){
    const div = document.createElement('div');
    const label = document.createElement('label');
    const input = document.createElement('input');
    const alert = document.createElement('span');

    div.classList.add('field');
    label.for = input_id;
    label.textContent = input_label;


    input.classList.add('input');
    input.type = input_type;
    input.name = input_id;
    input.id = input_id;
    input.placeholder = placeholder;
    input.required = required;

    div.append(label, input);

    return div;
}

export function display_options(content, options, option_type){
    const fs = document.createElement('fieldset');
    const legend = document.createElement('legend');
    const div = document.createElement('div');

    div.classList.add('options');
    fs.append(legend, div);
    if(Array.isArray(options)){
        options.forEach(option => {
            const label = document.createElement('label');
            label.classList.add('check');
            const input = document.createElement('input');
            input.type = option_type;
            input.name = content;
            input.value = option.value;
            label.append(input);
            div.append(label);
        });
    }
    return fs;
}

export function grid_two(...elements){
    const div = document.createElement('div');
    div.classList.add('grid-2');

    div.append(...elements);

    return div;

}