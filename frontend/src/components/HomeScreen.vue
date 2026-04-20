<template>
  <div class="flex flex-col items-center w-full px-5 pt-8 pb-10">

    <!-- Header -->
    <img
      src="/images/ALMGlogo.png"
      alt="ALMG Logo"
      class="w-28 h-28 object-contain mb-3"
    />
    <h1 class="text-lg font-bold text-[#1a5c2a] text-center leading-tight">
      Academia de Lenguas Mayas<br>de Guatemala
    </h1>
    <p class="text-sm text-[#2d8a4e] mt-1 mb-6 text-center">Traductor</p>

    <!-- Language bar -->
    <div class="w-full max-w-sm flex items-center justify-between bg-[#2d8a4e] rounded-2xl px-5 py-3 mb-5 shadow">
      <span class="text-white font-semibold text-sm tracking-wide">Español</span>
      <span class="text-white text-xl select-none">⇄</span>
      <span class="text-white font-semibold text-sm tracking-wide">Chuj</span>
    </div>

    <!-- Input box -->
    <div class="w-full max-w-sm mb-4">
      <label class="block text-xs font-semibold text-[#1a5c2a] uppercase tracking-widest mb-1.5 ml-1">
        Texto en Español
      </label>
      <textarea
        v-model="inputText"
        rows="4"
        placeholder="Escribe aquí el texto a traducir..."
        class="w-full rounded-2xl border border-[#c8e6c9] bg-white px-4 py-3 text-sm text-gray-700 resize-none focus:outline-none focus:ring-2 focus:ring-[#2d8a4e] placeholder-gray-400 shadow-sm"
      />
    </div>

    <!-- Translate button -->
    <button
      :disabled="translating || !inputText.trim()"
      class="w-full max-w-sm bg-[#1a5c2a] hover:bg-[#155224] disabled:opacity-50 text-white font-semibold py-3 rounded-2xl shadow active:scale-95 transition-transform mb-5 flex items-center justify-center gap-2"
      @click="translate"
    >
      <span v-if="translating" class="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full"></span>
      <span>{{ translating ? 'Traduciendo…' : 'Traducir' }}</span>
    </button>

    <!-- Result box -->
    <div class="w-full max-w-sm">
      <label class="block text-xs font-semibold text-[#1a5c2a] uppercase tracking-widest mb-1.5 ml-1">
        Resultado en Chuj
      </label>
      <textarea
        :value="resultText"
        rows="4"
        readonly
        placeholder="La traducción aparecerá aquí…"
        class="w-full rounded-2xl border border-[#c8e6c9] bg-[#f0f7f2] px-4 py-3 text-sm text-[#1a5c2a] resize-none focus:outline-none placeholder-[#a5c9ad] shadow-sm cursor-default"
      />
    </div>

    <!-- Error message -->
    <p v-if="error" class="mt-3 text-red-600 text-xs text-center">{{ error }}</p>

  </div>
</template>

<script setup>
import { ref } from 'vue'

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
