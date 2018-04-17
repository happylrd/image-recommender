// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import VueLazyload from 'vue-lazyload'
import App from './App'
import router from './router'

Vue.config.productionTip = false

Vue.use(Vuetify, {
  theme: {
    primary: '#00BCD4',
    secondary: '#0097A7',
    accent: '#FF4081',
    error: '#f44336',
    warning: '#ffeb3b',
    info: '#2196f3',
    success: '#4caf50'
  }
})

// TODO: will be removed later
Vue.use(VueLazyload)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
