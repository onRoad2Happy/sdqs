const express = require('express');
const router = express.Router();


const tableService = require('../services/tableService');


// GET /api/v1/tables
router.get('/tables', function(req, res) {
    tableService.getTables()
    .then(tables => res.json(tables))
});



// GET /api/v1/tables/:id
router.get('/tables/:id', function(req, res) {
    const id = req.params.id;
    tableService.getTable(+id)
        .then(table => res.json(table));
});

module.exports = router;