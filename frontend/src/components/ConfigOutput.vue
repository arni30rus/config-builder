<template>
  <div v-if="blocks.length > 0" class="bg-slate-800 rounded-xl border border-slate-700 shadow-lg overflow-hidden">
    <div class="p-4 border-b border-slate-700 flex justify-between items-center">
      <h2 class="text-lg font-semibold text-cyan-400">Готовая конфигурация</h2>
      <button @click="copyAll" class="px-4 py-1 bg-green-600 hover:bg-green-500 rounded font-bold text-xs transition shadow">📋 Скопировать всё</button>
    </div>
    <div v-for="(block, index) in blocks" :key="index" class="border-b border-slate-700 last:border-b-0">
      <div class="flex justify-between items-center bg-slate-700/30 px-4 py-1">
        <h3 class="font-bold text-cyan-300 text-xs">{{ block.title }}</h3>
        <button @click="copyToClipboard(block.content, block.title)" class="px-3 py-0.5 bg-green-700 hover:bg-green-600 rounded text-xs font-bold transition">Скопировать блок</button>
      </div>
      <pre class="p-4 text-sm text-slate-200 whitespace-pre-wrap overflow-x-auto font-mono leading-relaxed">{{ block.content }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Единый вызов defineProps. Сохраняем в переменную props, чтобы использовать в методах ниже
const props = defineProps({
  blocks: Array
})

const copiedNotice = ref('')
const emit = defineEmits(['error'])

const copyToClipboard = async (text, title) => {
  try {
    await navigator.clipboard.writeText(text)
    copiedNotice.value = `Блок "${title}" скопирован!`
    setTimeout(() => copiedNotice.value = '', 2000)
  } catch (err) {
    alert('Не удалось скопировать')
  }
}

const copyAll = async () => {
  // Теперь props доступен, так как мы сохранили его выше
  const fullConfig = props.blocks.map(b => b.content).join('\n!\n')
  await copyToClipboard(fullConfig, 'Весь конфиг')
}
</script>
