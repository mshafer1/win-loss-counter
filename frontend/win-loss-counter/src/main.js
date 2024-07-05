import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import VueSocketIO from 'vue-3-socket.io'
import SocketIO from 'socket.io-client'
import router from './router'

const app = createApp(App)
app.use(router)

var socket_addr = import.meta.env.VITE_DOMAIN
if (typeof(socket_addr) == "undefined") {
    socket_addr = "/";
}

console.log("Domain / host", socket_addr)

app.use(new VueSocketIO({
    debug: true,
    connection: SocketIO(socket_addr, {path: ''}),
    // vuex: {
        
    // }
}))


app.mount('#app')
