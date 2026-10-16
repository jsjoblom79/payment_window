import {display_topbar} from "/js/components.js";
import display_main from "/js/main.js";

let main;
window.addEventListener('pywebviewready', async () =>{
    const user_info = await window.pywebview.api.data.get_current_user();
    const topbar = display_topbar(user_info["name"]);
    main = await display_main();
    document.body.append(topbar, main);
});