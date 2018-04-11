import Vue from 'vue'
import Router from 'vue-router'
import HomeView from '@/view/HomeView'
import PhotoItemView from '@/view/PhotoItem'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: HomeView
    },
    {
      path: '/photo/:id',
      component: PhotoItemView
    }
  ],
  scrollBehavior (to, from, savedPosition) {
    return {x: 0, y: 0}
  }
})
