<template>
  <transition name="slide">
    <!-- Sử dụng internalShow để điều khiển hiển thị/ẩn thông báo -->
    <div v-if="internalShow" :class="['notification', notificationType]">
      <p>{{ message }}</p>
    </div>
  </transition>
</template>

<script setup>
import { ref, computed, watch } from "vue";

const props = defineProps({
  message: {
    type: String,
    required: true,
  },
  duration: {
    type: Number,
    default: 3000,
  },
  type: {
    type: String,
    default: "success",
  },
  show: {
    type: Boolean,
    required: true,
  },
});

const internalShow = ref(false);

// Theo dõi prop `show` để hiển thị hoặc ẩn thông báo
watch(
  () => props.show,
  (newVal) => {
    if (newVal) {
      internalShow.value = true;
      setTimeout(() => {
        internalShow.value = false;
      }, props.duration);
    }
  }
);

// Xác định kiểu thông báo dựa trên prop 'type'
const notificationType = computed(() => {
  return props.type === "error" ? "notification-error" : "notification-success";
});
</script>

<style scoped>
/* Thêm hiệu ứng chuyển động cho enter/leave */
.slide-enter-active,
.slide-leave-active {
  transition: transform 1s ease-in-out; /* Hiệu ứng chuyển động từ phải sang trái */
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%); /* Bắt đầu từ ngoài màn hình ở bên phải */
}

.notification {
  position: fixed;
  top: 0;
  right: 0;
  color: white;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  white-space: nowrap;
}

.notification-success {
  background-color: #4caf50;
}

.notification-error {
  background-color: #f44336;
}
</style>
