<template>
  <div>
    <v-toolbar
      app
      color="primary"
      dark
      fixed
    >
      <v-btn icon @click="toHomePage">
        <v-icon>close</v-icon>
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

            <span style="font-size: 18px" class="ml-2">{{ curPhoto.owner.nickname }}</span>
          </div>

          <div class="my-4">
            <v-chip outline color="secondary"
                    v-for="tag in curTags" :key="tag.id"
                    @click="toTagItem(tag.content)"
            >{{ tag.raw }}</v-chip>
          </div>

          <div style="font-size: 20px" class="mb-2">相关推荐</div>

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
  import {getTags} from '../api/tag'
  import {CODE_SUCCESS} from '../api/constant'

  export default {
    data () {
      return {
        isLoading: false,
        curPhoto: null,
        curTags: [],
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
            this.curPhoto = res.data
          }
        })
      },
      _getTags () {
        getTags(this.$route.params.id).then(res => {
          if (res.code === CODE_SUCCESS) {
            // console.log(res.data)
            this.curTags = res.data
          }
        })
      },
      _getRecPhotos () {
        getRecPhotos(this.$route.params.id).then(res => {
          if (res.code === CODE_SUCCESS) {
            this.isLoading = false
            this.recPhotos = res.data
          }
        })
      },
      fetchData () {
        this.isLoading = true
        this._getPhoto()
        this._getTags()
        this._getRecPhotos()
      },
      toHomePage () {
        this.$router.push('/')
      },
      toPhotoItem (photoId) {
        console.log('click')
        this.$router.push(`/photo/${photoId}`)
      },
      toTagItem (tagName) {
        this.$router.push(`/tag/${tagName}`)
      }
    }
  }
</script>

<style scoped>

</style>
