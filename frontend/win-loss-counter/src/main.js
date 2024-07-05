import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import VueSocketIO from 'vue-3-socket.io'
import SocketIO from 'socket.io-client'
import router from './router'

const app = createApp(App)
app.use(router)

app.use(new VueSocketIO({
    debug: true,
    connection: SocketIO('http://localhost:5000', {path: ''}),
    // vuex: {
        
    // }
}))


app.mount('#app')
