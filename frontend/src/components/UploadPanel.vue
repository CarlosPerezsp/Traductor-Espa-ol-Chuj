<template>
  <div class="w-full max-w-sm mt-8">
    <!-- Divider -->
    <div class="flex items-center gap-3 mb-5">
      <div class="flex-1 h-px bg-[#c8e6c9]"></div>
      <span class="text-xs text-[#2d8a4e] font-semibold uppercase tracking-widest">Cargar datos</span>
      <div class="flex-1 h-px bg-[#c8e6c9]"></div>
    </div>

    <!-- File input -->
    <label class="block text-xs font-semibold text-[#1a5c2a] uppercase tracking-widest mb-1.5 ml-1">
      Archivo Excel (.xlsx)
    </label>
    <div class="flex gap-2 mb-3">
      <label
        class="flex-1 flex items-center gap-2 rounded-2xl border border-[#c8e6c9] bg-white px-4 py-2.5 text-sm text-gray-500 cursor-pointer hover:border-[#2d8a4e] transition-colors shadow-sm truncate"
      >
        <svg class="w-4 h-4 shrink-0 text-[#2d8a4e]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2M12 12V4m0 0L8 8m4-4 4 4"/>
        </svg>
        <span class="truncate">{{ selectedFile ? selectedFile.name : 'Seleccionar archivo…' }}</span>
        <input type="file" accept=".xlsx,.xlsm" class="hidden" @change="onFileChange" />
      </label>
    </div>

    <!-- Category label (static for now) -->
    <p class="text-xs text-[#2d8a4e] ml-1 mb-4">Categoría: <strong>Números</strong></p>

    <!-- Upload button -->
    <button
      :disabled="!selectedFile || uploading"
      class="w-full bg-[#2d8a4e] hover:bg-[#1a5c2a] disabled:opacity-50 text-white font-semibold py-3 rounded-2xl shadow active:scale-95 transition-transform flex items-center justify-center gap-2"
      @click="uploadFile"
    >
      <span v-if="uploading" class="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full"></span>
      <span>{{ uploading ? 'Cargando…' : 'Cargar traducciones' }}</span>
    </button>

    <!-- Result -->
    <div v-if="result" class="mt-4 rounded-2xl border border-[#c8e6c9] bg-[#f0f7f2] px-4 py-3 text-sm text-[#1a5c2a] shadow-sm">
      <p class="font-semibold mb-1">Carga completada</p>
      <p>Insertadas: <strong>{{ result.inserted }}</strong></p>
      <p>Omitidas (duplicadas): <strong>{{ result.skipped }}</strong></p>
    </div>

    <!-- Error -->
    <p v-if="error" class="mt-3 text-red-600 text-xs text-center">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const selectedFile = ref(null)
const uploading = ref(false)
const result = ref(null)
const error = ref('')

function onFileChange(e) {
  result.value = null
  error.value = ''
  selectedFile.value = e.target.files[0] || null
}

async function uploadFile() {
  if (!selectedFile.value) return
  uploading.value = true
  error.value = ''
  result.value = null

  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try {
    const res = await fetch('/api/upload/excel', {
      method: 'POST',
      body: formData,
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`)
    result.value = data
  } catch (e) {
    error.value = e.message || 'Error al cargar el archivo'
  } finally {
    uploading.value = false
  }
}
</script>
