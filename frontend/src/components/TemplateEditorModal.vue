<template>
  <!-- Обычная полноэкранная страница -->
  <div class="min-h-screen bg-slate-900 text-slate-200 font-sans">
    
    <!-- Шапка редактора (прижата к верху) -->
    <div class="bg-slate-800 border-b border-slate-700 p-4 sticky top-0 z-10 shadow-lg">
      <div class="max-w-4xl mx-auto flex justify-between items-center">
        <div class="flex items-center gap-4">
          <button @click="$emit('close')" class="text-slate-400 hover:text-white transition font-bold">
            ← Назад
          </button>
          <input v-model="templateName" type="text" placeholder="Название шаблона" class="bg-slate-700 border border-slate-600 rounded px-3 py-2 w-64 focus:outline-none focus:border-cyan-500 text-lg">
        </div>
        <div class="flex gap-3">
          <button @click="$emit('close')" class="px-6 py-2 bg-slate-600 hover:bg-slate-500 rounded-lg font-bold transition">Отмена</button>
          <button @click="save" class="px-6 py-2 bg-cyan-600 hover:bg-cyan-500 rounded-lg font-bold transition">Сохранить</button>
        </div>
      </div>
    </div>

    <!-- Контент редактора -->
    <div class="max-w-4xl mx-auto p-6 space-y-10 pb-20">
      
      <!-- 1. Основной шаблон -->
      <div>
        <h3 class="text-xl font-semibold text-white mb-3 border-b border-slate-700 pb-2">1. Базовый конфиг</h3>
        
        <!-- ТУЛБАР С КНОПКАМИ -->
        <div class="flex items-center gap-2 mb-2 bg-slate-800 p-2 rounded border border-slate-700">
          <button @mousedown.prevent="createBlock" class="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 rounded text-xs font-bold transition shadow">📦 Выделить блок</button>
          <button @mousedown.prevent="createVariable" class="px-3 py-1.5 bg-purple-600 hover:bg-purple-500 rounded text-xs font-bold transition shadow">✏️ Заменить на переменную</button>
        </div>

        <textarea ref="mainTextArea" v-model="mainText" class="w-full h-96 bg-slate-900 p-4 font-mono text-sm focus:outline-none resize-y text-green-300 border border-slate-700 rounded-lg"></textarea>
      </div>

      <!-- 2. Переменные -->
      <div>
        <div class="flex justify-between items-center mb-4 border-b border-slate-700 pb-2">
          <h3 class="text-xl font-semibold text-white">2. Переменные</h3>
          <div class="flex gap-2 items-center">
            <button @click="addLocalVariable" class="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 rounded text-sm font-bold transition">+ Локальная</button>
            <select v-model="selectedGlobalVarName" @change="addGlobalVariable" class="bg-green-700 hover:bg-green-600 rounded text-sm font-bold transition text-white px-3 py-2 cursor-pointer">
              <option value="" disabled>+ Общая переменная</option>
              <option v-for="gv in availableGlobalVars" :key="gv.id" :value="gv.name">
                {{ gv.label }} ({{ gv.name }})
              </option>
              <option v-if="globalVars.length === 0" disabled>Нет общих переменных</option>
            </select>
          </div>
        </div>
        
        <div v-if="variables.length === 0" class="text-sm text-slate-500 italic text-center py-4 bg-slate-800 rounded-lg">Нет переменных.</div>
        
        <div class="space-y-3">
          <div 
            v-for="(v, index) in variables" 
            :key="index" 
            :class="['p-4 rounded-lg border grid grid-cols-12 gap-4 items-center', v.isGlobal ? 'bg-green-900/20 border-green-800' : 'bg-slate-800 border-slate-700']"
          >
            <div class="col-span-5">
              <label class="block text-xs mb-1" :class="v.isGlobal ? 'text-green-400' : 'text-slate-400'">Описание</label>
              <input v-model="v.label" type="text" :readonly="v.isGlobal" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-sm focus:outline-none" :class="v.isGlobal ? 'cursor-not-allowed opacity-80' : ''">
            </div>
            <div class="col-span-6 flex gap-2 items-center">
              <span class="text-slate-500 font-mono pt-5">{{ openBrace }}</span>
              <div class="flex-1">
                <label class="block text-xs mb-1" :class="v.isGlobal ? 'text-green-400' : 'text-slate-400'">Имя</label>
                <input v-model="v.name" type="text" :readonly="v.isGlobal" class="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2 text-sm focus:outline-none font-mono" :class="v.isGlobal ? 'text-green-300 cursor-not-allowed opacity-80' : 'text-cyan-300'">
              </div>
              <span class="text-slate-500 font-mono pt-5">{{ closeBrace }}</span>
            </div>
            <div class="col-span-1 flex justify-center pt-4">
              <button @click="variables.splice(index, 1)" class="text-red-400 hover:text-red-300 font-bold text-xl">&times;</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. Опции -->
      <div>
        <div class="flex justify-between items-center mb-4 border-b border-slate-700 pb-2">
          <h3 class="text-xl font-semibold text-white">3. Опции (варианты)</h3>
          <button @click="addOption" class="px-4 py-2 bg-purple-600 hover:bg-purple-500 rounded text-sm font-bold transition">+ Добавить опцию</button>
        </div>
        <div v-if="options.length === 0" class="text-sm text-slate-500 italic text-center py-4 bg-slate-800 rounded-lg">Нет опций.</div>
        
        <div class="space-y-6">
          <div v-for="(opt, index) in options" :key="index" class="bg-slate-800 p-4 rounded-lg border border-slate-700">
            <div class="flex justify-between items-center mb-3">
              <input v-model="opt.label" type="text" placeholder="Название опции (например: WAN_STATIC)" class="bg-slate-700 border border-slate-600 rounded px-3 py-2 w-1/2 focus:outline-none focus:border-cyan-500 text-sm">
              <button @click="options.splice(index, 1)" class="text-red-400 hover:text-red-300 text-sm font-bold">Удалить опцию</button>
            </div>
            <textarea v-model="opt.code" class="w-full h-64 bg-slate-900 p-4 font-mono text-sm focus:outline-none resize-y text-green-300 border border-slate-700 rounded-lg"></textarea>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const openBrace = '{{'
