<script setup>
defineEmits(['change'])
</script>

<template>
  <div class="w3-xxlarge">
    <p v-text="label"></p>
    <input class="w3-input w3-xxlarge" type="number" v-model="value" @input="onChanged()" />
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
