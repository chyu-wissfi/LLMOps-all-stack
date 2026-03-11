<template>
  <div class="about">
    <h1>This is an about page</h1>
    <h1 class="text-3xl font-bold underline">Hello world!</h1>
    <p>Wissfi</p>
    <a-button type="primary">注册登录</a-button>
    <a-avatar :style="{ backgroundColor: '#3370ff' }">
      <IconUser />
    </a-avatar>
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
