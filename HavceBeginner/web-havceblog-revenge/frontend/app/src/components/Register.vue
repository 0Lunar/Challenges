<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import Navbar from "./utils/Navbar.vue";

const router = useRouter();
const name = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const error = ref("");
const displayName = ref("");

const handleRegister = async () => {
    if (password.value !== confirmPassword.value) {
        error.value = "Le password non corrispondono";
        return;
    }

    try {
        const response = await axios.post("/api/auth/register", {
            username: name.value,
            password: password.value,
            displayname: displayName.value
        });

        router.push("/login");
    } catch (err) {
        error.value = err.response?.data?.message || "Errore durante la registrazione";
    }
};
</script>

<template>
    <Navbar />
    <div class="min-h-screen bg-gray-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div class="sm:mx-auto sm:w-full sm:max-w-md">
            <h2 class="text-center text-3xl font-extrabold text-white">
                Crea un nuovo account
            </h2>
            <p class="mt-2 text-center text-sm text-gray-400">
                <router-link to="/login" class="font-medium text-indigo-400 hover:text-indigo-300">
                    accedi al tuo account
                </router-link>
            </p>
        </div>

        <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
            <div class="bg-gray-800 py-8 px-4 shadow-xl sm:rounded-lg sm:px-10">
                <form class="space-y-6" @submit.prevent="handleRegister">
                    <div v-if="error" class="rounded-md bg-red-900/50 p-4">
                        <p class="text-sm text-red-200">{{ error }}</p>
                    </div>

                    <div>
                        <label for="name" class="block text-sm font-medium text-gray-300">
                            Nome
                        </label>
                        <div class="mt-1">
                            <input id="name" v-model="name" name="name" type="text" autocomplete="name" required
                                class="bg-gray-700 appearance-none block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-white sm:text-sm" />
                        </div>
                    </div>

                    <div>
                        <label for="name" class="block text-sm font-medium text-gray-300">
                            Display Name
                        </label>
                        <div class="mt-1">
                            <input id="displayName" v-model="displayName" name="displayName" type="text"
                                autocomplete="displayName" required
                                class="bg-gray-700 appearance-none block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-white sm:text-sm" />
                        </div>
                    </div>

                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-300">
                            Password
                        </label>
                        <div class="mt-1">
                            <input id="password" v-model="password" name="password" type="password"
                                autocomplete="new-password" required
                                class="bg-gray-700 appearance-none block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-white sm:text-sm" />
                        </div>
                    </div>

                    <div>
                        <label for="confirm-password" class="block text-sm font-medium text-gray-300">
                            Conferma Password
                        </label>
                        <div class="mt-1">
                            <input id="confirm-password" v-model="confirmPassword" name="confirm-password"
                                type="password" autocomplete="new-password" required
                                class="bg-gray-700 appearance-none block w-full px-3 py-2 border border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-white sm:text-sm" />
                        </div>
                    </div>

                    <div>
                        <button type="submit"
                            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 focus:ring-offset-gray-800">
                            Registrati
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
