import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

// 导入路由
import router from './router'

// 导入Pinia状态管理
import pinia from './store'
import { useAuthStore } from './store/auth.store'

// 创建应用实例
const app = createApp(App)

// 使用插件
app.use(router)
app.use(pinia)

// 初始化用户认证状态
const authStore = useAuthStore()
authStore.initializeUserState()

// 挂载应用
app.mount('#app')
