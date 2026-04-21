import pool from "../db.js"

export const getUsers = (req, res) => {
    pool.query('SELECT id, displayname, username, lastlogin, role FROM users')
    .then(([rows]) => {
        res.json(rows);
    })
    .catch(err => {
      console.error("Query test fallita:", err);
    });
}

export const getUserById = (req, res) => {
    const { id } = req.params;
    pool.query('SELECT displayname, lastlogin, role FROM users WHERE id = ?', [id])
    .then(([rows]) => {
        res.json(rows);
    })
    .catch(err => {
        res.status(500);
        res.json({"err" : "Impossible to get this user"});
        console.error("Query fallita:", err);
    });
}

export const editUserById = (req, res) => {
    const { id } = req.params;
    const { displayname, role } = req.body;

    pool.query('UPDATE users SET displayname = ?, role = ? WHERE id = ?', [displayname, role, id])
    .then(([result]) => {
        if (result.affectedRows > 0) {
            res.json({ status: "User edited successfully" });
        } else {
            res.status(404).json({ message: "User not found" });
        }
    })
    .catch(err => {
        res.status(500).json({ err: "Unable to edit the user" });
        console.error("Query failed:", err);
    });   
}

export const deleteUserById = (req, res) => {
    const { id } = req.params;

    pool.query('DELETE FROM users WHERE id = ?', [id])
    .then(([result]) => {
        if (result.affectedRows > 0) {
            res.json({ status: "User deleted successfully" });
        } else {
            res.status(404).json({ message: "User not found" });
        }
    })
    .catch(err => {
        res.status(500).json({ err: "Unable to delete the user" });
        console.error("Query failed:", err);
    });   
}