<template>
    <header class="bg-gray-800 border-b border-gray-700">
        <div class="container mx-auto px-4 py-3 flex items-center">
            <div class="flex items-center space-x-6">
                <router-link to="/" class="text-white flex items-center">
                    <font-awesome-icon :icon="['fas', 'newspaper']" class="h-6 w-6 text-indigo-400 mr-2" />
                    <span class="text-xl font-bold">havce's blog</span>
                </router-link>

                <nav class="hidden md:flex space-x-4">
                    <router-link to="/" class="text-gray-300 hover:text-white px-3 py-2 text-sm font-medium"
                        active-class="text-white">
                        Home
                    </router-link>
                    <router-link v-if="isAuthenticated"  to="/newpost" class="text-gray-300 hover:text-white px-3 py-2 text-sm font-medium"
                        active-class="text-white">
                        Nuovo Post
                    </router-link>
                </nav>
            </div>
            <button v-if="!isAuthenticated"
                @click="$router.push('/login')"
                class="absolute top-3 right-6 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors duration-200">
                Login
            </button>

            <button v-else
                @click="logout"
                class="absolute top-3 right-6 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors duration-200">
                Logout
            </button>
        </div>
    </header>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();

const isAuthenticated = ref(false);
const showDashboard = ref(false);
const isAdmin = ref(false);

onMounted(() => {
  const cookie = document.cookie;
  const token = cookie.split('=')[1];

  isAuthenticated.value = !!token;

  if (token) {
    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      const role = payload.role;

      const roleHierarchy = {
        'user': 0,
        'writer': 1,
        'admin': 2
      };

      const userLevel = roleHierarchy[role] ?? -1;
      showDashboard.value = userLevel >= roleHierarchy['admin'];
    } catch (err) {
      console.error('Token decode error:', err);
      showDashboard.value = false;
    }
  }
});

const logout = () => {
    deleteCookie("token");
    router.push("/login");
};

const deleteCookie = (name) => {
    document.cookie = `${name}=; Max-Age=0; path=/; SameSite=Lax`;
};
</script>

