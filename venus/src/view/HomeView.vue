<template>
  <div>
    <v-toolbar
      app
      color="primary"
      dark
      fixed
    >
      <v-text-field
        flat
        solo-inverted
        prepend-icon="search"
        label="搜索..."
      ></v-text-field>
    </v-toolbar>

    <v-content>
      <v-container fluid>
        <div style="text-align: center" v-if="isLoading">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </div>

        <v-card v-for="photo in photos" :key="photo.id" class="my-2">
          <v-card-media :src="photo.url" height="200px" @click="toPhotoItem(photo.id)">
          </v-card-media>
        </v-card>
      </v-container>
    </v-content>

    <v-bottom-nav
      app
      fixed
      :value="true"
      :active.sync="pageValue"
      color="white"
      class="bg-bottom-nav"
    >
      <v-btn flat color="primary" value="home">
        <span>首页</span>
        <v-icon>home</v-icon>
      </v-btn>

      <v-btn flat color="primary" value="find">
        <span>发现</span>
        <v-icon>explore</v-icon>
      </v-btn>

      <v-btn flat color="primary" value="me">
        <span>我的</span>
        <v-icon>person</v-icon>
      </v-btn>
    </v-bottom-nav>
  </div>
</template>

<script>
  import {getHotPhotos} from '../api/photo'
  import {CODE_SUCCESS} from '../api/constant'

  export default {
    data () {
      return {
        isLoading: false,
        photos: [],
        pageValue: 'home'
      }
    },
    created () {
      this.fetchData()
    },
    methods: {
      _getHotPhotos () {
        getHotPhotos().then(res => {
          if (res.code === CODE_SUCCESS) {
            // console.log(res.data)
            this.isLoading = false
            this.photos = res.data.content
          }
        })
      },
      fetchData () {
        this.isLoading = true
        this._getHotPhotos()
        // setTimeout(this._getHotPhotos, 1000)
      },
      toPhotoItem (photoId) {
        this.$router.push(`/photo/${photoId}`)
      }
    }
  }
</script>

<style scoped>
  .bg-bottom-nav {
    opacity: 0.95; /* work with color prop */
  }
</style>
