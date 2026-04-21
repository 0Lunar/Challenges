<script setup>
import Navbar from "./utils/Navbar.vue";
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();
const username = ref("");
const password = ref("");
const error = ref("");

const handleLogin = async () => {
    try {
        const response = await axios.post("/api/auth/login", {
            username: username.value,
            password: password.value,
        });

        document.cookie = `token=${response.data.token}; path=/; secure;`;
        router.push("/");
    } catch (err) {
        error.value = err.response.data.err || "Errore durante il login";
    }
};
</script>

<template>
    <Navbar />
    <div class="min-h-screen bg-gray-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-md">
            <h2 class="text-center text-3xl font-extrabold text-white">
                Accedi al tuo account
            </h2>
            <p class="mt-2 text-center text-sm text-gray-400">
                Oppure
                <router-link to="/register" class="font-medium text-indigo-400 hover:text-indigo-300">
                    registra un nuovo account
                </router-link>
            </p>
        </div>

        <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
            <div class="bg-gray-800 py-8 px-4 shadow-xl sm:rounded-lg sm:px-10">
                <form class="space-y-6" @submit.prevent="handleLogin">
                    <div v-if="error" class="rounded-md bg-red-900/50 p-4">
                        <p class="text-sm text-red-200">{{ error }}</p>
                    </div>

                    <div>
                        <label for="username" class="block text-sm font-medium text-gray-300">
                            Username
                        </label>
                        <div class="mt-1">
                            <input id="username" v-model="username" name="username" type="text" autocomplete="username"
                                required
                                class="bg-gray-700 appearance-none block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-white sm:text-sm" />
                        </div>
                    </div>

                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-300">
                            Password
                        </label>
                        <div class="mt-1">
                            <input id="password" v-model="password" name="password" type="password"
                                autocomplete="current-password" required
                                class="bg-gray-700 appearance-none block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-white sm:text-sm" />
                        </div>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="text-sm">
                            <a href="#" class="font-medium text-indigo-400 hover:text-indigo-300">
                                Password dimenticata?
                            </a>
                        </div>
                    </div>

                    <div>
                        <button type="submit"
                            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:ring-offset-gray-800">
                            Accedi
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* Stili aggiuntivi se necessari */
</style>
