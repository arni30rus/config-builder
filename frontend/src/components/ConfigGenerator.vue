<template>
  <div>
    <!-- Опции (Радиокнопки) -->
    <div v-if="options.length > 0" class="bg-slate-800 rounded-xl border border-slate-700 p-6 shadow-lg mb-6">
      <h2 class="text-lg font-semibold text-cyan-400 mb-4">Варианты конфигурации</h2>
      <div class="flex flex-wrap gap-4">
        <div v-for="opt in options" :key="opt.id" class="flex items-center gap-2 bg-slate-700 p-3 rounded-lg cursor-pointer hover:bg-slate-600 transition">
          <input type="radio" :id="opt.id" :value="opt.id" :checked="selectedOptionId === opt.id" @change="$emit('update:selectedOptionId', opt.id)" class="w-4 h-4 text-cyan-500 bg-slate-600 border-slate-500 focus:ring-cyan-500 cursor-pointer">
          <label :for="opt.id" class="text-sm font-medium cursor-pointer">{{ opt.label }}</label>
        </div>
      </div>
    </div>

    <!-- Переменные -->
    <div v-if="variables.length > 0" class="bg-slate-800 rounded-xl border border-slate-700 p-6 shadow-lg mb-6">
      <h2 class="text-lg font-semibold text-cyan-400 mb-4">Параметры</h2>
      <div class="grid grid-cols-2 gap-x-6 gap-y-4">
        <!-- Выводим label, а биндимся к name -->
        <div v-for="varItem in variables" :key="varItem.name">
          <label class="block text-sm font-medium text-slate-300 mb-1">{{ varItem.label }}</label>
          <input 
            type="text" 
            :value="variableValues[varItem.name]" 
            @input="updateVariable(varItem.name, $event.target.value)" 
            class="w-full bg-slate-700 border border-slate-600 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-cyan-500" 
            :placeholder="varItem.label"
          >
        </div>
      </div>
    </div>

    <!-- Кнопка генерации -->
    <button @click="$emit('generate')" :disabled="isLoading || !hasTemplate" class="w-full py-3 bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-400 hover:to-blue-400 rounded-lg font-bold text-lg text-white shadow-lg transition disabled:opacity-40">
      {{ isLoading ? 'Генерация...' : 'Сгенерировать конфигурацию' }}
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  options: Array,
  variables: Array, // Теперь это массив объектов { name, label }
  variableValues: Object,
  selectedOptionId: String,
  isLoading: Boolean,
  hasTemplate: Boolean
})

const emit = defineEmits(['update:selectedOptionId', 'update:variableValues', 'generate'])

const updateVariable = (varName, value) => {
  const newValues = { ...props.variableValues, [varName]: value };
  emit('update:variableValues', newValues);
}
</script>
