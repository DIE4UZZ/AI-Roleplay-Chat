# AI角色聊天项目依赖文档

## 项目简介
AI-Roleplay-Chat是一个基于Vue 3的现代化角色聊天应用，提供用户与AI角色进行交互的功能。

## 核心依赖

### 生产依赖

| 依赖名称 | 版本 | 用途 |
|---------|------|------|
| vue | ^3.3.4 | 核心前端框架，提供响应式视图渲染 |
| vue-router | ^4.5.1 | 路由管理，处理页面导航和组件切换 |
| pinia | ^3.0.3 | 状态管理库，管理应用的全局状态 |
| axios | ^1.12.2 | HTTP客户端，用于API请求和数据交互 |
| @types/node | ^24.5.2 | Node.js类型定义，提供TypeScript支持 |

### 开发依赖

| 依赖名称 | 版本 | 用途 |
|---------|------|------|
| typescript | ^5.0.2 | TypeScript语言支持，提供静态类型检查 |
| vite | ^4.4.5 | 现代前端构建工具，提供快速的开发体验和构建优化 |
| @vitejs/plugin-vue | ^4.2.3 | Vite的Vue插件，支持Vue组件的处理 |
| vue-tsc | ^1.8.5 | Vue的TypeScript编译器，检查Vue组件中的类型错误 |

## 安装说明

### 前置要求
- Node.js 16.x或更高版本
- npm、yarn或pnpm包管理器

### 安装步骤

1. 克隆项目仓库
```bash
git clone <repository-url>
cd AI-Roleplay-Chat/Fronted
```

2. 安装依赖
```bash
# 使用npm
npm install

# 或使用yarn
yarn install

# 或使用pnpm
pnpm install
```

3. 开发环境运行
```bash
npm run dev
```

4. 构建生产版本
```bash
npm run build
```

5. 预览生产构建
```bash
npm run preview
```

## 技术栈说明

### 前端框架
- **Vue 3**: 采用组合式API，提供更好的TypeScript集成和性能优化
- **Vue Router 4**: 支持Vue 3的路由库，提供动态路由和导航守卫
- **Pinia**: 轻量级状态管理库，替代Vuex，简化状态管理

### 开发工具
- **Vite**: 提供极速的开发服务器启动和热模块替换
- **TypeScript**: 提供静态类型检查，增强代码可维护性

### HTTP请求
- **Axios**: 处理API请求，支持拦截器、取消请求等高级功能

## 推荐IDE设置

- **VSCode** + **Volar**插件: 提供Vue 3语法高亮和智能提示
- **ESLint**: 代码质量检查
- **Prettier**: 代码格式化

## 浏览器兼容性

- Chrome (最新2个版本)
- Firefox (最新2个版本)
- Safari (最新2个版本)
- Edge (最新2个版本)