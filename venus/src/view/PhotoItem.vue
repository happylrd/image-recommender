<template>
  <div>
    <v-toolbar
      app
      color="primary"
      dark
      fixed
    >
      <v-btn icon @click="toHomePage">
        <v-icon>arrow_back</v-icon>
      </v-btn>

      <v-toolbar-title v-if="curPhoto">{{curPhoto.title}}</v-toolbar-title>
    </v-toolbar>

    <v-content>
      <v-container fluid>
        <div style="text-align: center" v-if="isLoading">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </div>

        <div v-if="curPhoto">
          <v-card>
            <v-card-media :src="curPhoto.url" height="200px">
            </v-card-media>
          </v-card>

          <div class="my-4">
            <v-avatar
              size="48px"
            >
              <img :src="curPhoto.owner.avatar" alt="avatar">
            </v-avatar>

            <span style="font-size: 18px">{{ curPhoto.owner.nickname }}</span>
          </div>

          <div style="font-size: 20px" class="mb-2">可能也喜欢</div>

          <v-card v-for="recPhoto in recPhotos" :key="recPhoto.id" class="my-2">
            <v-card-media :src="recPhoto.url" height="200px" @click="toPhotoItem(recPhoto.id)">
            </v-card-media>
          </v-card>
        </div>
      </v-container>
    </v-content>
  </div>
</template>

<script>
  import {getPhoto, getRecPhotos} from '../api/photo'
  import {CODE_SUCCESS} from '../api/constant'

  export default {
    data () {
      return {
        isLoading: false,
        curPhoto: null,
        recPhotos: []
      }
    },
    created () {
      this.fetchData()
    },
    watch: {
      '$route': 'fetchData'
    },
    methods: {
      _getPhoto () {
        getPhoto(this.$route.params.id).then(res => {
          if (res.code === CODE_SUCCESS) {
            console.log(res.data)
            // this.isLoading = false
            this.curPhoto = res.data
          }
        })
      },
      _getRecPhotos () {
        getRecPhotos(this.$route.params.id).then(res => {
          if (res.code === CODE_SUCCESS) {
            // console.log(res.data)
            this.isLoading = false
            this.recPhotos = res.data
          }
        })
      },
      fetchData () {
        this.isLoading = true
        this._getPhoto()
        this._getRecPhotos()
      },
      toHomePage () {
        this.$router.push('/')
      },
      toPhotoItem (photoId) {
        console.log('click')
        this.$router.push(`/photo/${photoId}`)
      }
    }
  }
</script>

<style scoped>

</style>
