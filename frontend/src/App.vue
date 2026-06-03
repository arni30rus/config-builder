<template>
  <div class="min-h-screen bg-slate-900 text-slate-200 font-sans">
    
    <!-- ВИД 1: ГЛАВНАЯ (Генератор) -->
    <div v-if="currentView === 'home'" class="p-6 flex flex-col items-center">
      <div class="w-full max-w-4xl flex flex-col gap-6">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
            ⚡ Конструктор конфигураций
          </h1>
          <button @click="currentView = 'manager'" class="px-6 py-2.5 bg-purple-600 hover:bg-purple-500 rounded-lg font-bold transition shadow">
            ⚙️ Редактор шаблонов
          </button>
        </div>

        <!-- Блок выбора шаблона -->
        <div class="bg-slate-800 rounded-xl border border-slate-700 p-6 shadow-lg">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-semibold text-cyan-400">Выберите шаблон</h2>
            <!-- Строка поиска -->
            <div class="relative">
              <input 
                type="text" 
                v-model="searchQuery" 
                placeholder="Поиск..." 
                class="bg-slate-700 border border-slate-600 rounded-lg pl-8 pr-3 py-1.5 text-sm focus:outline-none focus:border-cyan-500 w-48"
              >
              <span class="absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm">🔍</span>
            </div>
          </div>

          <div v-if="filteredTemplates.length > 0" class="space-y-1 max-h-64 overflow-y-auto pr-1">
            <div 
              v-for="tmpl in filteredTemplates" :key="tmpl.id" 
              @click="selectedTemplateId = tmpl.id"
              :class="['p-2 rounded-lg cursor-pointer transition border', selectedTemplateId === tmpl.id ? 'bg-cyan-900/30 border-cyan-500' : 'bg-slate-700 border-slate-600 hover:bg-slate-600']"
            >
              <!-- Уменьшенный шрифт для названия -->
              <span class="font-medium text-base text-slate-100">{{ tmpl.name }}</span>
            </div>
          </div>
          <div v-else class="text-center text-slate-400 italic py-4 text-sm">
            {{ templates.length > 0 ? 'Шаблоны не найдены по вашему запросу.' : 'Шаблонов пока нет. Создайте их в Редакторе.' }}
          </div>
        </div>

        <ConfigGenerator 
          v-if="currentTemplate"
          :options="currentOptions"
          :variables="currentVariables"
          :variableValues="variableValues"
          v-model:selectedOptionId="selectedOptionId"
          :isLoading="isLoading"
          :hasTemplate="!!currentTemplate"
          @update:variableValues="variableValues = $event"
          @generate="generateConfig"
        />
        
        <p v-if="error" class="text-red-400 text-sm text-center -mt-4">{{ error }}</p>
        <ConfigOutput :blocks="blocks" />
      </div>
    </div>

    <!-- ВИД 2: РЕДАКТОР ШАБЛОНОВ И ПЕРЕМЕННЫХ -->
    <div v-if="currentView === 'manager'" class="p-6">
      <div class="max-w-4xl mx-auto space-y-8">
        
        <div class="flex justify-between items-center">
          <button @click="currentView = 'home'" class="text-cyan-400 hover:text-cyan-300 transition font-bold">
            ← Назад к конструктору
          </button>
          <h1 class="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-500">
            Управление
          </h1>
          <div class="w-32"></div>
        </div>

        <!-- Блок: Общие переменные -->
        <div class="bg-slate-800 rounded-xl border border-slate-700 p-6 shadow-lg">
          <div class="flex justify-between items-center mb-4 border-b border-slate-700 pb-3">
            <h2 class="text-xl font-semibold text-white">1. Общие переменные</h2>
            <button @click="openGlobalVarEditor" class="px-4 py-2 bg-green-600 hover:bg-green-500 rounded text-sm font-bold transition">+ Добавить общую</button>
          </div>
          <div v-if="globalVars.length === 0" class="text-sm text-slate-500 italic text-center py-2">Нет общих переменных.</div>
          <div class="space-y-2">
            <div v-for="gv in globalVars" :key="gv.id" class="flex items-center justify-between bg-slate-700 p-3 rounded-lg">
              <div>
                <span class="font-mono text-cyan-300 text-sm">{{ gv.name }}</span> <span class="text-slate-400 mx-2">—</span> <span class="text-sm">{{ gv.label }}</span>
              </div>
              <button @click="deleteGlobalVar(gv.id)" class="text-red-400 hover:text-red-300 font-bold text-xs">Удалить</button>
            </div>
          </div>
        </div>

        <!-- Блок: Шаблоны -->
        <div class="bg-slate-800 rounded-xl border border-slate-700 p-6 shadow-lg">
          <div class="flex justify-between items-center mb-4 border-b border-slate-700 pb-3">
            <h2 class="text-xl font-semibold text-white">2. Шаблоны</h2>
            <button @click="openTemplateEditor('create')" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded text-sm font-bold transition">+ Создать шаблон</button>
          </div>
          <div v-if="templates.length === 0" class="text-sm text-slate-500 italic text-center py-2">Нет шаблонов.</div>
          <div class="space-y-3">
            <div v-for="tmpl in templates" :key="tmpl.id" class="bg-slate-700 p-4 rounded-lg flex justify-between items-center border border-slate-600">
              <span class="font-bold text-sm">{{ tmpl.name }}</span>
              <div class="flex gap-3">
                <button @click="openTemplateEditor('edit', tmpl)" class="px-4 py-1.5 bg-slate-600 hover:bg-slate-500 rounded text-xs font-bold transition">Изменить</button>
                <button @click="deleteTemplate(tmpl.id)" class="px-4 py-1.5 bg-red-700 hover:bg-red-600 rounded text-xs font-bold transition">Удалить</button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- ВИД 3: СТРАНИЦА РЕДАКТИРОВАНИЯ ШАБЛОНА -->
    <TemplateEditorPage 
      v-if="currentView === 'editor'" 
      :mode="editorMode" 
      :editData="editingTemplate"
      :globalVars="globalVars"
      @close="currentView = 'manager'" 
      @save="handleSaveTemplate" 
    />

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import ConfigGenerator from './components/ConfigGenerator.vue'
import ConfigOutput from './components/ConfigOutput.vue'
import TemplateEditorPage from './components/TemplateEditorModal.vue'

