<template>
  <div class="app-container">
    <!-- 路由视图，用于显示当前路由对应的组件 -->
    <router-view />
  </div>
</template>

<script setup lang="ts">
// App组件作为应用的根组件，主要用于显示路由视图
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}
</style>
