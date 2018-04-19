<template>
  <div>
    <v-toolbar
      app
      color="secondary"
      dark
      fixed
    >
      <v-btn icon @click="toPrevPage">
        <v-icon>arrow_back</v-icon>
      </v-btn>

      <v-toolbar-title>{{ tagName }}</v-toolbar-title>
    </v-toolbar>

    <v-content>
      <v-container fluid grid-list-md>
        <div style="text-align: center" v-if="isLoading">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </div>

        <v-layout row wrap>
          <v-flex v-for="photo in photos" :key="photo.id" xs12 sm6 md4 lg3 xl2>
            <v-card class="my-2">
              <v-card-media :src="photo.url" height="200px" @click="toPhotoItem(photo.id)">
              </v-card-media>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </div>
</template>

<script>
  import {getPhotosByTag} from '../api/photo'
  import {CODE_SUCCESS} from '../api/constant'

  export default {
    data () {
      return {
        isLoading: false,
        tagName: this.$route.params.name,
        photos: []
      }
    },
    created () {
      this.fetchData()
    },
    watch: {
      '$route': 'fetchData'
    },
    methods: {
      _getPhotosByTag () {
        getPhotosByTag(this.tagName).then(res => {
          if (res.code === CODE_SUCCESS) {
            this.isLoading = false
            this.photos = res.data
          }
        })
      },
      fetchData () {
        this.isLoading = true
        this._getPhotosByTag()
      },
      toPrevPage () {
        this.$router.go(-1)
      },
      toPhotoItem (photoId) {
        this.$router.push(`/photo/${photoId}`)
      }
    }
  }
</script>

<style scoped>

</style>
