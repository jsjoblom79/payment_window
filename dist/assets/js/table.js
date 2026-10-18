"use strict";

export default async function display_table(table_data){
    const card = document.createElement('div');
    const table_wrap = document.createElement('div');
    const table = document.createElement('table');
    const thead = document.createElement('thead');
    const tbody = document.createElement('tbody');
    const fields = await window.pywebview.api.data.get_payment_fields();
    card.classList.add('card');
    table_wrap.classList.add('table-wrap');

    const table_header = [
        'id','SSN', 'Payment Date', 'Cash Amount',
        'Check Amount', 'Credit Amount', 'Void',
        'Posted', 'Check Number', 'Payment Method',
        'Payment Amount', 'Change Date', 'Comments',
        'Receipt Emailed Date'];

    const th_row = document.createElement('tr');

    fields.forEach(field => {
       const th = document.createElement('th');
       th.textContent = field;
       th_row.append(th);
    });
    thead.append(th_row);
    table.append(thead,tbody);

    const create_row = async(record) => {
        const tr = document.createElement('tr');
        fields.forEach(key => {
            const td = document.createElement('td');
            td.textContent = record[key];
            tr.append(td);
        });

        tbody.append(tr);


    };

    if(Array.isArray(table_data)){
        table_data.forEach(record => {
           create_row(record);
        });
    }


    table_wrap.append(table);
    card.append(table_wrap);

    return card;
}