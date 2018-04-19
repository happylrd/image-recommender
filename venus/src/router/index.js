import Vue from 'vue'
import Router from 'vue-router'
import HomeView from '@/view/HomeView'
import FindView from '@/view/Find'
import MeView from '@/view/MeView'
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
      path: '/find',
      component: FindView
    },
    {
      path: '/me',
      component: MeView
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
