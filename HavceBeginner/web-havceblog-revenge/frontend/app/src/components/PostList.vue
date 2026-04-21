<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute } from 'vue-router'
import axios from "axios";
import Navbar from "./utils/Navbar.vue";
import MarkdownIt from "markdown-it";
import DOMPurify from "dompurify";

const md = new MarkdownIt({
    html: true,
    breaks: true,
    linkify: true,
    typographer: true,
    xhtmlOut: true,
});

const route = useRoute()
const error = route.query.error

const posts = ref([]);
const isAuthenticated = ref(false);
const currentPage = ref(1);
const postsPerPage = 5;

onMounted(async () => {
    isAuthenticated.value = !!document.cookie;

    const res = await axios.get("/api/blog/posts");
    posts.value = res.data
        .map((post) => ({
            ...post,
            content: post.content.trim(),
        }))
        .reverse();
});

const paginatedPosts = computed(() => {
    const start = (currentPage.value - 1) * postsPerPage;
    const end = start + postsPerPage;
    return posts.value.slice(start, end);
});

const totalPages = computed(() => {
    return Math.ceil(posts.value.length / postsPerPage);
});

const nextPage = () => {
    if (currentPage.value < totalPages.value) {
        currentPage.value++;
    }
};

const prevPage = () => {
    if (currentPage.value > 1) {
        currentPage.value--;
    }
};

const goToPage = (page) => {
    currentPage.value = page;
};

const render = (content) => {
    const cleanedContent = content.trim().replace(/^\s+/gm, "");
    return DOMPurify.sanitize(md.render(cleanedContent));
};

const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    return new Intl.DateTimeFormat('it-IT', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    }).format(date);
}
</script>

<template>
    <Navbar />
    <div class="min-h-screen bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-4xl mx-auto">
            <div class="flex justify-between items-center mb-12">
                <div class="text-center w-full">
                    <p class="text-xl text-gray-400">Pensieri ed idee sulle guerre economiche</p>
                </div>
            </div>

            <div v-if="error"
                class="bg-red-900/50 border border-red-700 text-red-200 px-6 py-4 mb-8 rounded-lg shadow-md animate-fade-in">
                <div class="flex items-start space-x-3">
                    <span class="text-2xl">❌</span>
                    <p class="text-sm sm:text-base leading-relaxed">
                        {{ error }}
                    </p>
                </div>
            </div>

            <div class="space-y-6">
                <article v-for="post in paginatedPosts" :key="post.id" @click="$router.push(`/post/${post.id}`)"
                class="group bg-gray-800 rounded-xl shadow-lg overflow-hidden transition-all duration-300 hover:shadow-xl hover:-translate-y-1 cursor-pointer border border-gray-700 hover:border-indigo-500">
                    <div class="p-6 sm:p-8">
                        <div class="flex items-center justify-between mb-4">
                            <span
                                class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-900 text-indigo-200">
                                {{ post.category || 'Generale' }}
                            </span>
                            <span class="text-sm text-gray-400">🕒 {{ formatDate(post.timestamp) }}</span>
                        </div>

                        <h2
                            class="text-2xl font-bold text-white group-hover:text-indigo-400 transition-colors duration-200 mb-3">
                            {{ post.title }}
                        </h2>

                        <div class="flex items-center text-gray-400 mb-4">
                            <span class="inline-block mr-2">✍️</span>
                            <span class="font-medium">{{ post.author }}</span>
                        </div>

                        <div class="prose prose-invert max-w-none text-gray-300 mb-4 line-clamp-3"
                            v-html="render(post.content.slice(0, 200) + '...')"></div>

                        <div class="flex justify-between items-center mt-6">
                            <span
                                class="text-indigo-400 font-medium group-hover:text-indigo-300 transition-colors duration-200">
                                Leggi tutto →
                            </span>
                            <span class="text-sm text-gray-500">{{ post.reading_time || '3 min' }} di lettura</span>
                        </div>
                    </div>
                </article>
            </div>

            <!-- Pagination Controls -->
            <div v-if="totalPages > 1" class="mt-12 flex items-center justify-center space-x-2 space-y-3 py-4">
                <button @click="prevPage" :disabled="currentPage === 1"
                    class="px-4 py-2 rounded-md bg-gray-800 text-gray-300 hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors border border-gray-700">
                    &larr; Precedente
                </button>

                <div class="flex space-x-2">
                    <button v-for="page in totalPages" :key="page" @click="goToPage(page)"
                        :class="['px-3 py-1 rounded-md transition-colors', currentPage === page ? 'bg-indigo-600 text-white' : 'bg-gray-800 text-gray-300 hover:bg-gray-700']">
                        {{ page }}
                    </button>
                </div>

                <button @click="nextPage" :disabled="currentPage === totalPages"
                    class="px-4 py-2 rounded-md bg-gray-800 text-gray-300 hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors border border-gray-700">
                    Successiva &rarr;
                </button>
            </div>
        </div>
    </div>
</template>

<style>
.prose-invert {
    --tw-prose-body: #e5e7eb;
    --tw-prose-headings: #f3f4f6;
    --tw-prose-lead: #d1d5db;
    --tw-prose-links: #818cf8;
    --tw-prose-code: #f0f0f0;
    --tw-prose-pre-code: #f0f0f0;
    --tw-prose-quotes: #e5e7eb;
}

.prose-invert code {
    @apply bg-gray-700 text-indigo-200 px-2 py-1 rounded;
}

.prose-invert pre {
    @apply bg-gray-700 border border-gray-600 rounded-lg overflow-x-auto;
}

.prose-invert pre code {
    @apply bg-transparent p-0;
}

.line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

@keyframes fade-in {
    0% {
        opacity: 0;
        transform: translateY(-6px);
    }

    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in {
    animation: fade-in 0.4s ease-out;
}
</style>
