<template>
  <div class="red circle w3-padding w3-display-container">
    <div v-if="!connection_ready" class="w3-display-middle title-text">
      Loading scores...
    </div>
    <div v-else> 
      <div class="w3-display-top title-text" style="">
        <p>Death Counter</p>
      </div>
      <div class="w3-display-middle body-text super-large-text rock-salt-regular" style="font-size: 100pt;">
        <div class="w3-display-middle" v-text="wins" style="margin-top: -65px; margin-left: -80px;"></div> 
        <div style="font-size: 200pt; font-weight: 50; margin-top: -10px;" class="w3-display-middle">/</div>
        <div class="w3-display-middle" v-text="losses" style="margin-top: 60px; margin-left: 110px;"> </div>
        <div class="label-text w3-display-middle" style="top: 70px; left: -110px; font-weight: bold">P</div>
        <div class="label-text w3-display-middle" style="top: -70px; left: 130px; font-weight: bold">D</div>
      </div>
    </div>
  </div>
</template>

<script>
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
  computed: {
    percentage: function () {
      if (this.wins == 0 && this.losses == 0) {
        return '-'
      }
      if (this.losses == 0) {
        return '100% !'
      }
      var result = (this.wins * 100) / (this.losses + this.wins)
      var rounded = Math.round(result * 100) / 100
      return `${rounded} %`
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
  },
  mounted() {
    this.init_score()
  }
}
</script>

<style>
</style>