<script setup>
import NumberInputVue from './NumberInput.vue'
</script>

<template>
  <div class="w3-xxlarge rowdies-bold">
    <div v-if="!connection_ready">Connecting...</div>
    <div v-else>
      <NumberInputVue :label="'Potato'" v-on:change="updateScore" v-bind:valueParent="wins" />
      <br />
      <NumberInputVue :label="'Dalma'" v-on:change="updateScore" v-bind:valueParent="losses" />
    </div>
  </div>
</template>
  
  <script>
// import { ref, reactive, computed } from 'vue'
// <span :v-html="percentage"></span><span> %</span>
export default {
  name: 'ScoreBoard',
  data: () => {
    return {
      wins: 0,
      losses: 0,
      connection_ready: false,
      connection_error: false,
      websocket: null
    }
  },
  sockets: {
    connect: function () {
      console.log('socket connected')
      this.connection_ready = true
    },
    disconnect: function () {
      this.connection_ready = false
    },
    customEmit: function (data) {
      console.log('this method was fired by the socket server. eg: io.emit("customEmit", data)')
    },
    newScore: function (data) {
      console.log('New Score logged', data)
      this.wins = data.wins
      this.losses = data.losses
    }
  },
  methods: {
    init_score() {
      self.wins = 0
      self.losses = 0

      this.$socket.emit('connected')
    },
    updateScore(label, value) {
        console.log("Recived update event", label, value)
        this[label] = value;
        this.$socket.emit("new score", JSON.stringify({wins: this.wins, losses: this.losses}))
      },
  },
  mounted() {
    this.init_score()
  }
}
</script>
  
<style>
</style>