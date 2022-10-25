import axios from 'axios'
import { ElMessageBox, ElMessage } from 'element-plus'

// 创建axios实例
const service = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

//请求拦截器：携带的token字段
service.interceptors.request.use(
  config => {
    // do something before request is sent
    config.headers=config.headers || {}
    if (localStorage.getItem('token')) {
      config.headers.token = localStorage.getItem('token') || ''
    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

//响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    console.log(res)
    console.log(res.status)
    //服务器响应失败在干什么,因为咱们真实服务器返回code  20000也有可能200
    if (res.code !== 20000 && res.code!=200) {
      ElMessage({
        message: res.message || 'Error',
        type: 'error',
        duration: 5 * 1000
      })

      // 50008: Illegal token; 50012: Other clients logged in; 50014: Token expired;
      if (res.code === 50008 || res.code === 50012 || res.code === 50014) {
        // to re-login
        ElMessageBox.confirm('You have been logged out, you can cancel to stay on this page, or log in again', 'Confirm logout', {
          confirmButtonText: 'Re-Login',
          cancelButtonText: 'Cancel',
          type: 'warning'
        }).then(() => {
          localStorage.dispatch('user/resetToken').then(() => {
            location.reload()
          })
        })
      }
      return ''
    } else {
    //服务器相应成功干什么
      return res
    }
  },
  error => {
    console.log('err' + error) // for debug
    ElMessage({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
