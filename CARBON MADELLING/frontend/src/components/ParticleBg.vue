<template>
  <canvas ref="c" class="fixed inset-0 -z-10"></canvas>
</template>
<script setup>
import { onMounted, ref } from 'vue';
const c = ref(null);
onMounted(() => {
  const canvas = c.value;
  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  function resize() {
    canvas.width = window.innerWidth * dpr;
    canvas.height = window.innerHeight * dpr;
  }
  resize();
  window.addEventListener('resize', resize);
  const leaves = Array.from({ length: 60 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    r: 1 + Math.random() * 2,
    vx: -0.15 - Math.random() * 0.15,
    vy: -0.1 + Math.random() * 0.2,
    a: 0.2 + Math.random() * 0.3,
  }));
  function tick() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    leaves.forEach(p => {
      ctx.fillStyle = `rgba(50,160,90,${p.a})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fill();
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0) p.x = canvas.width;
      if (p.y < 0) p.y = canvas.height;
      if (p.y > canvas.height) p.y = 0;
    });
    requestAnimationFrame(tick);
  }
  tick();
});
</script>
<style scoped>
canvas { pointer-events: none; }
</style> 