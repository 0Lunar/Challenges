import express from 'express';
import { getUsers, getUserById, editUserById, deleteUserById } from '../controllers/userController.js';
import { authenticateToken, requireAdmin } from '../middlewares/authMiddleware.js';

const router = express.Router();

router.get('/', authenticateToken, requireAdmin, getUsers);
router.post('/:id', authenticateToken, requireAdmin, getUserById);
router.put('/:id', authenticateToken, requireAdmin, editUserById);
router.delete('/:id', authenticateToken, requireAdmin, deleteUserById);

export default router;
