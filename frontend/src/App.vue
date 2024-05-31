<template>
  <el-container class="layout-container-demo">
    <el-header style="font-size: 12px">
      <el-image src="/logo.png"></el-image>
    </el-header>
    <el-container>
      <el-aside width="200px">
        <el-scrollbar>
          <el-menu :default-openeds="['assetGroup']" :default-active="activeIndex" @select="handleMenuSelect">
            <el-menu-item index="settings">配置</el-menu-item>
            <el-menu-item index="users" :disabled="unset">用户</el-menu-item>
            <el-sub-menu index="assetGroup">
              <template #title>资产</template>
              <el-menu-item index="hosts" :disabled="unset">主机</el-menu-item>
              <el-menu-item index="databases" :disabled="true">数据库</el-menu-item>
            </el-sub-menu>
            <el-menu-item index="perms" :disabled="unset">授权</el-menu-item>
          </el-menu>
        </el-scrollbar>
      </el-aside>
      <el-container class="main-container">
        <el-divider>基于 v3.10.10</el-divider>
        <!-- 根据菜单选项展示不同的页面内容 -->
        <el-main v-if="activeIndex === 'settings'" class="container-settings">
          <el-form :model="config" label-width="auto" style="max-width: 500px">
            <el-form-item required label="JumpServer站点">
              <el-input v-model="config.jms_base_url" clearable></el-input>
            </el-form-item>
            <el-form-item required label="Access Key">
              <el-input v-model="config.jms_access_key" clearable></el-input>
            </el-form-item>
            <el-form-item required label="Access Secret">
              <el-input v-model="config.jms_access_secret" show-password></el-input>
            </el-form-item>
            <el-form-item v-show="set_error">
              <span style="color: red">配置信息错误，请检查后再试！</span>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit" class="onSubmit">提交</el-button>
            </el-form-item>
          </el-form>
        </el-main>
        <el-main v-if="activeIndex !== 'settings'" class="container-bus" >
          <el-row>
            <a :href="tplUrl" class="btn tpl">
              <el-button type="info">下载模板</el-button>
            </a>
          </el-row>
          <el-row v-loading="loading" element-loading-text="拼命处理中">
            <el-upload
                class="upload-demo"
                drag
                :action="uploadUrl"
                :show-file-list="false"
                :on-success="handleUploadSuccess"
                :before-upload="beforeUpload">
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">将 <strong style="color: orangered">{{uploadType}}</strong> 文件拖到此处，或 <em>点击上传</em></div>
              <div class="el-upload__tip" slot="tip">只能上传 <strong>xlsx/csv</strong> 文件</div>
            </el-upload>
          </el-row>
          <el-row class="result">
            <el-text style="color: red" v-show="exception !== undefined">处理失败：{{exception}}</el-text>
            <el-text v-show="result !== undefined" >
            成功 <el-text type="success">{{result.成功 ? result.成功:0}}</el-text> ， 失败 <el-text type="danger">{{result.失败 ? result.失败:0}}</el-text>，查看详情请 <el-link :href="result.url" type="primary">下载结果</el-link>
            </el-text>
          </el-row>
        </el-main>
        <el-footer>Footer</el-footer>
      </el-container>
    </el-container>

  </el-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      loading: true,
      activeIndex: 'settings',
      config: {
        jms_base_url: '',
        jms_access_key: '',
        jms_access_secret: ''
      },
      unset: true,
      set_error: false,
      downloadReady: true,
      uploadType: '',
      baseUrl: '',
      uploadUrl: '',
      tplUrl: '',
      result: undefined,
      exception: undefined,
      resultMap: {
        users: undefined,
        hosts: undefined,
        databases: undefined,
        perms: undefined,
      },
      lanMap: {
        settings: '配置',
        users: '用户',
        hosts: '主机',
        databases: '数据库',
        perms: '权限',
      }
    };
  },
  created() {
    this.handleMenuSelect(this.activeIndex)
    this.initSettings()
  },
  methods: {
    initSettings() {
      axios.get(this.baseUrl + '/api/settings').then(res => {
        this.loading = false
        this.config = res.data
        if (this.config !== undefined && this.config.jms_base_url !== '') {
          this.unset = false
          this.handleMenuSelect('users')
        }
      })
      console.log(this.activeIndex)
    },
    handleMenuSelect(index) {
      this.downloadReady = true
      this.activeIndex = index

      this.uploadType = this.lanMap[index]
      this.uploadUrl = this.baseUrl + '/api/' + index + '/upload'
      this.tplUrl = this.baseUrl + '/api/' + index + '/tpl'
      // 获取缓存的结果文件下载地址
      this.result = this.resultMap[index]
    },
    onSubmit() {
      axios.post(this.baseUrl+'/api/settings', this.config, {
        headers: { 'Content-Type': 'application/json' }
      }).then(response => {
        const res = response.data
        if (res.code === 200) {
          this.$message({
            type: 'success',
            message: `JumpServer连接信息设置成功！`
          });

          this.unset = false
          this.activeIndex = 'users'
          this.set_error = false
          this.handleMenuSelect(this.activeIndex)
        }else {
          this.set_error = true
          this.$message({
            type: 'error',
            message: `JumpServer连接信息设置失败，${res.msg}`
          });
        }
      })
    },
    handleUploadSuccess(response, file) {
      let res = this.resultMap[this.activeIndex]
      res = response.data
      this.loading = false
      // 处理文件上传成功的逻辑
      if (response.code === 200) {
        this.downloadReady = false
        res['url'] = this.baseUrl + `/results/${res.filename}`
        this.result = res
        this.resultMap[this.activeIndex] = res

        this.$message({
          type: 'success',
          message: `处理完成，请下载结果查看详情！`
        });
      }else {
        this.exception = res.exception
        this.resultMap[this.activeIndex] = res
        this.$message({
          type: 'error',
          message: `处理失败，${res.exception}`
        });
      }
    },
    beforeUpload(file) {
      // 文件上传前的校验逻辑
      console.log('上传文件前检验')
      this.result = undefined
      this.resultMap[this.activeIndex] = undefined
      this.loading = true
    }
  }
};
</script>

<style>
/* 可以根据需要添加样式 */
/* loading 遮罩 */
body {
  margin: 0;
}

.layout-container-demo {
  border: 1px solid black;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vw;
}

.layout-container-demo .el-header {
  text-align: left;
  position: relative;
  background-color: rgb(0,132,107);
  color: black;
  height: 50px;
}

.layout-container-demo .el-header .el-image {
  width: 200px;
  padding: 5px 0;
  vertical-align: middle;
}

.layout-container-demo .el-aside {
  height: 100%;
  position: relative;
  background-color: #ffffff;
  color: white;
}

.layout-container-demo .main-container {
  padding: 0 10px;
}

.layout-container-demo .main-container .container-bus {
  text-align: center;
}

.layout-container-demo .main-container .container-bus .el-row {
  padding-top: 10px;
  padding-bottom: 10px;
}

</style>