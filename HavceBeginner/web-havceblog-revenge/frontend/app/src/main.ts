import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/output.css'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  faUser,
  faHome,
  faPenToSquare,
  faTrash,
  faUsers,
  faFileLines,
  faArrowRight,
  faExternalLinkAlt,
  faNewspaper,
  faSync,
  faSpinner
} from '@fortawesome/free-solid-svg-icons'

library.add(
  faUser,
  faHome,
  faPenToSquare,
  faTrash,
  faUsers,
  faFileLines,
  faArrowRight,
  faExternalLinkAlt,
  faNewspaper,
  faSync,
  faSpinner
)

const app = createApp(App)
app.use(router)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')
