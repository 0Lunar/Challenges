import pool from "../db.js"

export const getPosts = (req, res) => {
    pool.query('SELECT posts.id, displayname as author, role as author_role, title, content, timestamp FROM posts JOIN users ON users.id = posts.id_author')
        .then(([rows]) => {
            if (rows.length > 0) {
                res.json(rows);
            } else {
                res.status(404).json({ message: "No posts found" });
            }
        })
        .catch(err => {
            res.status(500).json({ err: "Unable to fetch posts" });
            console.error("Query failed:", err);
        });
};

export const newPost = (req, res) => {
    const { title, content } = req.body;
    const user = req.user;

    pool.query("SELECT id FROM users WHERE username = ?", [user.username])
        .then(([rows]) => {
            if (rows.length > 0) {
                const userId = rows[0].id;
                pool.query("INSERT INTO posts (title, content, id_author) VALUES (?, ?, ?)", [title, content, userId])
                    .then(([result]) => {
                        res.json({ status: "Post added successfully", postId: result.insertId });
                    })
                    .catch((err) => {
                        res.status(500);
                        res.json({ err: "Unable to add new post" });
                        console.error("Query failed:", err);
                    });
            } else {
                res.status(400);
                res.json({ err: "User not found" });
            }
        })
        .catch((err) => {
            res.status(500);
            res.json({ err: "Unable to add new post" });
            console.error("Query failed:", err);
        });
};


export const getPostById = (req, res) => {
    const { id } = req.params;

    const query = `SELECT displayname as author, title, content, timestamp
                   FROM posts
                   JOIN users ON users.id = posts.id_author
                   WHERE posts.id = ${id}`;

    pool.query(query)
        .then(([rows]) => {
            if (rows.length > 0) {
                res.json(rows[0]);
            } else {
                res.status(404).json({ message: "Post not found" });
            }
        })
        .catch(err => {
            res.status(500).json({ err: "Unable to fetch the post" });
            console.error("Query failed:", err);
        });
};

export const deletePostById = (req, res) => {
    const { id } = req.params;
    pool.query('DELETE FROM posts WHERE id = ?', [id])
        .then(([result]) => {
            if (result.affectedRows > 0) {
                res.json({ status: "Post deleted successfully" });
            } else {
                res.status(404).json({ message: "Post not found" });
            }
        })
        .catch(err => {
            res.status(500).json({ err: "Unable to delete the post" });
            console.error("Query failed:", err);
        });
};

export const editPostById = (req, res) => {
    const { id } = req.params;
    const { title, content } = req.body;

    pool.query('UPDATE posts SET title = ?, content = ? WHERE id = ?', [title, content, id])
    .then(([result]) => {
        if (result.affectedRows > 0) {
            res.json({ status: "Post edited successfully" });
        } else {
            res.status(404).json({ message: "Post not found" });
        }
    })
    .catch(err => {
        res.status(500).json({ err: "Unable to edit the post" });
        console.error("Query failed:", err);
    });
}
