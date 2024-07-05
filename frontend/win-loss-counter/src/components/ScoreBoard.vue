<template>
  <div>
    <div v-if="!connection_ready">
      Connecting...
    </div>
    <div v-else> 
      <!-- background-color: #181818; -->
      <span v-text="wins"></span> <span>/</span> <span v-text="losses"> </span>
      <br />
      <span v-text="percentage"></span>
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