<template>
  <v-card>
    <v-snackbar
      v-model="snackbar"
      :color="color"
      :multi-line="mode === 'multi-line'"
      :timeout="timeout"
      :vertical="mode === 'vertical'"
      top
    >
      {{ text }}
    </v-snackbar>
  </v-card>
</template>

<script>
export default {
  name: 'infoSnackBar',
  props: ['snackProps'],
  delimiters: ['${', '}'],
  data () {
    return {
      snackbar: this.snackProps.display,
      color: this.snackProps.color,
      mode: this.snackProps.mode,
      timeout: this.snackProps.timeout,
      text: this.snackProps.text
    }
  },
  watch: {
    snackbar (val) {
      this.$emit('complete')
    }
  }
}
</script>
