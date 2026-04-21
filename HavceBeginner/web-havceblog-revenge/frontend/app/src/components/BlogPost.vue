<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import MarkdownIt from "markdown-it";
import DOMPurify from "dompurify";
import hljs from "highlight.js";
import Navbar from "./utils/Navbar.vue";
import "highlight.js/styles/atom-one-dark.css";

const md = new MarkdownIt({
    html: true,
    breaks: true,
    linkify: true,
    typographer: true,
    xhtmlOut: true,
    highlight: function (str, lang) {
        if (lang && hljs.getLanguage(lang)) {
            try {
                return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang }).value}</code></pre>`;
            } catch (_) { }
        }
        return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`;
    },
});

const route = useRoute();
const post = ref(null);

onMounted(async () => {
    const res = await axios.get(`/api/blog/posts/${route.params.id}`);
    post.value = res.data;
});

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
        second: '2-digit'
    }).format(date);
}

</script>
<template>
    <Navbar />
    <div v-if="post" class="min-h-screen bg-gray-900 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-4xl mx-auto">
            <!-- Article Container -->
            <article class="bg-gray-800 rounded-xl shadow-2xl overflow-hidden">
                <!-- Article Header -->
                <header class="border-b border-gray-700 p-6 sm:p-8">
                    <div class="flex items-center justify-between mb-4">
                        <span
                            class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-indigo-900 text-indigo-200">
                            {{ post.category || 'Generale' }}
                        </span>
                        <span class="text-sm text-gray-400">{{ formatDate(post.timestamp) }}</span>
                    </div>

                    <h1 class="text-3xl sm:text-4xl font-bold text-white mb-4">
                        {{ post.title }}
                    </h1>

                    <div class="flex items-center space-x-3">
                        <div class="flex-shrink-0">
                            <span class="text-2xl">👤</span>
                        </div>
                        <div>
                            <p class="text-sm font-medium text-gray-300">{{ post.author }}</p>
                            <p class="text-xs text-gray-500">{{ post.reading_time || '5 min' }} di lettura</p>
                        </div>
                    </div>
                </header>

                <!-- Article Content -->
                <div class="prose prose-invert max-w-none p-6 sm:p-8" v-html="render(post.content)"></div>

                <!-- Article Footer -->
                <footer class="border-t border-gray-700 p-6 sm:p-8">
                    <router-link to="/"
                        class="inline-flex items-center text-indigo-400 hover:text-indigo-300 transition-colors">
                        ← Torna agli articoli
                    </router-link>
                </footer>
            </article>
        </div>
    </div>
</template>

<style>
.prose {
    color: #e5e7eb;
}

.prose h1,
.prose h2,
.prose h3,
.prose h4 {
    color: #f3f4f6;
}

.prose a {
    color: #818cf8;
    text-decoration: none;
    transition: color 0.2s;
}

.prose a:hover {
    color: #6366f1;
    text-decoration: underline;
}

.prose code {
    @apply bg-gray-700 text-indigo-200 px-2 py-1 rounded;
}

.prose pre {
    @apply bg-gray-700 border border-gray-600 rounded-lg overflow-x-auto;
}

.prose pre code {
    @apply bg-transparent p-0;
}

.prose blockquote {
    @apply border-l-4 border-indigo-500 pl-4 italic text-gray-300;
}

.prose img {
    @apply rounded-lg shadow-lg mx-auto;
}

.hljs {
    @apply rounded-lg p-4 overflow-x-auto !important;
}

.hljs code {
    @apply rounded-lg p-4 overflow-x-auto;
}

.prose table {
    @apply w-full border-collapse;
}

.prose th {
    @apply bg-gray-700 text-left px-4 py-2 border-b border-gray-600;
}

.prose td {
    @apply px-4 py-2 border-b border-gray-700;
}
</style>
