<template>
  <div>
    {{ this.$store.state.verification }}
    <button @click="() => this.$store.commit('verificationGet', 'wws')">
      按钮
    </button>
  </div>
</template>

<script>
import service from "../utils/request.js";

export default {};
</script>
