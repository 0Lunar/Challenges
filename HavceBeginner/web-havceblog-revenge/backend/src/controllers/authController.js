import jwt from "jsonwebtoken";
import bcrypt from "bcryptjs";
import pool from "../db.js";

export const registerUser = async (req, res) => {
    const { displayname, username, password } = req.body;

    try {
        const hash = await bcrypt.hash(password, 10);
        const [result] = await pool.query("INSERT INTO users (displayname, username, password, role) VALUES (?, ?, ?, 'user')", [displayname, username, hash]);

        res.json({ status: "user registered ", userId: result.insertId });
    } catch (err) {
        res.status(500).json({ status: "Unable to register user" });
        console.error("query failed:", err);
    }
};

export const loginUser = async (req, res) => {
    const { username, password } = req.body;

    try {
        const [rows] = await pool.query("SELECT password, role FROM users WHERE username = ?", [username]);

        if (rows.length === 0) {
            return res.status(401).json({ err: "Invalid credentials" });
        }

        const { password: hash, role } = rows[0];
        const match = await bcrypt.compare(password, hash);
        if (!match) {
            return res.status(401).json({ err: "Invalid credentials" });
        }

        const token = jwt.sign({ username: username, role: rows[0].role }, process.env.SECRET, {
            expiresIn: '2h'
        });
        res.json({ token });
    } catch (err) {
        res.status(500).json({ err: "Unable to login user" });
        console.error("Query failed:", err);
    }
};
