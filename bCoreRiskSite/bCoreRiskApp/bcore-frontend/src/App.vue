<template>
  <v-app dark>
    <v-content>
      <v-toolbar color="primary">
        <v-toolbar-title>Risk Manager</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon>
          <v-icon>search</v-icon>
        </v-btn>
        <v-btn icon>
          <v-icon>apps</v-icon>
        </v-btn>
        <v-btn icon>
          <v-icon>refresh</v-icon>
        </v-btn>
        <v-btn icon>
          <v-icon>more_vert</v-icon>
        </v-btn>
      </v-toolbar>
      <risk-entry></risk-entry>
    </v-content>
  </v-app>
</template>

<script>
import riskEntry from './components/riskEntry'

export default {
  name: 'riskApp',
  delimiters: ['${', '}'],
  data () {
    return {
      risks: [],
      loading: false,
      currentRisk: {},
      message: null,
      newRisk: { 'risk_class': null }
    }
  },
  components: {
    'risk-entry': riskEntry
  },
  mounted: function () {
  },
  methods: {
  }
}

</script>
