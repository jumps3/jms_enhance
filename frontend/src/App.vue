<template>
  <div>
    <el-container class="tac">
      <el-header>
        <!-- 菜单栏 -->
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleMenuSelect">
          <el-menu-item index="settings">配置</el-menu-item>
          <el-menu-item index="users" :disabled="unset">用户</el-menu-item>
          <el-menu-item index="assets" :disabled="unset">资产</el-menu-item>
          <el-menu-item index="perms" :disabled="unset">授权</el-menu-item>
        </el-menu>
      </el-header>
      <el-main class="content">
        <!-- 根据菜单选项展示不同的页面内容 -->
        <div v-show="activeIndex === 'settings'">
          <el-form ref="form" :model="form" label-width="150px">
            <el-form-item required label="JumpServer站点">
              <el-input v-model="form.jms_base_url" clearable></el-input>
            </el-form-item>
            <el-form-item required label="Access Key">
              <el-input v-model="form.jms_access_key" clearable></el-input>
            </el-form-item>
            <el-form-item required label="Access Secret">
              <el-input v-model="form.jms_access_secret" show-password></el-input>
            </el-form-item>
            <el-form-item v-show="set_error">
              <span style="color: red">配置信息错误，请检查后再试！</span>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit" :loading="loading">提交</el-button>
            </el-form-item>
          </el-form>
        </div>
        <div v-show="activeIndex !== 'settings'">
          <el-row>
            <a :href="tplUrl" class="btn tpl">
              <el-button type="info">下载模板</el-button>
            </a>
          </el-row>
          <el-upload
              class="upload-demo"
              drag
              :action="uploadUrl"
              :on-success="handleUploadSuccess"
              :before-upload="beforeUpload">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将 <strong style="color: orangered">{{uploadType}}</strong> 文件拖到此处，或 <em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">只能上传 <strong>xlsx/csv</strong> 文件</div>
          </el-upload>
          <el-row class="result">
            <span style="color: red" v-show="exception !== undefined">处理失败：{{exception}}</span>
            <span v-show="result !== undefined" >
              成功 <span style="color: green">{{result.成功 ? result.成功:0}}</span> ， 失败 <span style="color: red">{{result.失败 ? result.失败:0}}</span>，查看详情请 <a :href="result.url">下载结果</a>
            </span>
          </el-row>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      loading: false,
      activeIndex: 'settings',
      form: {},
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
        assets: undefined,
        perms: undefined,
      },
      lanMap: {
        settings: '配置',
        users: '用户',
        assets: '资产',
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
      this.loading = true
      axios.get(this.baseUrl + '/api/settings').then(res => {
        this.loading = false
        this.form = res.data
        if (this.form.jms_base_url !== '') {
          this.unset = false
          this.handleMenuSelect('users')
        }
      })
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
      axios.post(this.baseUrl+'/api/settings', this.form, {
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
      // 处理文件上传成功的逻辑
      if (response.code === 200) {
        this.downloadReady = false
        res['url'] = this.baseUrl + `/api/result/${res.filename}`
        this.result = res
        this.resultMap[this.activeIndex] = res

        this.$message({
          type: 'success',
          message: `创建成功，请下载结果查看详情！`
        });
      }else {
        this.exception = res.exception
        this.resultMap[this.activeIndex] = res
        this.$message({
          type: 'error',
          message: `批量创建失败，${res.exception}`
        });
      }
    },
    beforeUpload(file) {
      // 文件上传前的校验逻辑
      console.log('上传文件前检验')

    }
  }
};
</script>

<style>
/* 可以根据需要添加样式 */
.tac {
  width: 30vw;
  display: flex;
  justify-content: flex-start;
}
.content {
  padding-left: 10px;
}
.btn {
  margin-bottom: 20px;
}
.result {
  margin-top: 20px;
}
</style>