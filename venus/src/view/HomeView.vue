<template>
  <div>
    <v-toolbar
      app
      color="primary"
      dark
      fixed
    >
      <v-toolbar-title>Venus</v-toolbar-title>
    </v-toolbar>

    <v-content>
      <v-container fluid grid-list-md>
        <div v-infinite-scroll="loadMore" infinite-scroll-disabled="isBusy" infinite-scroll-distance="10">

          <v-layout row wrap>
            <v-flex v-for="photo in photos" :key="photo.id" xs12 sm6 md4 lg3 xl2>
              <v-card class="my-2">
                <v-card-media :src="photo.url" height="200px" @click="toPhotoItem(photo.id)">
                </v-card-media>
              </v-card>
            </v-flex>
          </v-layout>

          <div style="text-align: center" v-if="isLoading">
            <v-progress-circular indeterminate color="primary"></v-progress-circular>
          </div>
        </div>
      </v-container>
    </v-content>

    <v-bottom-nav
      app
      fixed
      :value="true"
      :active.sync="viewValue"
      color="white"
      class="bg-bottom-nav"
    >
      <v-btn flat color="primary" value="home">
        <span>首页</span>
        <v-icon>home</v-icon>
      </v-btn>

      <v-btn flat color="primary" value="find" @click="toFindView">
        <span>发现</span>
        <v-icon>explore</v-icon>
      </v-btn>

      <v-btn flat color="primary" value="me" @click="toMeView">
        <span>我的</span>
        <v-icon>person</v-icon>
      </v-btn>
    </v-bottom-nav>
  </div>
</template>

<script>
  import infiniteScroll from 'vue-infinite-scroll'
  import {getHotPhotos} from '../api/photo'
  import {CODE_SUCCESS} from '../api/constant'

  const PAGE_SIZE = 10

  export default {
    directives: {infiniteScroll},
    data () {
      return {
        isLoading: false,
        photos: [],
        isBusy: false,
        pageNum: 0,
        viewValue: 'home'
      }
    },
    created () {
    },
    methods: {
      loadMore () {
        this.isLoading = true
        this.isBusy = true
        this._getHotPhotos()
      },
      _getHotPhotos () {
        getHotPhotos(this.pageNum, PAGE_SIZE).then(res => {
          if (res.code === CODE_SUCCESS) {
            console.log(`Invoke getHotPhotos api by (pageNum:${this.pageNum}, pageSize:${PAGE_SIZE})`)
            this.isLoading = false
            this.photos = this.photos.concat(res.data.content)
            this.isBusy = false
            this.pageNum += 1
          }
        })
      },
      toPhotoItem (photoId) {
        this.$router.push(`/photo/${photoId}`)
      },
      toFindView () {
        this.$router.push('/find')
      },
      toMeView () {
        this.$router.push('/me')
      }
    }
  }
</script>

<style scoped>
  .bg-bottom-nav {
    opacity: 0.95; /* work with color prop */
  }
</style>
