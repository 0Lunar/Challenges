import express from 'express';
import { getPosts, getPostById, deletePostById, newPost, editPostById } from '../controllers/blogController.js';
import { authenticateToken, requireAdmin, requireWriter } from '../middlewares/authMiddleware.js';

const router = express.Router();

router.get('/posts', getPosts);
router.get('/posts/:id', getPostById);
router.delete('/posts/:id', authenticateToken, requireAdmin, deletePostById);
router.put('/posts/:id', authenticateToken, requireAdmin, editPostById);
router.post('/new', authenticateToken, requireWriter, newPost);

export default router;