// Навигация
const currentView = ref('home')
const editorMode = ref('create')
const editingTemplate = ref(null)

// Данные
const templates = ref([])
const globalVars = ref([])
const selectedTemplateId = ref(null)
const variableValues = ref({})
const selectedOptionId = ref('')
const blocks = ref([])
const isLoading = ref(false)
const error = ref('')

// Поиск
const searchQuery = ref('')

const currentTemplate = computed(() => templates.value.find(t => t.id === selectedTemplateId.value))
const currentVariables = computed(() => currentTemplate.value ? currentTemplate.value.variables : [])
const currentOptions = computed(() => currentTemplate.value ? currentTemplate.value.options : [])

// Фильтрация шаблонов для поиска
const filteredTemplates = computed(() => {
  if (!searchQuery.value) return templates.value
  const query = searchQuery.value.toLowerCase()
  return templates.value.filter(t => t.name.toLowerCase().includes(query))
})

watch(selectedTemplateId, () => {
  variableValues.value = {}
  selectedOptionId.value = ''
  blocks.value = []
  error.value = ''
})

// --- API ЗАПРОСЫ ---
onMounted(async () => {
  await fetchTemplates()
  await fetchGlobalVars()
})

const fetchTemplates = async () => {
  try {
    const response = await fetch('/api/templates')
    if (response.ok) templates.value = await response.json()
  } catch (err) { console.error(err) }
}

// ИСПРАВЛЕНА ОШИБКА ЗДЕСЬ: Название функции во множественном числе
const fetchGlobalVars = async () => {
  try {
    const response = await fetch('/api/global-variables')
    if (response.ok) globalVars.value = await response.json()
  } catch (err) { console.error(err) }
}

const openGlobalVarEditor = async () => {
  const label = prompt('Введите описание общей переменной (например: Имя устройства):')
  if (!label) return
  const name = prompt('Введите системное имя (например, hostname):')
  if (!name) return

  try {
    const response = await fetch('/api/global-variables', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, label })
    })
    if (!response.ok) {
      const errData = await response.json()
      throw new Error(errData.detail || 'Ошибка')
    }
    await fetchGlobalVars() // ИСПРАВЛЕНА ОШИБКА ЗДЕСЬ
  } catch (err) {
    alert('Ошибка: ' + err.message)
  }
}

const deleteGlobalVar = async (id) => {
  if (!confirm('Удалить эту общую переменную?')) return
  await fetch(`/api/global-variables/${id}`, { method: 'DELETE' })
  await fetchGlobalVars()
}

const openTemplateEditor = (mode, template = null) => {
  editorMode.value = mode
  editingTemplate.value = template
  currentView.value = 'editor'
}

const handleSaveTemplate = async (templateData) => {
  try {
    let response;
    if (editorMode.value === 'create') {
      response = await fetch('/api/templates', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(templateData)
      })
    } else {
      response = await fetch(`/api/templates/${editingTemplate.value.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(templateData)
      })
    }

    if (!response.ok) {
      const errData = await response.json()
      throw new Error(JSON.stringify(errData.detail) || 'Ошибка сохранения');
    }

    await fetchTemplates()
    currentView.value = 'manager'
  } catch (err) {
    alert('Ошибка при сохранении: ' + err.message)
  }
}

const deleteTemplate = async (id) => {
  if (!confirm('Удалить этот шаблон?')) return
  await fetch(`/api/templates/${id}`, { method: 'DELETE' })
  await fetchTemplates()
  if (selectedTemplateId.value === id) selectedTemplateId.value = null
}

const generateConfig = async () => {
  if (!currentTemplate.value) return;
  error.value = ''
  blocks.value = []
  isLoading.value = true

  try {
    const finalVariables = { ...variableValues.value };
    currentOptions.value.forEach(opt => {
      finalVariables[opt.id] = (selectedOptionId.value === opt.id);
    });

    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        template_id: currentTemplate.value.id,
        variables: finalVariables
      })
    })

    if (!response.ok) {
      const errData = await response.json()
      throw new Error(errData.detail || 'Ошибка сервера')
    }
    const data = await response.json()
    blocks.value = parseBlocks(data.rendered_config)
  } catch (err) {
    error.value = `Ошибка: ${err.message}`
  } finally {
    isLoading.value = false
  }
}

const parseBlocks = (text) => {
  const result = []
  const regex = /\[BLOCK: (.*?)\]\n/g
  let match;
  while ((match = regex.exec(text)) !== null) result.push({ title: match[1].trim(), content: '' });
  const sections = text.split(/\[BLOCK: .*?\]\n/)
  for (let i = 0; i < result.length; i++) result[i].content = sections[i + 1] ? sections[i + 1].trim() : ''
  if (result.length === 0 && text.trim().length > 0) result.push({ title: 'Полный конфиг', content: text.trim() })
  return result
}
</script>
