import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/PostListView.vue')
  },
  {
    path: '/post/:id',
    name: 'Post',
    component: () => import('@/views/BlogPostView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/RegisterView.vue')
  },
  {
    path: '/newpost',
    name: 'newpost',
    component: () => import('@/views/NewPostView.vue'),
    meta: { requiresAuth: true, requiredRole: 'user' }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

type UserRole = 'user' | 'writer' | 'admin';
type RoleHierarchy = {
  [key in UserRole]: number;
} & {
  '': number;
  undefined: number;
  null: number;
};

router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth) {
      const token = document.cookie.split('=')[1];

      if (!token) {
        return next('/login');
      }

      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        const userRole = payload.role as string;

        if (to.meta.requiredRole) {
          const roleHierarchy: RoleHierarchy = {
            'user': 0,
            'writer': 1,
            'admin': 2,
            '': -1,
            'undefined': -1,
            'null': -1
          };

          const requiredRole = String(to.meta.requiredRole) as keyof RoleHierarchy;
          const requiredLevel = roleHierarchy[requiredRole] ?? 999;

          const safeUserRole = String(userRole) as keyof RoleHierarchy;
          const userLevel = roleHierarchy[safeUserRole] ?? -1;

          if (userLevel < requiredLevel) {
            return next({ path: '/', query: { error: 'Non hai i permessi necessari per accedere a questa pagina' } });
          }
        }

        next();
      } catch (error) {
        console.error('Error verifying token:', error);
        document.cookie = 'token=; Max-Age=0; path=/; SameSite=Lax';
        next('/login');
      }
    } else {
      next();
    }
  });

export default router;
