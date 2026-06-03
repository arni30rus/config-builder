<template>
  <div class="bg-slate-800 rounded-xl border border-slate-700 p-6 shadow-lg">
    <div class="flex gap-4">
      <button @click="$emit('create')" class="px-6 py-2.5 bg-blue-600 hover:bg-blue-500 rounded-lg font-bold transition shadow">
        + Создать шаблон
      </button>
      <div class="flex-1 flex gap-2">
        <select :value="modelValue" @change="$emit('update:modelValue', $event.target.value)" class="flex-1 bg-slate-700 border border-slate-600 rounded-lg px-4 py-2 focus:outline-none focus:border-cyan-500">
          <option :value="null" disabled>Выберите сохраненный шаблон...</option>
          <option v-for="tmpl in templates" :key="tmpl.id" :value="tmpl.id">{{ tmpl.name }}</option>
        </select>
        <button @click="$emit('edit')" :disabled="!modelValue" class="px-4 py-2 bg-slate-600 hover:bg-slate-500 rounded-lg font-bold transition shadow disabled:opacity-40">
          Изменить
        </button>
        <button @click="$emit('delete')" :disabled="!modelValue" class="px-4 py-2 bg-red-600 hover:bg-red-500 rounded-lg font-bold transition shadow disabled:opacity-40">
          Удалить
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  templates: Array,
  modelValue: [String, Number, null] // ID может быть числом из БД или null
})
defineEmits(['update:modelValue', 'create', 'edit', 'delete'])
</script>
