<template>
  <div class="flex flex-col items-center w-full px-5 md:px-8 lg:px-12 pt-8 pb-10">

    <!-- Header -->
    <img
      src="/images/ALMGlogo.png"
      alt="ALMG Logo"
      class="w-20 h-20 md:w-28 md:h-28 object-contain mb-3"
    />
    <h1 class="text-lg md:text-2xl lg:text-3xl font-bold text-[#1a5c2a] text-center leading-tight">
      Academia de Lenguas Mayas<br>de Guatemala
    </h1>
    <p class="text-sm md:text-base text-[#2d8a4e] mt-1 mb-6 text-center">Traductor</p>

    <!-- Language bar -->
    <div class="w-full max-w-sm md:max-w-xl lg:max-w-2xl flex items-center justify-between bg-[#2d8a4e] rounded-2xl px-5 py-3 mb-5 shadow">
      <span class="text-white font-semibold text-sm md:text-base tracking-wide">Español</span>
      <span class="text-white text-xl select-none">⇄</span>
      <span class="text-white font-semibold text-sm md:text-base tracking-wide">Chuj</span>
    </div>

    <!-- Input / Output grid (2 columns on lg+) -->
    <div class="w-full max-w-sm md:max-w-xl lg:max-w-2xl lg:grid lg:grid-cols-2 lg:gap-6 mb-4">

      <!-- Input box -->
      <div class="w-full mb-4 lg:mb-0">
        <label class="block text-xs font-semibold text-[#1a5c2a] uppercase tracking-widest mb-1.5 ml-1">
          Texto en Español
        </label>
        <textarea
          v-model="inputText"
          rows="4"
          placeholder="Escribe aquí el texto a traducir..."
          class="w-full rounded-2xl border border-[#c8e6c9] bg-white px-4 py-3 text-sm text-gray-700 resize-none focus:outline-none focus:ring-2 focus:ring-[#2d8a4e] placeholder-gray-400 shadow-sm lg:h-36"
        />
      </div>

      <!-- Result box -->
      <div class="w-full">
        <label class="block text-xs font-semibold text-[#1a5c2a] uppercase tracking-widest mb-1.5 ml-1">
          Resultado en Chuj
        </label>
        <textarea
          :value="resultText"
          rows="4"
          readonly
          placeholder="La traducción aparecerá aquí…"
          class="w-full rounded-2xl border border-[#c8e6c9] bg-[#f0f7f2] px-4 py-3 text-sm text-[#1a5c2a] resize-none focus:outline-none placeholder-[#a5c9ad] shadow-sm cursor-default lg:h-36"
        />
      </div>

    </div>

    <!-- Translate button -->
    <button
      :disabled="translating || !inputText.trim()"
      class="w-full max-w-sm md:max-w-xl lg:max-w-2xl bg-[#1a5c2a] hover:bg-[#155224] disabled:opacity-50 text-white font-semibold py-3 rounded-2xl shadow active:scale-95 transition-transform mb-5 flex items-center justify-center gap-2"
      @click="translate"
    >
      <span v-if="translating" class="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full"></span>
      <span>{{ translating ? 'Traduciendo…' : 'Traducir' }}</span>
    </button>

    <!-- Error message -->
    <p v-if="error" class="mt-3 text-red-600 text-xs text-center">{{ error }}</p>

    <!-- Upload Panel -->
    <UploadPanel />

  </div>
</template>

<script setup>
import { ref } from 'vue'
import UploadPanel from './UploadPanel.vue'

const inputText = ref('')
const resultText = ref('')
const translating = ref(false)
const error = ref('')

async function translate() {
  translating.value = true
  error.value = ''
  resultText.value = ''
  try {
    const res = await fetch('/api/translate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: inputText.value.trim(),
        source_lang: 'es',
        target_lang: 'chuj'
      })
    })
    if (res.status === 404) throw new Error('Traducción no encontrada')
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    resultText.value = data.target_text
  } catch (e) {
    error.value = e.message || 'Error al conectar con el servidor'
  } finally {
    translating.value = false
  }
}
</script>
