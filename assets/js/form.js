"use strict";

import display_button, {
    btn_type,
    display_input,
    display_options, grid_three,
    grid_two, in_div,
    input_type,
    option_type, returnFormattedDate
} from "/assets/js/components.js";

export default function display_form(id, user_info){
    const div = document.createElement('div');
    const form = document.createElement('form');
    div.classList.add('card');

    form.setAttribute("novalidate",null);
    form.id = id;
    const now = new Date();
    const teller = display_input("Teller","pay-teller", input_type.TEXT, false,null, user_info["name"]);
    const paydate = display_input("Payment Date", "pay_pay_date", input_type.DATE, true, null, now.toISOString().split('T')[0]);
    const Name = display_input("Name", "pay-Name", input_type.TEXT, false);
    const ssn_accnt = display_input("SSN or ACCT", "pay-SSN_ACCOUNT", input_type.TEXT, true);
    const pay_method = display_options("Payment Method", "pay-payment_method", ["Cash", "Check", "Credit"],option_type.RADIO);
    const pay_amount = display_input("Payment Amount", "pay-payment_amount", input_type.TEXT, false, "50.00");
    const address_line = display_input("Address", "pay-address", input_type.TEXT, false, "7400 Tiburon St.");
    const city = display_input("City", "pay-city", input_type.TEXT, false, "Albuquerque");
    const state = display_input("State", "pay-state", input_type.TEXT, false, "NM");
    const zip = display_input("Zip", "pay-zip", input_type.TEXT, false, "87109");
    const email = display_input("Email", "pay-email", input_type.TEXT, false, "address@domain.com");
    const system = display_input("System", "pay-system", input_type.TEXT, false, "IFA");
    const hundreds = display_input("Hundreds", "pay-hundreds", input_type.TEXT, false, null, 0.0);
    const fifties = display_input("Fifties", "pay-fifties", input_type.TEXT, false, null, 0.0);
    const twenties = display_input("Twenties", "pay-twenties", input_type.TEXT, false, null, 0.0);
    const tens = display_input("Tens", "pay-tens", input_type.TEXT, false, null, 0.0);
    const fives = display_input("Fives", "pay-fives", input_type.TEXT, false, null, 0.0);
    const ones = display_input("Ones", "pay-ones", input_type.TEXT, false, null, 0.0);
    const twos  = display_input("Twos", "pay-twos", input_type.TEXT, false, null, 0.0);
    const coins = display_input("Coins", "pay-coins", input_type.TEXT, false, null, 0.0);
    const cash_total = display_input("Cash Amount", "pay-cash_amount", input_type.TEXT, false,null, 0.0);
    const email_receipt = display_options("Email Receipt to Borrower", "pay-email_receipt_to_borrower", ["Email Receipt to Borrower"], option_type.CHECKBOX);
    const email_receipt_sent = display_input("Date/Time Receipt Sent", "pay-email_sent", input_type.DATE, false);
    const comments = display_input("Comments", "pay-comments", input_type.TEXTAREA, false,"Enter your comments here");
    hundreds.addEventListener('change', (e) => { cash_total.add();});
    fifties.addEventListener('change', (e) =>{ cash_total.add();});
    twenties.addEventListener('change', (e) => { cash_total.add();});
    tens.addEventListener('change', (e)=>{ cash_total.add();});
    fives.addEventListener('change', (e) => { cash_total.add();});
    ones.addEventListener('change', (e) => {cash_total.add();});
    twos.addEventListener('change', (e) => { cash_total.add();});
    coins.addEventListener('change', (e) => {cash_total.add();});
    const cash_amount_fields = [hundreds, fifties, twenties, tens, fives, ones, twos, coins];
    form.append(
        grid_two(teller, paydate), grid_two(Name, ssn_accnt),
        grid_two(pay_method,pay_amount),
        grid_two(
            in_div(email, address_line,grid_three(city, state, zip)),
            in_div(grid_three(hundreds, tens,ones), grid_three(fifties, fives, coins), grid_three(twenties, twos, cash_total))
        )
        ,grid_two(
            in_div(email_receipt, email_receipt_sent),
            in_div(system)
        ),
       comments
    );

    cash_total.add = () => {
        let amt = 0.0;
        cash_amount_fields.forEach(field => {
           const key = field.input.id.replace('pay-', '');
           const field_amt = parseFloat(field.get_value());

           switch(key){
               case "hundreds":
                   amt += (field_amt * 100);
                   break;
               case "fifties":
                   amt += (field_amt * 50);
                   break;
               case "twenties":
                   amt += (field_amt * 20);
                   break;
               case "tens":
                   amt += (field_amt * 10);
                   break;
               case "fives":
                   amt += (field_amt * 5);
                   break;
               case "ones":
                   amt += field_amt;
                   break;
               case "twos":
                   amt += (field_amt * 2);
                   break;
               case "coins":
                   amt += (field_amt / 100);
                   break;
               default:
                   amt;
           }

        });
        cash_total.set_value(amt);
    };
    const button = display_button("submit",async() => {
        let check_amount = 0;
        let credit_amount = 0;
        const payMethod = pay_method.getValue();
        console.log(payMethod);
        switch(payMethod){
            case "check":
                check_amount = pay_amount.input.value;
                break;
            case "credit":
                credit_amount = pay_amount.input.value;
                break;
        }
        const payment = {
            "ssn_hash": ssn_accnt.input.value,
            "last_four": ssn_accnt.input.value.substring(ssn_accnt.input.value.length - 4, ssn_accnt.input.value.length),
            "payment_date": paydate.input.value,
            "name": Name.input.value,
            "address": address_line.input.value,
            "city": city.input.value,
            "state": state.input.value,
            "zip_code": zip.input.value,
            "email": email.input.value,
            "system": system.input.value,
            "cash_amount": cash_total.input.value,
            "check_amount": check_amount,
            "credit_amount": credit_amount,
            "void": null,
            "posted": null,
            "check_number": null,
            "payment_method": pay_method.getValue(),
            "payment_amount": pay_amount.input.value,
            "change_due": null,
            "comments": comments.input.value,
            "receipt_emailed_date": email_receipt_sent.input.value,


        };
        await window.pywebview.api.data.make_payment(payment);
        console.log(payment);
    }, btn_type.PRIMARY);
    form.append(button);
    div.append(form);
    return div;
}