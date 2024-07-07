<script setup>
defineEmits(['change'])
</script>

<template>
  <div class="w3-xxlarge text-color">
    <p v-text="label"></p>
    <span class="w3-hide-small w3-hide-medium">
      <input class="w3-input w3-xxlarge" type="number" v-model="value" @input="onChanged()" />
    </span>
    <span class="w3-row w3-hide-large">
      <div class="w3-col s8 responsive-border large-text">
      {{ value }}
      </div>
      <div class="w3-col s4">
        <button class="w3-button w3-gray" @click="up">&#x25B2;</button>
        <br/>
        <button class="w3-button w3-gray" @click="down">&#x25BC;</button>
      </div>
    </span>
  </div>
</template>

<script>
export default {
  name: 'NumberInput',
  props: {
    label: { type: String, required: true },
    valueParent: { type: Number, required: true }
  },
  watch: {
    valueParent: function (newVal, oldVal) {
      // watch it
      console.log('Prop changed: ', newVal, ' | was: ', oldVal)
      this.value = newVal
    }
  },
  data: () => {
    return {
      value: 0,
      oldValue: 0
    }
  },
  methods: {
    up() {
      this.olValue = this.value;
      this.value += 1;
      this.$emit('change', this.label.toLowerCase(), this.value);
    },
    down() {
      this.olValue = this.value;
      this.value -= 1;
      this.$emit('change', this.label.toLowerCase(), this.value);
    },
    onChanged(event) {
      if (this.value == this.oldValue) {
        return
      }

      this.oldValue = this.value
      this.$emit('change', this.label.toLowerCase(), this.value)
    }
  },
  mounted() {
    this.value = this.valueParent;
  }
}
</script>
