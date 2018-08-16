<template>
  <v-app dark>
    <v-content>
      <v-toolbar color="primary">
        <v-toolbar-title>
          {{rManager ? 'Risk Manager' : 'Risk Viewer'}}
        </v-toolbar-title>
        <v-divider
          class="mx-2"
          inset
          vertical
        >
        </v-divider>
        <v-btn
          round
          color="secondary"
          @click.native="changeView('manager')"
        >
          Risk Manager
        </v-btn>
        <v-divider
          class="mx-2"
          inset
          vertical
        >
        </v-divider>
        <v-btn
          round
          color="secondary"
          @click.native="changeView('viewer')"
        >
          Risk Viewer
        </v-btn>
      <v-divider
        class="mx-2"
        inset
        vertical
      >
      </v-divider>
      </v-toolbar>
      <risk-entry v-if="rManager"></risk-entry>
      <risk-viewer v-else></risk-viewer>
    </v-content>
  </v-app>
</template>

<script>
import riskEntry from './components/riskEntry'
import riskViewer from './components/riskViewer'

export default {
  name: 'riskApp',
  delimiters: ['${', '}'],
  data () {
    return {
      risks: [],
      rManager: true,
      loading: false,
      currentRisk: {},
      message: null,
      newRisk: { 'risk_class': null }
    }
  },
  components: {
    'risk-entry': riskEntry,
    'risk-viewer': riskViewer
  },
  mounted: function () {
  },
  methods: {
    changeView: function (dialog) {
      if (dialog === 'manager') {
        this.rManager = true
      } else if (dialog === 'viewer') {
        this.rManager = false
      } else {
        this.rManager = true
      }
    }
  }
}
</script>