const closeBrace = '}}'

const props = defineProps({
  mode: String,
  editData: Object,
  globalVars: Array
})

const emit = defineEmits(['close', 'save'])

const templateName = ref('')
const mainText = ref('')
const variables = ref([])
const options = ref([])

// Ссылка на поле ввода для работы с выделением текста
const mainTextArea = ref(null)

const selectedGlobalVarName = ref('')

const availableGlobalVars = computed(() => {
  if (!props.globalVars) return []
  return props.globalVars.filter(gv => !variables.value.some(v => v.name === gv.name))
})

watch(() => props.editData, (newVal) => {
  if (props.mode === 'edit' && newVal) {
    templateName.value = newVal.name
    mainText.value = newVal.main_text
    variables.value = JSON.parse(JSON.stringify(newVal.variables || [])).map(v => ({
      ...v,
      isGlobal: props.globalVars ? props.globalVars.some(gv => gv.name === v.name) : false
    }))
    options.value = JSON.parse(JSON.stringify(newVal.options || []))
  } else {
    templateName.value = ''
    mainText.value = ''
    variables.value = []
    options.value = []
  }
}, { immediate: true })

const addLocalVariable = () => {
  variables.value.push({ name: '', label: '', isGlobal: false })
}

const addGlobalVariable = () => {
  if (!selectedGlobalVarName.value) return
  const selectedVar = props.globalVars.find(gv => gv.name === selectedGlobalVarName.value)
  if (selectedVar) {
    variables.value.push({ name: selectedVar.name, label: selectedVar.label, isGlobal: true })
  }
  selectedGlobalVarName.value = ''
}

const addOption = () => {
  options.value.push({ id: '', label: '', code: '' })
}

// --- ЛОГИКА РАБОТЫ С ВЫДЕЛЕНИЕМ ТЕКСТА ---

const createBlock = () => {
  const textarea = mainTextArea.value;
  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;
  
  if (start === end) {
    alert('Сначала выделите текст в поле базового конфига!');
    return;
  }

  // Считаем, сколько блоков уже есть в тексте, чтобы назвать следующий по порядку
  const matches = mainText.value.match(/\[BLOCK: /g);
  const blockNumber = matches ? matches.length + 1 : 1;

  const text = mainText.value;
  const selectedText = text.substring(start, end);
  
  // Автоматически вставляем номер блока
  mainText.value = text.substring(0, start) + `[BLOCK: ${blockNumber}]\n` + selectedText + text.substring(end);
}

const createVariable = () => {
  const textarea = mainTextArea.value;
  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;

  if (start === end) {
    alert('Сначала выделите значение в поле базового конфига, которое нужно заменить на переменную!');
    return;
  }

  let varName = prompt('Введите имя переменной (например: ip_address):');
  if (!varName) return;

  // ЗАЩИТА ОТ ПРОБЕЛОВ: Заменяем пробелы на подчеркивания для Jinja2
  const safeVarName = varName.replace(/\s+/g, '_').replace(/[^a-zA-Z0-9_]/g, '');
  if (!safeVarName) return;

  const text = mainText.value;
  // Заменяем выделенный текст на безопасную переменную
  mainText.value = text.substring(0, start) + `{{ ${safeVarName} }}` + text.substring(end);

  // Автоматически добавляем эту переменную в список локальных переменных
  if (!variables.value.some(v => v.name === safeVarName)) {
    variables.value.push({ name: safeVarName, label: varName, isGlobal: false });
  }
}

const save = () => {
  if (!templateName.value || !mainText.value) {
    alert('Заполните название и базовый конфиг!');
    return
  }
  const cleanVars = variables.value.filter(v => v.name.trim() !== '');
  const processedOptions = [];
  
  options.value.forEach(opt => {
    if (!opt.label || !opt.code) return;
    const optId = opt.label.replace(/\s+/g, '_').toUpperCase().replace(/[^A-Z0-9_]/g, '');
    processedOptions.push({ id: optId, label: opt.label, code: opt.code });
  });

  emit('save', {
    name: templateName.value,
    main_text: mainText.value,
    variables: cleanVars,
    options: processedOptions
  })
}
</script>
