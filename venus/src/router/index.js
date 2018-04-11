import Vue from 'vue'
import Router from 'vue-router'
import HomeView from '@/view/HomeView'
import PhotoItemView from '@/view/PhotoItem'
import TagItemView from '@/view/TagItem'

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
    },
    {
      path: '/tag/:name',
      component: TagItemView
    }
  ],
  scrollBehavior (to, from, savedPosition) {
    return {x: 0, y: 0}
  }
})
