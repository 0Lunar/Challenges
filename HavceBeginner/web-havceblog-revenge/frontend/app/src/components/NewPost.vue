<template>
    <div class="min-h-screen bg-gray-900">
        <Navbar />
        <div class="container mx-auto px-4 py-8">
            <div class="max-w-4xl mx-auto">
                <!-- Titolo e pulsante indietro -->
                <div class="flex justify-between items-center mb-8">
                    <h1 class="text-3xl font-bold text-white">Crea un nuovo post</h1>
                    <router-link to="/"
                        class="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors">
                        Annulla
                    </router-link>
                </div>

                <!-- Form di creazione -->
                <div class="bg-gray-800 rounded-xl shadow-lg p-6 mb-6">
                    <form @submit.prevent="submitPost">
                        <!-- Titolo -->
                        <div class="mb-6">
                            <label for="title" class="block text-gray-300 mb-2">Titolo</label>
                            <input type="text" id="title" v-model="post.title"
                                class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                                placeholder="Inserisci un titolo accattivante..." required />
                        </div>

                        <!-- Contenuto -->
                        <div class="mb-6">
                            <label for="content" class="block text-gray-300 mb-2">Contenuto</label>
                            <textarea id="content" v-model="post.content" rows="10"
                                class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                                placeholder="Scrivi il contenuto del post qui..." required></textarea>
                        </div>

                        <!-- Pulsanti -->
                        <div class="flex justify-end space-x-4">
                            <button type="button" @click="resetForm"
                                class="bg-gray-600 hover:bg-gray-500 text-white px-6 py-2 rounded-lg transition-colors">
                                Resetta
                            </button>
                            <button type="submit"
                                class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded-lg transition-colors">
                                Pubblica Post
                            </button>
                        </div>
                    </form>
                </div>

                <!-- Messaggio di stato -->
                <div v-if="message"
                    :class="['p-4 rounded-lg mb-6', message.type === 'success' ? 'bg-green-800 text-green-100' : 'bg-red-800 text-red-100']">
                    {{ message.text }}
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from './utils/Navbar.vue'
import axios from "axios";

const router = useRouter()

const post = ref({
    title: '',
    content: '',
})

const message = ref(null)

const submitPost = async () => {
    try {
        console.log('Post da inviare:', post.value)

        const token = `Bearer ${document.cookie.split('=')[1]}`;
        try {

            const res = axios.post("api/blog/new", post.value, {
                headers: { authorization: token }
            });
        } catch (error) {
            message.value = {
                type: 'error',
                text: 'Impossibile inviare il post'
            }
        }


        message.value = {
            type: 'success',
            text: 'Post creato con successo!'
        }

        // Resetta il form dopo 2 secondi
        setTimeout(() => {
            resetForm()
            router.push('/') // Reindirizza alla home dopo il successo
        }, 2000)

    } catch (error) {
        console.error('Errore durante la creazione del post:', error)
        message.value = {
            type: 'error',
            text: 'Errore durante il salvataggio del post. Riprova più tardi.'
        }
    }
}

const resetForm = () => {
    post.value = {
        title: '',
        content: '',
    }
}
</script>
