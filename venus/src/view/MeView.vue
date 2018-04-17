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
      <v-container fluid>
        <div class="my-4" v-if="!curUser" @click="showDialog = true">
          <v-avatar size="48px">
            <v-icon x-large>account_circle</v-icon>
          </v-avatar>

          <span style="font-size: 18px" class="ml-2">点击登录</span>
        </div>

        <div class="my-4" v-if="curUser" @click="showDialog = true">
          <v-avatar
            size="48px"
          >
            <img :src="curUser.avatar" alt="avatar">
          </v-avatar>

          <span style="font-size: 18px" class="ml-2">{{ curUser.nickname }}</span>
        </div>

        <div v-if="curUser">

          <div style="font-size: 20px" class="mb-2">相关推荐</div>

          <v-card v-for="recPhoto in recPhotos" :key="recPhoto.id" class="my-2">
            <v-card-media :src="recPhoto.url" height="200px" @click="toPhotoItem(recPhoto.id)">
            </v-card-media>
          </v-card>
        </div>

        <div class="mt-4 mb-2" v-if="curUser">
          <v-btn color="error" block @click="doLogout()">退出登录</v-btn>
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
      <v-btn flat color="primary" value="home" @click="toHomeView">
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

    <v-dialog v-model="showDialog" persistent max-width="500">
      <v-card>
        <v-card-title class="headline">登录</v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>

              <v-flex xs12>
                <v-text-field
                  label="用户名"
                  v-model="username"
                ></v-text-field>
              </v-flex>

              <v-flex xs12>
                <v-text-field
                  label="密码"
                  v-model="password"
                  :append-icon="passwordVisible ? 'visibility' : 'visibility_off'"
                  :append-icon-cb="() => (passwordVisible = !passwordVisible)"
                  :type="passwordVisible ? 'password' : 'text'"
                ></v-text-field>
              </v-flex>

            </v-layout>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="warning" flat="flat" @click.native="showDialog = false">取消</v-btn>
          <v-btn color="primary" flat="flat" @click.native="doLogin">登录</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar
      bottom
      v-model="showLoginSnackbar"
    >
      登录成功
      <v-btn flat color="accent" @click.native="showLoginSnackbar = false">Close</v-btn>
    </v-snackbar>

    <v-snackbar
      bottom
      v-model="showLogoutSnackbar"
    >
      退出成功
      <v-btn flat color="accent" @click.native="showLogoutSnackbar = false">Close</v-btn>
    </v-snackbar>
  </div>
</template>

<script>
  import {login, getInfo, getRecPhotos} from '../api/user'
  import {CODE_SUCCESS} from '../api/constant'

  export default {
    data () {
      return {
        username: '',
        password: '',
        curUser: null,
        recPhotos: [],
        viewValue: 'me',
        showDialog: false,
        showLoginSnackbar: false,
        showLogoutSnackbar: false,
        passwordVisible: true
      }
    },
    created () {
      let token = localStorage.__v_token__
      let username = localStorage.__v_user_username__
      // console.log(`token: ${token}, username: ${username}`)
      if ((token !== undefined) && (username !== undefined)) {
        this._getInfo(username, token)
      }
    },
    methods: {
      doLogin () {
        this.showDialog = false
        this._login()
      },
      doLogout () {
        this.curUser = null
        this.showLogoutSnackbar = true
        localStorage.removeItem('__v_token__')
        localStorage.removeItem('__v_user_username__')
      },
      _login () {
        login(this.username, this.password).then(res => {
          this.showLoginSnackbar = true
          let token = res
          this._getInfo(this.username, token)
        })
      },
      _getInfo (username, token) {
        getInfo(username, token).then(res => {
          if (res.code === CODE_SUCCESS) {
            this.curUser = res.data
            localStorage.__v_token__ = token
            localStorage.__v_user_username__ = this.curUser.username
            this._getRecPhotos(token)
          }
        })
      },
      _getRecPhotos (token) {
        getRecPhotos(this.curUser.id, token).then(res => {
          if (res.code === CODE_SUCCESS) {
            this.recPhotos = res.data
          }
        })
      },
      toHomeView () {
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
