import apiRoutes from "./routes/api.js";
import express from "express";
import pool from './db.js';
import cors from 'cors';
import path from "path";
import morgan from 'morgan';

const app = express()

pool.getConnection()
  .then((pool) => {
    // dopo devo toglierlo lol
    app.use(cors());

    // logger
    app.use(morgan('dev'));

    // parse request
    app.use(express.json());

    // start every request with /api/
    app.use('/api', apiRoutes)

    const PORT = process.env.PORT || 3000;

    app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server in ascolto su 0.0.0.0:${PORT}`);

        // Test query

        pool.query('SELECT 1')
          .then(([rows]) => {
            console.log("Query test riuscita:", rows);
          })
          .catch(err => {
            console.error("Query test fallita:", err);
          });
      });
  })
  .catch(err => {
    console.error('❌ Connessione al DB fallita:', err);
    process.exit(1);
  });
